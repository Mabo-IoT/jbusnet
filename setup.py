# coding: utf-8

from setuptools import setup, find_packages
import sys

if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
    setup(
        name='jbusnet',
        version='0.1.1',
        author='HeathKang',
        author_email='heath.kang@foxmail.com',
        description='A lib to parse Jbusnet protocol',
        packages=find_packages(exclude=[]),
        include_package_data=True,
        license='MIT',
    )

