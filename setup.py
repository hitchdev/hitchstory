# -*- coding: utf-8 -*
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
import subprocess
import codecs
import sys
import os


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), "r"
    ).read()


setup(
    name="hitchstory",
    version=read("VERSION").replace("\n", ""),
    description="Type-safe, YAML-based BDD, TDD & specification by example framework for python.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Operating System :: Unix",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="hitchdev framework bdd tdd declarative tests testing yaml",
    author="Colm O'Connor",
    author_email="colm.oconnor.github@gmail.com",
    url="https://hitchdev.com/hitchstory/",
    license="MIT",
    install_requires=[
        "strictyaml>=0.15.3",
        "path.py",
        "jinja2",
        "colorama",
        "pathquery>=0.2.0",
        "python-slugify>=1.2.1",
        "prettystack>=0.3.0",
        "jinja2",
    ],
    packages=find_packages(
        exclude=[
            "docs",
        ]
    ),
    package_data={},
    zip_safe=False,
    include_package_data=True,
)
