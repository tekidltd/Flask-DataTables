# -*- coding: utf-8 -*-
# pylint: disable=all
# type: ignore

from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

__version__ = '0.1.0'

# setup attributes
attrs = dict(
    name='Flask-DataTables-peewee',
    version=__version__,
    description='Flask integration with DataTables and peewee.',
    long_description=long_description,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    maintainer='Jarry Shaw',
    maintainer_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/Flask-DataTables',
    download_url='https://github.com/JarryShaw/Flask-DataTables/archive/v%s.tar.gz' % __version__,
    # py_modules
    packages=[
        'flask_datatables',
    ],
    # scripts
    # ext_modules
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    # distclass
    # script_name
    # script_args
    # options
    license='BSD 3-Clause License',
    keywords=[
        'flask',
        'peewee',
        'datatables',
    ],
    platforms=[
        'any',
    ],
    # cmdclass
    # data_files
    # package_dir
    # obsoletes
    # provides
    # requires
    # command_packages
    # command_options
    package_data={
        '': [
            'LICENSE',
            'README.md',
        ],
        'flask_datatables': [
            'py.typed',
        ],
    },
    # include_package_data
    # libraries
    # headers
    # ext_package
    # include_dirs
    # password
    # fullname
    # long_description_content_type
    # python_requires
    # zip_safe,
    install_requires=[
        'Flask',
        'peewee',

        'typing; python_version<"3.5"',
        'typing_extensions',
    ],
    #entry_points
    #extras_require
    #setup_requires
)

try:
    from setuptools import setup
    from setuptools.command.build_py import build_py

    attrs.update(dict(
        include_package_data=True,
        # libraries
        # headers
        # ext_package
        # include_dirs
        # password
        # fullname
        long_description_content_type='text/x-rst',
        python_requires='>=3.6',
        # zip_safe=True,
    ))
except ImportError:
    from distutils.core import setup
    from distutils.command.build_py import build_py


# set-up script for pip distribution
setup(**attrs)
