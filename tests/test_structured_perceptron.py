#!/usr/bin/env python
# -*- compile-command: "cd ../ && make test" -*-
# Time-stamp: <2014-02-04 11:58:58 phuong>
import sys, os
import numpy as np

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm

def f1(x, y):
    if x == 0 and y == 1:
        return 1
    return 0

gm = opengm.graphicalModel([2, 3])

# third order function for variable 3x2x2
f = np.zeros([2, 3])
for x in range(0, 2):
    for y in range(0, 3):
            f[x,y] = f1(1, y) # fix x == 0
fid = gm.addFunction(f)
gm.addFactor(fid,[0, 1])

param = opengm.InfParam(steps=100, damping=0.5)
inf=opengm.inference.BeliefPropagation(gm,parameter=param)
# start inference (in this case unverbose infernce)
inf.infer()
print inf.marginals(0)
print inf.marginals(1)
print inf.arg()

            
def test_structured_perceptron():
    N = 10
    w = np.random.uniform(-1, 1, size=N)
    train = [
        ([1,2,3,4,5], [6,7]),
        ([4,5,6,1], [2,3])
    ]
    for x, y in train:
        print x, y
        y_hat = predict(w, x)
        if y_hat != y:
            # update
            w = w - alpha*gen(x, y_hat)
    return w
