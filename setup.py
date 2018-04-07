#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(
    name='brave',
    version='1.0.1',
    description='Python Brave New Coin Client',
    author='Paula Grangeiro',
    author_email='contato@paulagrangeiro.com.br',
    url='https://github.com/pgrangeiro/python-bravenewcoin-client',
    license='GPL 3',
    python_requires='>=3.6',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests>=2.18', 'pytz>=2018.3'],
)
