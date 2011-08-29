from plone.app.portlets.storage import PortletAssignmentMapping
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, getMultiAdapter

from plone.portlet.collection import collection
from plone.portlet.collection.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='plone.portlet.collection.Collection')
        self.assertEquals(portlet.addview, 'plone.portlet.collection.Collection')

    def testInterfaces(self):
        portlet = collection.Assignment(header=u"title")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='plone.portlet.collection.Collection')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={'header': u"test title"})
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], collection.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = collection.Assignment(header=u"title")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, collection.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = collection.Assignment(header=u"title")

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, collection.Renderer))


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or collection.Assignment(header=u"title")

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal, assignment=collection.Assignment(header=u"title"))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.assertTrue('title' in output)

    def test_collection_path_unicode(self):
        # Cover problem in #9184
        r = self.renderer(context=self.portal,
                          assignment=collection.Assignment(header=u"title",
                                                           target_collection=u"/events"))
        r = r.__of__(self.folder)
        self.assertEqual(r.collection().id, 'events')

    def test_css_class(self):
        r = self.renderer(context=self.portal,
                          assignment=collection.Assignment(header=u"Welcome text"))
        self.assertEquals('portlet-collection-welcome-text', r.css_class())


class TestCollectionQuery(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.collection = self._createType(self.folder, 'Topic', 'collection')

    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog

        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        return obj

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def testPortletAvailabilityWithPrivateFolders(self):
        private_folder = self._createType(self.folder, 'Folder', 'private')
        public_subfolder = self._createType(private_folder, 'Folder', 'public')
        self.portal.portal_workflow.doActionFor(public_subfolder, 'publish')
        self.collection = self._createType(public_subfolder, 'Topic', 'collection')
        self.portal.portal_workflow.doActionFor(self.collection, 'publish')

        mapping = PortletAssignmentMapping()
        mapping['foo'] = collection.Assignment(header=u"title",
                target_collection='/Members/test_user_1_/private/public/collection')
        self.logout()
        collectionrenderer = self.renderer(context=None, request=None, view=None, manager=None, assignment=mapping['foo'])

        self.assertEquals(self.collection, collectionrenderer.collection())

    def testSimpleQuery(self):
        # set up our collection to search for Folders
        crit = self.folder.collection.addCriterion('portal_type', 'ATSimpleStringCriterion')
        crit.setValue('Folder')

        # add a few folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s'%i)
            getattr(self.folder, 'folder_%s'%i).reindexObject()

        # the folders are returned by the topic
        collection_num_items = len(self.folder.collection.queryCatalog())
        # We better have some folders
        self.failUnless(collection_num_items >= 6)

        mapping = PortletAssignmentMapping()
        mapping['foo'] = collection.Assignment(header=u"title", target_collection='/Members/test_user_1_/collection')
        collectionrenderer = self.renderer(context=None, request=None, view=None, manager=None, assignment=mapping['foo'])

        # we want the portlet to return us the same results as the collection
        self.assertEquals(collection_num_items, len(collectionrenderer.results()))

    def testRandomQuery(self):
        # set up our portlet renderer
        mapping = PortletAssignmentMapping()
        mapping['foo'] = collection.Assignment(header=u"title", random=True,
            target_collection='/Members/test_user_1_/collection')
        # add some folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s'%i)
            getattr(self.folder, 'folder_%s'%i).reindexObject()

        # collection with no criteria -- should return empty list
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        self.assertEqual(len(collectionrenderer.results()), 0)

        # collection with simple criterion -- should return 1 (random) folder
        crit = self.folder.collection.addCriterion('portal_type',
            'ATSimpleStringCriterion')
        crit.setValue('Folder')
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        self.assertEqual(len(collectionrenderer.results()), 1)

        # collection with multiple criteria -- should behave similarly
        crit = self.folder.collection.addCriterion('Creator',
            'ATSimpleStringCriterion')
        crit.setValue('test_user_1_')
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        collectionrenderer.results()

        # collection with sorting -- should behave similarly (sort is ignored
        # internally)
        self.folder.collection.setSortCriterion('modified', False)
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        self.assertEqual(len(collectionrenderer.results()), 1)

        # same criteria, now with limit set to 2 -- should return 2 (random)
        # folders
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        collectionrenderer.data.limit = 2
        self.assertEqual(len(collectionrenderer.results()), 2)

        # make sure there's no error if the limit is greater than the # of
        # results found
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        collectionrenderer.data.limit = 10
        self.failUnless(len(collectionrenderer.results()) >= 6)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    suite.addTest(makeSuite(TestCollectionQuery))
    return suite
