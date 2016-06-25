#!/usr/bin/env python
import os
from setuptools import find_packages, setup
import warnings


def parse_requirements(filename):
    """ Parse a requirements file ignoring comments and -r inclusions of other files """
    reqs = []
    with open(filename, 'r') as f:
        for line in f:
            hash_idx = line.find('#')
            if hash_idx >= 0:
                line = line[:hash_idx]
            line = line.strip()
            if line:
                reqs.append(line)
    return reqs


with open(os.path.join('codewords', 'VERSION'), 'r') as f:
    version = f.read().strip()


with open('README.md', 'r') as f:
    readme = f.read().strip()


def recursive_ls(directory):
    full_path = os.path.join('codewords', directory)
    output = []
    for root, _, files in os.walk(full_path):
        if not files:
            continue
        relpath = os.path.relpath(root, 'codewords')
        output.extend([os.path.join(relpath, filename) for filename in files])
    return output


setup(
    name="codewords",
    version=version,
    url="https://github.com/khwilson/codewords",
    author="Kevin Wilson",
    author_email="khwilson@gmail.com",
    license="Proprietary",
    packages=find_packages(),
    package_data={'codewords': ['VERSION']
                               + recursive_ls('static')
                               + recursive_ls('templates')},
    install_requires=parse_requirements('requirements.in'),
    tests_require=parse_requirements('requirements.testing.in'),
    description="A simple implementation of the game Codewords",
    entry_points="""
    [console_scripts]
    crun=codewords.cli:cli
    """,
    long_description="\n" + readme
)
