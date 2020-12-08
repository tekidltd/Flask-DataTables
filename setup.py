# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

__version__ = '0.0.0.dev0'

setup(
    name='Flask-DataTables-peewee',
    version=__version__,
    description='Flask integration with DataTables and peewee.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/JarryShaw/Flask-DataTables',
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    license='BSD License',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    keywords='bpc backport utilities',
    packages=['flask_datatables'],
    package_data={'flask_datatables': ['py.typed']},
    python_requires='>=3.6',
    install_requires=[
        'Flask',
        'peewee',
        'typing;python_version<"3.5"',
        'typing_extensions',
    ],
)
