#!/usr/bin/env python

import setuptools
import counter

with open('requirements.txt') as file:
    packages = filter(lambda x: x != "" and x[0] != "#", file.readlines())

with open('README.md') as file:
    description = file.read()

setuptools.setup(
    name='Counter',
    version=counter.__version__,
    author='V3lop5',
    author_email='v3lop5@gmail.com',
    description='Python Starter Project',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/v3lop5',
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=packages,
    setup_requires=['setuptools']
)
