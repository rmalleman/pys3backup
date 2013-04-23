#!/usr/bin/env python


import glob

from distutils.core import setup


setup(
    name='pys3backup',
    description='A package used to backup data to Amazon s3',
    version='0.0.1',
    author="Matt Alleman",
    author_email="rmalleman@gmail.com",
    license = "MIT",
    install_requires=['boto'],
    packages=[
        'pys3backup'
    ],

    package_dir={
        'pys3backup': 'src'
    },

    scripts=glob.glob('scripts/*'),
)
