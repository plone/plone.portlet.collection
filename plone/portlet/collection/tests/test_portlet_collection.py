from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, getMultiAdapter

from plone.portlet.collection import collection
from plone.portlet.collection.testing import (
    PLONE_PORTLET_COLLECTION_INTEGRATION_TESTING
)

import unittest2 as unittest


class TestPortlet(unittest.TestCase):

    layer = PLONE_PORTLET_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal.folder

    def testPortletTypeRegistered(self):
        portlet = getUtility(
            IPortletType, name='plone.portlet.collection.Collection')
        self.assertEqual(
            portlet.addview, 'plone.portlet.collection.Collection')

    def testInterfaces(self):
        portlet = collection.Assignment(header=u"title")
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(
            IPortletType, name='plone.portlet.collection.Collection')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={'header': u"test title"})
        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], collection.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = collection.Assignment(header=u"title")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, collection.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = collection.Assignment(header=u"title")

        renderer = getMultiAdapter((
            context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, collection.Renderer))


class TestRenderer(unittest.TestCase):

    layer = PLONE_PORTLET_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal.folder

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or collection.Assignment(header=u"title")

        return getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer
        )

    def test_render(self):
        r = self.renderer(
            context=self.portal,
            assignment=collection.Assignment(header=u"title")
        )
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.assertTrue('title' in output)

    def test_collection_path_unicode(self):
        self.portal.invokeFactory('Collection', 'events')
        # Cover problem in #9184
        renderer = self.renderer(
            context=self.portal,
            assignment=collection.Assignment(
                header=u"title",
                target_collection=u"/events"
            )
        )
        renderer = renderer.__of__(self.folder)
        self.assertEqual(renderer.collection().id, 'events')

    def test_css_class(self):
        r = self.renderer(
            context=self.portal,
            assignment=collection.Assignment(header=u"Welcome text")
        )
        self.assertEqual('portlet-collection-welcome-text', r.css_class())


class TestCollectionQuery(unittest.TestCase):

    layer = PLONE_PORTLET_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal.folder
        self.collection = self._createType(
            self.folder, 'Collection', 'collection')

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

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment
        return getMultiAdapter((
            context, request, view, manager, assignment),
            IPortletRenderer
        )

    def testPortletAvailabilityWithPrivateFolders(self):
        private_folder = self._createType(self.folder, 'Folder', 'private')
        public_subfolder = self._createType(private_folder, 'Folder', 'public')
        self.portal.portal_workflow.doActionFor(public_subfolder, 'publish')
        self.collection = self._createType(
            public_subfolder, 'Collection', 'collection')
        self.portal.portal_workflow.doActionFor(self.collection, 'publish')

        mapping = PortletAssignmentMapping()
        mapping['foo'] = collection.Assignment(
            header=u"title",
            target_collection='/folder/private/public/collection'
        )
        logout()
        collectionrenderer = self.renderer(
            context=None, request=None, view=None, manager=None,
            assignment=mapping['foo']
        )

        self.assertEqual(self.collection, collectionrenderer.collection())

    def testSimpleQuery(self):
        # set up our collection to search for Folders
        self.folder.collection.query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Folder',
        }]

        # add a few folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s' % i)
            getattr(self.folder, 'folder_%s' % i).reindexObject()

        # the folders are returned by the topic
        collection_num_items = len(self.folder.collection.results())
        # We better have some folders
        self.assertTrue(collection_num_items >= 6)

        mapping = PortletAssignmentMapping()
        mapping['foo'] = collection.Assignment(
            header=u"title",
            target_collection='/folder/collection'
        )
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        # we want the portlet to return us the same results as the collection
        self.assertEqual(collection_num_items, len(
            collectionrenderer.results()))

    def testRandomQuery(self):
        # set up our portlet renderer
        mapping = PortletAssignmentMapping()
        mapping['foo'] = collection.Assignment(
            header=u"title",
            random=True,
            target_collection='/folder/collection'
        )
        # add some folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s' % i)
            getattr(self.folder, 'folder_%s' % i).reindexObject()

        # collection with no criteria -- should return empty list
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        self.assertEqual(len(collectionrenderer.results()), 0)

        # collection with simple criterion -- should return 1 (random) folder
        self.folder.collection.query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Folder',
        }]
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        self.assertEqual(len(collectionrenderer.results()), 1)

        # collection with multiple criteria -- should behave similarly
        self.folder.collection.query = [
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.string.is',
                'v': 'Folder',
            },
            {
                'i': 'creator',
                'o': 'plone.app.querystring.operation.string.is',
                'v': 'test_user_1_',
            },
        ]
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        collectionrenderer.results()

        # collection with sorting -- should behave similarly (sort is ignored
        # internally)
        self.folder.collection.sort_on = 'modified'
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        self.assertEqual(len(collectionrenderer.results()), 1)

        # same criteria, now with limit set to 2 -- should return 2 (random)
        # folders
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        collectionrenderer.data.limit = 2
        self.assertEqual(len(collectionrenderer.results()), 2)

        # make sure there's no error if the limit is greater than the # of
        # results found
        collectionrenderer = self.renderer(
            context=None,
            request=None,
            view=None,
            manager=None,
            assignment=mapping['foo']
        )
        collectionrenderer.data.limit = 10
        self.assertTrue(len(collectionrenderer.results()) >= 6)
