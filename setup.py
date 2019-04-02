# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages


def get_version(*file_paths):
    """Retrieves the version from prompt_responses/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("reobj", "__init__.py")
readme = open('README.md').read()

setup(
    name='reobj',
    version=version,
    description="""Reusable object for easy dump and load""",
    long_description=readme,
    author='Dongkwan Kim',
    author_email='todoaskit@gmail.com',
    url='https://github.com/dongkwan-kim/re-obj',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "termcolor",
    ],
    license="MIT",
    zip_safe=False,
    keywords='Reusable Object',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
