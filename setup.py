#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


with open("README.md") as readme:
    long_description = readme.read()

print('AHA')
print(setuptools.find_packages())
setuptools.setup(
    name="DNNSed",
    version="0.9",
    author="Theo Glauch",
    author_email="theo.glauch@tum.de",
    description="Deep-learning tool to calculate Blazar nu-peaks",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/tglauch/DNNSed/",
    project_urls={
        "Source": "https://github.com/tglauch/DNNSed/",
        "Tracker": "https://github.com/tglauch/DNNSed/issues/"
        },
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
        ],
    python_requires=">=2.7",
    install_requires=[
        'tensorflow>=1.5,<2.0',
        'numpy>1.14',
        'scipy>1.2.0',
        'keras>2.0.0'],
    packages = setuptools.find_packages(),
    package_data={"DNNSed": ["models/*.h5",
                             "examples/*"]},
    )
