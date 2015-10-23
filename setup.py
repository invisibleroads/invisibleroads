from os.path import abspath, dirname, join
from setuptools import setup


ENTRY_POINTS = """
"""
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads',
    version='0.1.1',
    description='Simple framework for extensible command line scripts',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='http://invisibleroads.com',
    keywords='web pyramid pylons invisibleroads',
    package_dir={'': 'lib'},
    packages=['invisibleroads'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'invisibleroads-macros',
        'six',
        'stevedore'
    ],
    tests_require=[],
    entry_points=ENTRY_POINTS,
    scripts=['bin/invisibleroads'])
