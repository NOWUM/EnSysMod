#!/usr/bin/env python

import setuptools
import %SAFE_NAME%

with open('requirements.txt') as file:
    packages = filter(lambda x: x != "" and x[0] != "#", file.readlines())

with open('README.md') as file:
    description = file.read()

setuptools.setup(
    name='%SAFE_NAME%',
    version=%SAFE_NAME%.__version__,
    author='%ACTOR%',
    # author_email='',
    description='Default description for %NAME%.',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/%REPOSITORY%',
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=packages,
    setup_requires=['setuptools']
)
