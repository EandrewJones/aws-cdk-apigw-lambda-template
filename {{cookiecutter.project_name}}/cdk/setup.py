#!/usr/bin/env python
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

setup(
    name="service-cdk",
    version="3.1",
    description={{cookiecutter.project_short_description}},
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: {{cookiecutter.python_major_version}}.{{cookiecutter.python_minor_version}}",
    ],
    url={{cookiecutter.git_rep_url}},
    author={{cookiecutter.full_name}},
    author_email={{cookiecutter.email}},
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    package_data={"": ["*.json"]},
    include_package_data=True,
    python_requires=">={{cookiecutter.python_major_version}}.{{cookiecutter.python_minor_version}}",
    install_requires=[],
)
