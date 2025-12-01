from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Define the extension module
extensions = [
    Extension(
        "neuronet",
        sources=["src/cython/neuronet.pyx", "src/cpp/GrafoDisperso.cpp"],
        include_dirs=["src/cpp"],
        language="c++",
        extra_compile_args=["-std=c++11"],
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions),
)
