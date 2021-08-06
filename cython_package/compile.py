from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("cy_pakcage1",  ["cy_package1/__init__.py"]),
    # Extension("mymodule2",  ["mymodule2.py"]),#   ... all your modules that need be compiled ...
]
setup(
    name = 'My Cython Package',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)