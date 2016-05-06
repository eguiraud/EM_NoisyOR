#!/usr/bin/env python
# generate data-points from a Noisy-OR mixture
# author: blue, 29/03/2016

# This script generates ndps data-points of dimension dimdp with a noisy-OR
# generative model. The priors are taken all equal to 2/nHiddenVars and the
# weight matrices are single horizontal and vertical bars. The data-points will
# therefore consist of a superposition of an average of 2 bars, with noise.

import numpy as np
from scipy.stats import bernoulli
from math import sqrt
import argparse

# Defiine parser
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--nHiddenVars', default=10, dest='nHiddenVars',
                    type=int, help='number of hidden variables')
parser.add_argument('-n', '--ndps', default=1000, dest='ndps', type=int,
                    help='number of data-points to generate')
parser.add_argument('-d', '--dimdp', default=0, dest='dimdp', type=int,
                    help='linear dimension of each generated data-point, i.e.\
                          size of output array')
args = parser.parse_args()

# Define parameters
ndps = args.ndps
nHiddenVars = args.nHiddenVars
dimdp = args.dimdp
if not dimdp:
    dimdp = (nHiddenVars/2)**2

# Each W[:,h] is seen as a sqrt(dimdp)xsqrt(dimdp) matrix
# e.g. matrices will be 5x5 if dimdp==25
# Each of this matrices has one vertical or horizontal bar
# The number of matrices should be equal to the number of hidden variables
W = np.ones((dimdp, nHiddenVars))*0.1
dimMatrix = int(sqrt(dimdp))
nBars = min(nHiddenVars, 2*dimMatrix)
value = 0.8
# Paint vertical bars
for c in range(nBars/2):
    W[[ i*dimMatrix + c for i in range(dimMatrix) ], c ] = value
# Paint horizontal bars
for c in range(nBars/2):
    W[[ i + c*dimMatrix for i in range(dimMatrix) ], c + nBars/2 ] = value

# We want an average of 2 bars/data-point
Pi = 2./nHiddenVars

dps = []
for i in range(ndps):
    # Generate hidden variables array s
    s = bernoulli.rvs(Pi, size=nHiddenVars)
    # Evaluate array of bernoulli probabilities for the data-points y
    yProb = 1 - np.prod(1 - W*s, axis=1)
    # produce a data-point and put it in data-points
    dps.append([ bernoulli.rvs(yProb[d]) for d in range(dimdp) ])

dpsArray = np.array(dps, int)
np.set_printoptions(threshold=nHiddenVars-1)
print "data-points\n", dpsArray
print "\nPi", Pi
print "\nW\n", W
np.save("s" + str(ndps), dpsArray)
np.savez("t" + str(ndps), Pi=Pi, W=W)
print "parameters were saved in file t" + str(ndps) + ".npz"
print "data-points were saved in file s" + str(ndps) + ".npy"
