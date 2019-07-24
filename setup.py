from distutils.core import setup, Extension
from distutils.sysconfig import get_config_vars
import numpy
import os

(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
)

setup(
    name="pyviso2",
    version="0.1.0",
    py_modules=["viso2"],
    ext_modules=[
        Extension(
	    "_viso2",
            sources=[
                "src/filter.cpp",
                "src/matcher.cpp",
		        "src/matrix.cpp",
		        "src/reconstruction.cpp",
                "src/triangle.cpp",
                "src/viso.cpp",
                "src/viso_stereo.cpp",
                "src/viso_mono.cpp",
                "viso2.i"
            ],
            language="c++",
            swig_opts=['-c++','-threads'],
            extra_compile_args=['-msse3', '-std=c++11'],
            include_dirs=[numpy.get_include()]
        )
    ]
)
