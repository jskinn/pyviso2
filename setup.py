from setuptools import setup, Extension
import numpy


setup(
    name="pyviso2",
    version="0.1.0",
    py_modules=["viso2"],
    url='https://github.com/jskinn/pyviso2',
    maintainer='John Skinner',
    maintainer_email='jskinn7@gmail.com',
    zip_safe=False,
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
