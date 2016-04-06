#!/usr/bin/env python
# generate samples from a Noisy-OR mixture
# author: blue, 29/03/2016

import numpy as np
from scipy.stats import bernoulli
from math import sqrt
import argparse

# Defiine parser
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--nHiddenVars', default=8, dest='nHiddenVars',
                    type=int, help='number of hidden variables')
parser.add_argument('-n', '--nsamples', default=500, dest='nSamples', type=int,
                    help='number of samples to generate')
parser.add_argument('-d', '--dimSample', default=16, dest='dimSample', type=int,
                    help='linear dimension of each generated sample, i.e.\
                          size of output array')
args = parser.parse_args()

# Define parameters
nSamples = args.nSamples
nHiddenVars = args.nHiddenVars
dimSample = args.dimSample

# Each W[:,j] is seen as a sqrt(nHiddenVars)xsqrt(nHiddenVars) matrix
# e.g. matrices will be 5x5 if nHiddenVars==25
# Each of this matrices has one vertical or horizontal bar
W = np.ones((dimSample, nHiddenVars))*0.1
# W columns (vertical bars)
dimMatrix = int(sqrt(dimSample))
nBarPatterns = min(nHiddenVars/2, dimMatrix)
for c in range(nBarPatterns):
    W[[ i*dimMatrix + c for i in range(dimMatrix) ], c ] = 0.8
# W rows (horizontal bars)
for c in range(nBarPatterns):
    W[[ i + c*dimMatrix for i in range(dimMatrix) ], c + nBarPatterns ] = 0.8

# hidden variables' weights are random
hiddenVarWeights = np.random.rand(nHiddenVars)

samples = []
for i in range(nSamples):
    # Generate hidden variables array s
    s = np.array([ bernoulli.rvs(p) for p in hiddenVarWeights ])
    # Evaluate array of bernoulli probabilities for the samples y
    yProb = 1 - np.prod(1 - W*s, axis=1)
    # produce a sample and put it in samples
    samples.append([ bernoulli.rvs(yProb[d]) for d in range(dimSample) ])

samplesArray = np.array(samples, int)
np.set_printoptions(threshold=nHiddenVars-1)
print "samples\n", samplesArray
print "\nhidden vars weights", hiddenVarWeights
print "\nW\n", W
np.save("samples", samplesArray)
np.savez("t" + str(nSamples), hiddenVarWeights=hiddenVarWeights, W=W)
