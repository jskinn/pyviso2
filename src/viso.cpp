/*
Copyright 2011. All rights reserved.
Institute of Measurement and Control Systems
Karlsruhe Institute of Technology, Germany

This file is part of libviso2.
Authors: Andreas Geiger

libviso2 is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or any later version.

libviso2 is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
libviso2; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA 
*/

#include "viso.h"

#include <math.h>

using namespace std;

VisualOdometry::VisualOdometry (parameters param) : random_generator(std::random_device{} ()), param(param) {
  J         = 0;
  p_observe = 0;
  p_predict = 0;
  matcher   = new Matcher(param.match);
  Tr_delta  = Matrix::eye(4);
  Tr_valid  = false;
}

VisualOdometry::~VisualOdometry () {
  delete matcher;
}

void VisualOdometry::seed(int32_t val) {
  random_generator.seed(val);
}

bool VisualOdometry::updateMotion () {
  
  // estimate motion
  vector<double> tr_delta = estimateMotion(p_matched);
  
  // on failure
  if (tr_delta.size()!=6)
    return false;
  
  // set transformation matrix (previous to current frame)
  Tr_delta = transformationVectorToMatrix(tr_delta);
  Tr_valid = true;
  
  // success
  return true;
}

Matrix VisualOdometry::transformationVectorToMatrix (vector<double> tr) {

  // extract parameters
  double rx = tr[0];
  double ry = tr[1];
  double rz = tr[2];
  double tx = tr[3];
  double ty = tr[4];
  double tz = tr[5];

  // precompute sine/cosine
  double sx = sin(rx);
  double cx = cos(rx);
  double sy = sin(ry);
  double cy = cos(ry);
  double sz = sin(rz);
  double cz = cos(rz);

  // compute transformation
  Matrix Tr(4,4);
  Tr.val[0][0] = +cy*cz;          Tr.val[0][1] = -cy*sz;          Tr.val[0][2] = +sy;    Tr.val[0][3] = tx;
  Tr.val[1][0] = +sx*sy*cz+cx*sz; Tr.val[1][1] = -sx*sy*sz+cx*cz; Tr.val[1][2] = -sx*cy; Tr.val[1][3] = ty;
  Tr.val[2][0] = -cx*sy*cz+sx*sz; Tr.val[2][1] = +cx*sy*sz+sx*cz; Tr.val[2][2] = +cx*cy; Tr.val[2][3] = tz;
  Tr.val[3][0] = 0;               Tr.val[3][1] = 0;               Tr.val[3][2] = 0;      Tr.val[3][3] = 1;
  return Tr;
}

vector<int32_t> VisualOdometry::getRandomSample(int32_t N,int32_t num) {
  if (num > N) { // Cannot draw more than N samples
    num = N;
  }
  vector<int32_t> sample;

  if (N > 0 && num > 0) {
    if (num < N / 2) {
      // There are many fewer samples than the total number, shuffling the whole set is inefficient. Instead, draw until uniqueness
      sample.reserve(num);
      std::uniform_int_distribution<int32_t> dist(0, N - 1);
      while (sample.size() < (unsigned) num) {
        int32_t i = dist(random_generator);
        if (std::find(sample.begin(), sample.end(), i) == sample.end()) {
          sample.push_back(i);
        }
      }
    } else {
      // We require lots of samples, shuffle all the indexes
      sample.reserve(N);

      // create vector containing all indices, and shuffle it
      for (int32_t i=0; i<N; i++)
        sample.push_back(i);
      std::shuffle(sample.begin(), sample.end(), random_generator);

      // Remove all but the desired number of samples
      sample.resize(num);
    }
  }
  
  // return sample
  return sample;
}
