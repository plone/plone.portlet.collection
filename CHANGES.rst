Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

4.0.0a4 (2022-05-24)
--------------------

Bug fixes:


- Update ``ICollectionPortlet`` schema.
  Set option ``required`` to ``False`` of boolean fields.
  [1letter] (#32)


4.0.0a3 (2022-04-08)
--------------------

Breaking changes:


- Update for Plone 6 with Bootstrap markup
  [petschki, agitator] (#28)


Bug fixes:


- Use @@iconresolver to display icons
  [pbauer] (#31)


4.0.0a2 (2021-04-19)
--------------------

Breaking changes:


- Update for Plone 6 with Bootstrap markup
  [petschki, agitator] (#28)


Bug fixes:


- Show start date in portlet if available.
  [agitator] (#25)


4.0.0a1 (2021-04-19)
--------------------

Breaking changes:


- Update for Plone 6 with Bootstrap markup
  [petschki, agitator] (#28)


Bug fixes:


- Show start date in portlet if available.
  [agitator] (#25)


3.3.5 (2020-09-21)
------------------

Bug fixes:


- Removed fallback import of is_default_page.
  Fixed various DeprecationWarnings.
  [maurits] (#3130)


3.3.4 (2020-09-07)
------------------

Bug fixes:


- Fixed deprecation warning for ``setDefaultRoles``.
  [maurits] (#3130)


3.3.3 (2020-04-21)
------------------

Bug fixes:


- Minor packaging updates. (#1)


3.3.2 (2019-08-23)
------------------

Bug fixes:

- Fix deprecated import ``isDefaultPage``.
  [jensens]


3.3.1 (2018-11-02)
------------------

Bug fixes:

- Fix tests in Python 3
  [davisagli]


3.3.0 (2017-11-24)
------------------

Bug fixes:

- Fix collection selection for Plone 5.1
  [agitator]

- Fix test. Portlet renderer no longer mixes in Acquisition.Explicit.
  [pbauer]


3.2 (2017-07-03)
----------------

New features:

- add options to supress icons,
  read thumb_scale from registry plus  option to override thumb_scale individually
  or suppress thumbs.
  Replace paper clip (fontello icon) with mimetype icon
  from mimetype registry for files
  https://github.com/plone/Products.CMFPlone/issues/1734
  applied https://github.com/plone/Products.CMFPlone/issues/1483
  [fgrcon]

Bug fixes:


- fixed css-classes for thumb scales ...
  https://github.com/plone/Products.CMFPlone/issues/2077
  [fgrcon]

- Remove unittest2 dependency
  [kakshay21]


3.1 (2016-08-15)
----------------

New:

- If collection is default page in parent, link to parent.
  [malthe]

Fixes:

- Use zope.interface decorator.
  [gforcada]


3.0.6 (2016-01-08)
------------------

Fixes:

- Fixed sometimes failing test due to sorting.
  [maurits]


3.0.5 (2015-11-26)
------------------

Fixes:

- Used registry lookup for types_use_view_action_in_listings.
  [esteele]

- Cleanup and rework: contenttype-icons and showing thumbnails
  for images/leadimages in listings
  https://github.com/plone/Products.CMFPlone/issues/1226
  [fgrcon]


3.0.4 (2015-09-07)
------------------

- Fix show_dates by calling obj.Date(). This fixes https://github.com/plone/plone.app.contenttypes/issues/263
  [timo]


3.0.3 (2015-06-05)
------------------

- Fix test to be more forgiving on matches html
  [vangheem]

- This package does not depend on plone.app.form
  [tomgross]

- Fix last part of the test: regexp -> lxml
  [khink]

- Fix tests. Kids, don't parse HTML with regexps.
  [khink]

- Remove DL's from portlet templates.
  [khink]


3.0.2 (2015-03-13)
------------------

- ReST fix.
  [timo]


3.0.1 (2015-03-13)
------------------

- fix AttributeError: exclude_context on existing portlet assignments, refs #5
  [davisagli]

- Add an option for excluding the render context from the collection results
  since in most cases it's undesirable to include the current context in a
  listing on that context's view.
  [rpatterson]


3.0 (2014-04-05)
----------------

- Use z3c.form for portlet forms.
  [bosim, davisagli]

- Provide a hook to facilitate overrides that do not include an empty
  footer when the more link is turned off.
  [anthonygerrard]


2.2.1 (2014-02-22)
------------------

- Include rst files in releases.
  [timo]


2.2.0 (2014-02-22)
------------------

- Remove DL's from portlet templates.
  https://github.com/plone/Products.CMFPlone/issues/163
  [khink]

- plone.portlet.collection should also install plone.app.querystring:default
  profile
  [garbas]

- Replace deprecated test assert statements.
  [timo]

- Use PLONE_APP_CONTENTTYPES_FIXTURE as test layer for Plone 5 compatibility.
  [timo]


2.1.5 (2013-04-29)
------------------

- PEP8 cleanup.
  [timo]

- Migrate all tests to use the new Collection type instead of the old Topic
  type.
  [timo]

- Migrate all tests to plone.app.testing.
  [timo]

- Fix Archetypes brain rendering.
  This fixes http://dev.plone.org/ticket/13518.
  [timo]


2.1.4 (2013-03-19)
------------------

- Support for Dexterity-based collections added. Use 'title_or_id' instead of
  the AT-specific 'pretty_title_or_id'.
  [timo]

- Remove deprecated getIcon() method from collection portlet view.
  [timo]


2.1.3 (2013-01-01)
------------------

- Fix for #12274 - missing icons for some contenttypes.
  [spereverde]


2.1.2 (2012-10-03)
------------------

- Fix 'This portlet display a'.
  [danjacka]


2.1.1 (2012-06-29)
------------------

- accessibility improvements for screen readers regarding "more" links, see
  https://dev.plone.org/ticket/11982
  [rmattb, applied by polyester]


2.1 (2012-04-15)
----------------

- Support new-style collections a la plone.app.collection.
  [davisagli]


2.0.4 (2011-08-29)
------------------

- Portlet is shown when user has View permission for the collection.
  Fixes http://dev.plone.org/plone/ticket/12152
  [gotcha]

- Fix failing test.
  [davisagli]

2.0.3 - 2011-07-04
------------------

- Change the `target_collection` query to use a `portal_type` instead of an
  `object_provides` restriction. The data for the former is much more likely
  in the ZODB cache as many catalog queries use it.
  [hannosch]

- Fix 'Show more...' handling so it doesn't cause portletFooter to disappear.
  Fixes http://dev.plone.org/plone/ticket/9415.
  [msmith64]

2.0.2 - 2011-05-18
------------------

- Fix memoization of results when randomizing. We only memoize on the instance,
  in this case the rendered object, which is created per request and per
  portlet.
  [hannosch]

- Pass on `limit` setting from the portlet to the `queryCatalog` call, to take
  advantage of optimizations inside the catalog.
  [hannosch]

- Add MANIFEST.in.
  [WouterVH]

- Add metadata.xml to profile.
  [WouterVH]

- Added a dynamic dl class, generated from portlet's title. Code taken from
  plone.portlet.static.
  [zupo]


2.0.1 - 2011-01-03
------------------

- Add Site Administrator to the default roles for the
  "plone.portlet.collection: Add collection portlet" permission, for forward
  compatibility with Plone 4.1.
  [davisagli]

- Removed bug where a resultset with fewer items than limit wasn't randomized.
  [jaroel]

- Removed Plone 3 specific implementation in favor of a generic one.
  [jaroel]

- Fixed returning optional randomized results in the collection
  portlet.  This happened on Plone 4; if this makes the portlet too
  slow for you, you should switch off the randomizing.
  [maurits]

- Fixed wrong exception handling in random collection portlet that
  failed to catch an IndexError.
  [maurits]


2.0 - 2010-07-18
----------------

- Update license to GPL version 2 only.
  [hannosch]

- Add fix for http://dev.plone.org/plone/ticket/9198 so that
  typeUseViewActionInListings is respected.
  [aaronv]

- Removed msgids in portlets.xml. There is no support for
  msgids in the import of portlets.xml implementation.
  This allows to extract translatable strings with i18ndude.
  [vincentfretin]

- Add fix for http://dev.plone.org/plone/ticket/9184 so that
  restrictedTraverse always gets a string and not Unicode.
  [amleczko]


1.1.3 - 2008-07-07
------------------

- Added 'Select random items' option.
  [davisagli]


1.1.2 - 2008-06-01
------------------

- Use a custom edit permission for the portlet.
  [hannosch]


1.1.0 - 2008-04-20
------------------

- Added missing i18n markup to portlets.xml.
  [hannosch]

- Changed the i18n domain to `plone`.
  [hannosch]


1.0b1 - 2008-03-08
------------------

- Fix a typo in the CSS classes.
  [davisagli]

- Set default_query to get something to browse in the UberSelectionWidget from
  the start.
  [fschulze]

- Code cleanup and make showing of dates for items and a 'Show more...' link
  configurable.
  [optilude]


0.1.1 - 2007-11-19
------------------

- Set zip-safe flag for the egg to False so zcml can be correctly loaded.
  [wichert]

- Remove non-ASCII characters form the description since PyPI can not handle
  them.
  [wichert]


0.1 - 2007-11-19
----------------

- First public release
  [baekholt, wichert]
