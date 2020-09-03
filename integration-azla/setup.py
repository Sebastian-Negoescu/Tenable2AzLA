from setuptools import setup, find_packages
import os

long_description = '''
Tenable Assets & Vulnerabilities -> Azure Log Analytics
For usage documentation, please refer to the following pages:
Azure Log Analytics (HTTP Data Collector) -->
'''

setup(
    name='tenable_azla',
    version='1.0.0',
    description='',
    author='Sebastian Negoescu',
    long_description=long_description,
    author_email='sebastian.negoescu@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    keywords='microsoft azure loganalytics tenable assets vulnerabilities',
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        Tenable2AzLA=tenable_azla.main:cli
    ''',
)