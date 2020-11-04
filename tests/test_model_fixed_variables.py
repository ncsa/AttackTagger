#!/usr/bin/env python
# -*- compile-command: "cd ../ && make test" -*-
# Time-stamp: <2014-01-30 10:36:51 phuong>
import sys, os
import numpy as np

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm
from tables import Events as SE, UserStates as SU, AttackStates as SA

def test():
    from functions import F_ES, F_SS, F_M # functions

    # input event array
    E_ = [ SE.start,
           SE.login,
           SE.download,
           SE.download_sensitive,
           SE.compile,
           SE.stop
        ]
    E = np.array([int(x) for x in E_]) # convert enums to np array of ints
    
    # state spaces
    N_E = len([x for x in SE])
    N_SU = len([x for x in SU])
    N_SA = len([x for x in SA])
    L_V = [N_E, N_SU, N_SA]
    
    # run experiment
    infer_(E, F_ES, F_SS, F_M, L_V)

def infer_(E, F_ES, F_SS, F_M, L_V):
    # init
    N = len(E)
    assert N >= 3 # N must >= 3
    
    # fix variables
    fixed_vars = []
    for i in range(0,N):
        fixed_vars.append((i*3, E[i]))
        if i==0:
            fixed_vars.append((i*3+1, int(SU.start)))
            fixed_vars.append((i*3+2, int(SA.start)))
        if i==N-1:
            fixed_vars.append((i*3+1, int(SU.stop)))
            fixed_vars.append((i*3+2, int(SA.stop)))

    
    # build array of variables in the model
    # fixed variables are events and metrics

    # events and states
    event_and_state = L_V*N # 1-observed event, 4-user state, 4-attack state
    N_event_and_state = len(event_and_state)
    
    # metric
    N_metric = len(F_M)
    metric = [1]*N_metric
    
    # all variables: events, metrics, and states
    l = event_and_state + metric
    
    # construct grphical model based on the variable list
    gm = opengm.graphicalModel(l)

    #
    # Add features to the model
    #
    
    # factor for event-state
    for i in range(1, N-1):
        for f in F_ES:
            fa = np.zeros(L_V)
            for e in range(0, L_V[0]):
                for s1 in range(2, L_V[1]): # skip start-stop
                    for s2 in range(2, L_V[2]):
                        fa[e,s1,s2] = f(e, s1, s2) # fix e, e only has 1 state thus f[0, ...] 
            fid = gm.addFunction(fa)
            gm.addFactor(fid,[i*(len(L_V)) + x for x in [0, 1, 2]]) # TODO: fix this :(
    
    # factor for edge (including start-stop state)
    for i in range(1, N):
        e = E[i] # we only iterate in E for N times with N events
        ep = E[i-1]
        for f in F_SS:
            fa = np.zeros(L_V*2) # construct array of 6 variables in that factor
            for ep in range(0, L_V[0]):
                for sup in range(0, L_V[1]):
                    for sap in range(0, L_V[2]):
                        for e in range(0, L_V[0]):
                            for su in range(0, L_V[1]): # include start-stop
                                for sa in range(0, L_V[2]):
                                    fa[ep,sup,sap,e,su,sa] = f(ep, sup, sap, e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
                                    # TODO: fix this, avoid hard coding
            fid = gm.addFunction(fa)
            gm.addFactor(fid,[(i-1)*(len(L_V)) + x for x in [0, 1, 2, 3, 4, 5]])

    # metric
    current_metric_index = 0
    for f in F_M:
        fa = np.zeros([L_V[1], L_V[2], 1], dtype=float) # metric-su-sa TODO: fix this
        for su in range(2, L_V[1]): # skip start-stop
            for sa in range(2, L_V[2]):
                E_ = E[1:-1].astype(np.float32) # skip start-stop and convert E to float 
                fa[su, sa, 0] = f(E_, su, sa) # skip start-stop
        # normalize fa
        fa/=fa.sum()
        # w=1
        # fa*=w
        fid = gm.addFunction(fa)
        # TODO: better way to come up with this
        last_su = N_event_and_state-(len(L_V))  - 2 # skip start-stop and 
        last_sa = N_event_and_state-(len(L_V))  - 1 # skip start-stop and 
        current_metric = N_event_and_state - 3 + current_metric_index
        gm.addFactor(fid,[last_su, last_sa, current_metric])
        current_metric_index = current_metric_index + 1
    


    gm.fixVariables([x[0] for x in fixed_vars],
                    [x[1] for x in fixed_vars])


    param = opengm.InfParam(steps=100, damping=0.5)
    inf=opengm.inference.BeliefPropagation(gm,parameter=param, accumulator='maximizer')
    # start inference (in this case unverbose infernce)
    inf.infer()
    for x in gm.variables():
        # print 'M({}) = {}'.format(x, inf.marginals(x))
        pass
    Z = inf.arg()
    # print 'Z = {}'.format(Z)
    id2label(Z, E, N)
    # return (gm, inf)

    # param = opengm.InfParam(steps=10000)
    # inf = opengm.inference.Gibbs(gm, parameter=param, accumulator='minimizer')
    # callback=PyCallback()
    # pvisitor=inf.pythonVisitor(callback,1)
    # inf.infer(pvisitor)

def id2label(Z, E, N):
    # TODO: fix this
    for i in range(0, N):
        e = E[i]
        su = int(Z[i*3+1:i*3+2])
        sa = int(Z[i*3+2:i*3+3])
        print('{}\t\t\t\t{}\t{}'.format(SE(e), SU(su), SA(sa)))

def main():
    from tables import Events as SE, UserStates as SU, AttackStates as SA
