#!/usr/bin/env python2

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [ 
    Extension("app",  ["app.pyx"]),
]
setup(
    name = 'Colornos Menu',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

*****************************************************************************************
from app import app

app.run(host='127.0.0.1', port=80)

*******************************************************************************************
LINK:
https://stackoverflow.com/questions/50932527/how-do-you-compile-a-flask-app-with-cython
