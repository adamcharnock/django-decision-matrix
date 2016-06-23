#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

setup(
    name='django-decision-matrix',
    version=open('VERSION').read().strip(),
    # Your name & email here
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    # If you had ddm.tests, you would also include that in this list
    packages=find_packages(),
    scripts=[],
    url='https://github.com/adamcharnock/django-decision-matrix',
    license='MIT',
    description='Django app for using weighted attribute matrices for making complex decisions',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    install_requires=[
        'path.py',
        'django>=1.10b1',
        'django-extensions',
        'django-smalluuid>=0.1.2',
        'django-bootstrap3>=7.0.1',
        'dj_database_url',
        'gunicorn',
        'psycopg2',
    ],
)
