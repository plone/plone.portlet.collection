from ComputedAttribute import ComputedAttribute
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.portlets.browser import formhelper
from plone.app.portlets.portlets import base
from plone.app.uuid.utils import uuidToObject
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlet.collection import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.defaultpage import is_default_page
from Products.CMFPlone.interfaces.controlpanel import ISiteSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MimetypesRegistry.MimeTypeItem import guess_icon_path
from zExceptions import NotFound
from zope import schema
from zope.component import getUtility
from zope.interface import implementer

import os
import random


COLLECTIONS = []

try:
    from plone.app.collection.interfaces import ICollection

    COLLECTIONS.append(ICollection.__identifier__)
except ImportError:
    pass

try:
    from plone.app.contenttypes.interfaces import ICollection

    COLLECTIONS.append(ICollection.__identifier__)
except ImportError:
    pass


class ICollectionPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object."""

    header = schema.TextLine(
        title=_("Portlet header"),
        description=_("Title of the rendered portlet"),
        required=True,
    )

    widget(
        "uid",
        RelatedItemsFieldWidget,
        pattern_options={"selectableTypes": ["Collection"]},
    )
    uid = schema.Choice(
        title=_("Target collection"),
        description=_("Find the collection which provides the items to list"),
        required=True,
        vocabulary="plone.app.vocabularies.Catalog",
    )

    limit = schema.Int(
        title=_("Limit"),
        description=_(
            "Specify the maximum number of items to show in the "
            "portlet. Leave this blank to show all items."
        ),
        required=False,
    )

    random = schema.Bool(
        title=_("Select random items"),
        description=_(
            "If enabled, items will be selected randomly from the "
            "collection, rather than based on its sort order."
        ),
        required=False,
        default=False,
    )

    show_more = schema.Bool(
        title=_("Show more... link"),
        description=_(
            "If enabled, a more... link will appear in the footer "
            "of the portlet, linking to the underlying "
            "Collection."
        ),
        required=False,
        default=True,
    )

    show_dates = schema.Bool(
        title=_("Show dates"),
        description=_(
            "If enabled, effective dates will be shown underneath " "the items listed."
        ),
        required=False,
        default=False,
    )

    exclude_context = schema.Bool(
        title=_("Exclude the Current Context"),
        description=_(
            "If enabled, the listing will not include the current item the "
            "portlet is rendered for if it otherwise would be."
        ),
        required=False,
        default=True,
    )

    no_icons = schema.Bool(
        title=_("Suppress Icons"),
        description=_("If enabled, the portlet will not show document type icons."),
        required=False,
        default=False,
    )

    thumb_scale = schema.TextLine(
        title=_("Override thumb scale"),
        description=_(
            "Enter a valid scale name"
            " (see 'Image Handling' control panel) to override"
            " (e.g. icon, tile, thumb, mini, preview, ... )."
            " Leave empty to use default (see 'Site' control panel)."
        ),
        required=False,
        default="",
    )

    no_thumbs = schema.Bool(
        title=_("Suppress thumbs"),
        description=_("If enabled, the portlet will not show thumbs."),
        required=False,
        default=False,
    )


@implementer(ICollectionPortlet)
class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    header = ""
    limit = None
    random = False
    show_more = True
    show_dates = False
    exclude_context = False
    no_icons = False
    no_thumbs = False
    thumb_scale = None
    # bbb
    target_collection = None

    def __init__(
        self,
        header="",
        uid=None,
        limit=None,
        random=False,
        show_more=True,
        show_dates=False,
        exclude_context=True,
        no_icons=False,
        no_thumbs=False,
        thumb_scale=None,
    ):
        self.header = header
        self.uid = uid
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.exclude_context = exclude_context
        self.no_icons = no_icons
        self.no_thumbs = no_thumbs
        self.thumb_scale = thumb_scale

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header

    def _uid(self):
        # This is only called if the instance doesn't have a uid
        # attribute, which is probably because it has an old
        # 'target_collection' attribute that needs to be converted.
        path = self.target_collection
        portal = getToolByName(self, "portal_url").getPortalObject()
        try:
            collection = portal.unrestrictedTraverse(path.lstrip("/"))
        except (AttributeError, KeyError, TypeError, NotFound):
            return
        return collection.UID()

    uid = ComputedAttribute(_uid, 1)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile("collection.pt")
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return len(self.results())

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return
        parent = collection.aq_parent
        if is_default_page(parent, collection):
            collection = parent
        return collection.absolute_url()

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-collection-%s" % normalizer.normalize(header)

    @memoize
    def results(self):
        if self.data.random:
            return self._random_results()
        else:
            return self._standard_results()

    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            context_path = "/".join(self.context.getPhysicalPath())
            exclude_context = getattr(self.data, "exclude_context", False)
            limit = self.data.limit
            if limit and limit > 0:
                # pass on batching hints to the catalog
                results = collection.queryCatalog(
                    batch=True, b_size=limit + exclude_context
                )
                results = results._sequence
            else:
                results = collection.queryCatalog()
            if exclude_context:
                results = [
                    brain for brain in results if brain.getPath() != context_path
                ]
            if limit and limit > 0:
                results = results[:limit]
        return results

    def _random_results(self):
        # intentionally non-memoized
        results = []
        collection = self.collection()
        if collection is not None:
            context_path = "/".join(self.context.getPhysicalPath())
            exclude_context = getattr(self.data, "exclude_context", False)
            results = collection.queryCatalog(sort_on=None)
            if results is None:
                return []
            limit = self.data.limit and min(len(results), self.data.limit) or 1

            if exclude_context:
                results = [
                    brain for brain in results if brain.getPath() != context_path
                ]
            if len(results) < limit:
                limit = len(results)
            results = random.sample(results, limit)

        return results

    @memoize
    def collection(self):
        return uuidToObject(self.data.uid)

    def include_empty_footer(self):
        """Whether or not to include an empty footer element when the more
        link is turned off.
        Always returns True (this method provides a hook for
        sub-classes to override the default behaviour).
        """
        return True

    @memoize
    def thumb_scale(self):
        """Use override value or read thumb_scale from registry.
        Image sizes must fit to value in allowed image sizes.
        None will suppress thumb.
        """
        if self.data.thumb_scale:
            return self.data.thumb_scale
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema, prefix="plone", check=False)
        if settings.no_thumbs_portlet:
            return None
        thumb_scale_portlet = settings.thumb_scale_portlet
        return thumb_scale_portlet

    def getMimeTypeIcon(self, obj):
        fileo = obj.getObject().file
        portal_url = getNavigationRoot(self.context)
        mtt = getToolByName(self.context, "mimetypes_registry")
        if fileo.contentType:
            ctype = mtt.lookup(fileo.contentType)
            return os.path.join(portal_url, guess_icon_path(ctype[0]))
        return None


class AddForm(formhelper.AddForm):
    schema = ICollectionPortlet
    label = _("Add Collection Portlet")
    description = _("This portlet displays a listing of items from a " "Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(formhelper.EditForm):
    schema = ICollectionPortlet
    label = _("Edit Collection Portlet")
    description = _("This portlet displays a listing of items from a " "Collection.")
