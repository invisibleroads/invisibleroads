from setuptools import find_packages, setup


ENTRY_POINTS = '''
[console_scripts]
xyz = xyz.scripts:launch
[xyz]
a = xyz.scripts.a:AScript
b = xyz.scripts.b:BScript
x.a = xyz.scripts.x.a:XAScript
x.b = xyz.scripts.x.b:XBScript
y.a = xyz.scripts.y.a:YAScript
y.b = xyz.scripts.y.a:YAScript
'''
APPLICATION_REQUIREMENTS = [
    'invisibleroads',
]


setup(
    name='xyz',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=APPLICATION_REQUIREMENTS,
    entry_points=ENTRY_POINTS)
