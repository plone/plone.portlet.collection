from zope.i18nmessageid import MessageFactory
CollectionMessageFactory = MessageFactory('plone.portlet.collection')

def initialize(context):
    """Intializer called when used as a Zope 2 product."""