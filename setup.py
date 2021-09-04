from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Py-arn',
    version='0.1.0',
    long_description=readme,
    author='Quentin Cousin',
    license=license,
)