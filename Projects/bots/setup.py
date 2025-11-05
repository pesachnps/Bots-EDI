#!/usr/bin/env python
"""
Setup script for Bots EDI Environment
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='bots-edi-environment',
    version='1.0.0',
    description='Bots EDI Environment with REST API',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/bots-edi-environment',
    license='MIT',
    
    packages=find_packages(where='env/default'),
    package_dir={'': 'env/default'},
    
    install_requires=[
        'bots>=4.0.0',
        'Django>=3.2,<5.0',
        'cherrypy>=18.6.0',
        'python-dateutil>=2.8.0',
        'pytz>=2021.1',
    ],
    
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-django>=4.5.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
        'postgresql': [
            'psycopg2-binary>=2.9.0',
        ],
        'mysql': [
            'mysqlclient>=2.1.0',
        ],
        'excel': [
            'openpyxl>=3.0.0',
            'xlrd>=2.0.0',
        ],
        'sftp': [
            'paramiko>=2.7.0',
        ],
        'xml': [
            'lxml>=4.6.0',
        ],
    },
    
    python_requires='>=3.8',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Django',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
    keywords='edi edifact x12 tradacoms xml json csv bots translation',
    
    entry_points={
        'console_scripts': [
            'bots-manage-users=manage_users:main',
            'bots-api-management=usersys.api_management:main',
        ],
    },
    
    include_package_data=True,
    zip_safe=False,
)
