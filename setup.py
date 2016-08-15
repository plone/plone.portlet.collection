from setuptools import setup, find_packages

version = '3.1'

setup(name='plone.portlet.collection',
      version=version,
      description="A portlet that fetches results from a collection",
      long_description=open("README.rst").read() + "\n" +
      open("CHANGES.rst").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='collection portlet',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://pypi.python.org/pypi/plone.portlet.collection',
      license='GPL version 2',
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
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.app.contenttypes',
          ],
      }
      )
