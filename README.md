# Overview

`pyviso2` is a thin SWIG Python wrapping of the visual odometry library, [libviso2](http://www.cvlibs.net/software/libviso/).
Uses the latest version of libviso2 (updated 2017-06-12 according to their changelog), with the following changes:
- change matcher.cpp to use `std::shuffle` rather than `std::random_shuffle` (which is deprecated)
- Add an extra check to `Matcher::removeOutliers` to be really sure there are at least 3 points before delaunay triangulation. This prevents a segfault in triangle.cpp.

# Status

Currently, the stereo demo included with libviso2 has been replicated in Python. The nested parameter classes used to configure the VisualOdometry* classes have been flattened and renamed in order to work with Python (see [SWIG nested classes](http://www.swig.org/Doc3.0/SWIGPlus.html#SWIGPlus_nested_classes)). In addition, a few overloaded methods have been renamed in order to work properly:

- `Matrix::eye()` member function has been renamed to `Matrix::identity()` to allow the static member function `Matrix_eye(size)` to be created.
- `Matrix::inv()` member function has been renamed to `Matrix::setInverse()` to allow the static member function `Matrix_inv(Matrix)` to be created.
- A `VisualOdometryStereo::process_frame(img1,img2)` has been added to support [NumPy](http://www.numpy.org) grayscale images.

# Getting Started

Clone the repository: `git clone http://github.com/jskinn/pyviso2.git`
Build the extension in place: `python setup.py build_ext -i`
Build a source distribution:

- `python setup.py sdist`
- You can then install this distribution with `pip install <place you cloned>/pyviso2/dist/pyviso2-0.1.0.tar.gz`

Run the demo (either after building in-place, or installing the distribution): `python demo.py <path to synchronized/rectified image directory>`

# Requirements

`pyviso2` requires SWIG 3.0. CMake and libpng are required if you want to build the C++ demo from the original source. 

# License

`libviso2` is licensed under the GPL, therefore this software is under the GPL as well. Please see the [original readme](https://github.com/jlowenz/pyviso2/blob/master/readme.txt) for more information.
