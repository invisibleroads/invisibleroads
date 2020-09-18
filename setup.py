from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = '''
[console_scripts]
invisibleroads = invisibleroads.scripts:launch
'''
APPLICATION_CLASSIFIERS = [
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
]
APPLICATION_REQUIREMENTS = [
    'stevedore',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.md',
    'CHANGES.md',
])


setup(
    name='invisibleroads',
    version='0.3.3',
    description='Simple framework for extensible command line scripts',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=APPLICATION_CLASSIFIERS,
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='https://github.com/invisibleroads/invisibleroads',
    keywords='invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=APPLICATION_REQUIREMENTS,
    entry_points=ENTRY_POINTS)
