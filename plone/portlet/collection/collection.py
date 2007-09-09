from zope.interface import Interface

from zope.interface import implements
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget


from plone.portlet.collection import CollectionMessageFactory as _

class ICollectionPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object.
    """
    # is it wrong for this one to inherid IPortletDataProvider? 

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    target_collection = schema.Choice(title=_(u"Target collection"),
                                  description=_(u"As a path relative to the portal root."),
                                  required=True,
                                  source=SearchableTextSourceBinder({'is_folderish' : True}))
                                  # The source above needs to be changed. 
                                  # Right now it lists everything folderish.
                                  # It should only list collections



class Assignment(base.Assignment):
    """
    Portlet assignment.    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICollectionPortlet)

    header = u""
    target_collection=None

    def __init__(self, header=u"", target_collection=None):
        self.header = header
        self.target_collection=target_collection

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.
    
    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """


    render = ViewPageTemplateFile('collection.pt')


    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()


    def hasCollection(self):
        """ 
        test if we have a collection at all
        We can use this to check if we should render the portlet at all
        """
        return self.getCollection() is not None



    def getCollection(self):
        """ get the collection the portlet is pointing to"""
        collection_path = self.data.target_collection

        # it feels insane that i need to do manual strippping of the first slash in this string.
        # I must be doing something wrong
        # please make this bit more sane

        if collection_path is None or len(collection_path)==0:
            return None
        # The portal root is never a collection

        if collection_path[0]=='/':
            collection_path = collection_path[1:]
        collection = self.portal.restrictedTraverse(collection_path, default=None)

        # we should also check that the returned object implements the interfaces for collection
        # So that we don't accidentally return folders and stuff that will make things break
        return collection


    def results(self):
        """ get the actual result brains from the collection"""

        collection = self.getCollection()
        results = collection.queryCatalog()
        return results



class AddForm(base.AddForm):
    """Portlet add form.
    
    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICollectionPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    
    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(ICollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

