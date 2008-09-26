from zope import schema
from zope.interface import implements
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.ATContentTypes.content.image import ATImageSchema

from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.portlet.collection.collection import ICollectionPortlet
from plone.portlet.collection import collection
from plone.portlet.collection import PloneMessageFactory as _
from plone.memoize import forever
from plone.memoize import instance
from plone.app.portlets.portlets import base


@forever.memoize
def getATImageWidths():
    field = ATImageSchema['image']
    result = dict()
    widths = [(name, size[0]) for name, size in field.sizes.items()]

    def width_cmp(a, b):
        return cmp(a[1], b[1])

    widths.sort(cmp=width_cmp)
    return widths


class IImagesPortlet(ICollectionPortlet):
    """A portlet which renders the images
       among the results of a collection object.
    """

    width = schema.Int(title=_(u"Image width"),
                             description=_(u"Width of the images"),
                             required=True)


class Assignment(collection.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IImagesPortlet)

    def __init__(self, header=u"", target_collection=None, limit=None,
        random=False, show_more=True, show_dates=False, width=200):
        super(Assignment, self).__init__(header, target_collection, limit,
            random, show_more, show_dates)
        self.width = width


class Renderer(collection.Renderer):

    _template = ViewPageTemplateFile('images.pt')

    render = _template

    @instance.memoize
    def getImageFormat(self):
        for format, width in getATImageWidths():
            if self.data.width <= width:
                return format
        return getATImageWidths()[-1][0]

    def getURLWithFormat(self, url):
        return '%s/image_%s' % (url, self.getImageFormat())

    def results(self):
        return super(Renderer, self)._results(Type=("Image", ))


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IImagesPortlet).omit('show_dates')
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Add Images Portlet")
    description = _(u"This portlet display a listing"
        " of images from a Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IImagesPortlet).omit('show_dates')
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Edit Images Portlet")
    description = _(u"This portlet display a listing"
        " of images from a Collection.")
