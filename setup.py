#!/usr/bin/env python

import setuptools

import ensysmod

with open('requirements.txt') as file:
    packages = filter(lambda x: x != "" and x[0] != "#", file.readlines())

with open('README.md') as file:
    description = file.read()

setuptools.setup(
    name='ensysmod',
    version=ensysmod.__version__,
    author='NOWUM-Energy - FH Aachen',
    # author_email='',
    description='Just another energy system modeling tool made by Institut NOWUM-Energy - FH Aachen',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/NOWUM/EnSysMod',
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=packages,
    setup_requires=['setuptools']
)
