from setuptools import setup, find_packages

version = '1.1.0b1'

setup(name='plone.portlet.collection',
      version=version,
      description="A portlet that fetches results from a collection",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Geir Baekholt - Jarn',
      author_email='baekholt@jarn.com',
      url='http://svn.plone.org/svn/plone/plone.portlet.collection',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', "plone.portlet"],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.memoize',
          'plone.portlets',
          'plone.app.portlets',
          'plone.app.vocabularies',
          'plone.app.form',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
