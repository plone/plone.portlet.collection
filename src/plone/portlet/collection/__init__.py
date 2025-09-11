from AccessControl.Permission import addPermission
from zope.i18nmessageid import MessageFactory


PloneMessageFactory = MessageFactory("plone")
PROJECTNAME = "plone.portlet.collection"
DEFAULT_ADD_CONTENT_PERMISSION = "%s: Add collection portlet" % PROJECTNAME

addPermission(
    DEFAULT_ADD_CONTENT_PERMISSION,
    (
        "Manager",
        "Site Administrator",
        "Owner",
    ),
)
