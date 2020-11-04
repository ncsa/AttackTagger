#!/usr/bin/env python
# -*- compile-command: "cd ../ && make test" -*-
# Time-stamp: <2014-02-04 21:15:54 phuong>
import sys, os
import numpy as np

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm
from tables import Events as SE, UserStates as SU, AttackStates as SA


class GraphCRF():
    def __init__(self, events, states, metric_functions):
        # constants
        N_S = len(states) # number of states
        # print N_S

        # event array
        E = np.array([int(x) for x in events])
        N = len(E) # length of events
        # print E, N_E

        # metric functions
        N_M = len(metric_functions) # length of metrics
        # print N_M

        # metrics array
        M = np.zeros(shape=(N_M, N))
        for i in range(0, N):
            for f in metric_functions:
                row, col = metric_functions.index(f), i
                M[row, col] = f(E, i)

        U_ = np.array([1])
        E_ = np.array([1])
        M_ = np.ones(shape=(1, N_M))
        S_ = np.array(states)

        l = np.concatenate((U_, np.tile(np.concatenate((E_, M_.flatten(), S_.flatten())), N)))
        
        gm = opengm.graphicalModel(l)
        pass
    
    def add_event_state(self, factors):
        # skip start/stop events
        begin = 1
        end = N-1
        factor_shape = [1] + self.states
        for i in range(begin, end):
            e = self.E[i] 
            for f in factors:
                fa = np.zeros(factor_shape)
                for s1 in range(0, self.states[0]): # skip start-stop
                    for s2 in range(0, self.states[1]):
                        fa[0,s1,s2] = f(e, s1, s2) # fix e, e only has 1 state thus f[0, ...] 
                fid = gm.addFunction(fa)
                gm.addFactor(fid,[i*(len(L_S)) + x for x in [1, 2, 3]]) # TODO: fix this :(
        pass

def test_graphcrf():
    # test events
    E = [
        SE.start,
        SE.login,
        SE.download,
        SE.compile,
        SE.delete,
        SE.stop
        ]
    states = [len(list(SU)), len(list(SA))]
    metric_functions = [lambda E, i: 0, lambda E, i: 1]
    f = GraphCRF(E, states, metric_functions)

    l = [1, 2, 3]
    o = [0, 0, 0]
    for s in l:
        for t in range(1,s):
            o[l.index(s)] = t
            print o

def xest():
    from functions import F_ES, F_SS, F_M , F_SS_START, F_SS_STOP # functions

    # load incident dataset
    import dataset.ncsa as ncsa

    # state spaces
    N_SU = len([x for x in SU])
    N_SA = len([x for x in SA])
    L_S = [N_SU, N_SA]
        
    # for each incident
    for df, compromised_users in ncsa.read():
        print compromised_users
        # for each user
        for u in set(compromised_users):
            # add timestamp for stop and start
            df_user = df[df['user'] == u]
            df_user_with_start_stop = ncsa.add_start_stop_and_timestamp(df_user)
            # build the event array for the user, converting raw events to number
            E = np.array([int(SE(x)) for x in list(df_user_with_start_stop['event'])])
            # print u, df_user_with_start_stop, E
            print u
            # do the inference
            if (u == 'smisra'):
                infer_(E, F_ES, F_SS, F_SS_START, F_SS_STOP, F_M, L_S)

def infer_(E, F_ES, F_SS, F_SS_START, F_SS_STOP, F_M, L_S):
    # config
    UNARY = 1
    EVENT = 1
    START = 1
    STOP = 1
    EDGE = 1
    METRIC = 1
    
    # init
    N = len(E)
    assert N >= 3 # N must >= 3
    
    # build array of variables in the model
    # fixed variables are events and metrics

    # events and states
    t = [1] + L_S # This is the shape of a row: 1-userstate-attack-state
    event_and_state = t*N # 1-observed event, 4-user state, 4-attack state
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
    
    if UNARY:
        # unary factor for start
        fa = np.zeros([1])
        # TODO: fix this :(
        fa[0] = 1 # fa[idnex]: fix e, e only has 1 state thus f[0, ...] 
        fid = gm.addFunction(fa)
        gm.addFactor(fid,[0]) # [variables index]

        # unary factor for stop
        fa = np.zeros([1])
        # TODO: fix this :(
        fa[0] = 1 # fix e, e only has 1 state thus f[0, ...] 
        fid = gm.addFunction(fa)
        gm.addFactor(fid,[(N-1)*(len(L_S)+1) + x for x in [0]]) # TODO: fix this :(
    

    if EVENT:
        # factor for event-state
        for i in range(1, N-1):
            e = E[i] # we only iterate in E for N times with N events
            for f in F_ES:
                fa = np.zeros(t)
                for s1 in range(0, L_S[0]): # skip start-stop
                    for s2 in range(0, L_S[1]):
                        fa[0,s1,s2] = f(e, s1, s2) # fix e, e only has 1 state thus f[0, ...] 
                fid = gm.addFunction(fa)
                gm.addFactor(fid,[i*(len(L_S) + 1) + x for x in [0, 1, 2]]) # TODO: fix this :(

    if START:
        # factor for edge (including start-stop state)
        # start-first event
        for f in F_SS_START:
            e = E[1]
            fa = np.zeros([1, L_S[0], L_S[1]]) # construct array of 6 variables in that factor
            for su in range(0, L_S[0]): # include start-stop
                for sa in range(0, L_S[1]):
                    fa[0,su,sa] = f(e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
            fid = gm.addFunction(fa)
            gm.addFactor(fid,[3, 4, 5]) #TODO: fix this hard code
                
    if STOP:
        # stop-first event
        for f in F_SS_STOP:
            fa = np.zeros([1, L_S[0], L_S[1]]) # construct array of 6 variables in that factor
            e = E[N-2]
            for su in range(0, L_S[0]): # include start-stop
                for sa in range(0, L_S[1]):
                    fa[0,su,sa] = f(e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
            fid = gm.addFunction(fa)
            gm.addFactor(fid,[(N-2)*(len(L_S) + 1) + x for x in [0, 1, 2]])
                
    if EDGE:
        # edge-edge
        for i in range(2, N-1):
            ep = E[i-1]
            e = E[i] # we only iterate in E for N times with N events
            for f in F_SS:
                fa = np.zeros(t*2) # construct array of 6 variables in that factor
                for sup in range(0, L_S[0]):
                    for sap in range(0, L_S[1]):
                        for su in range(0, L_S[0]): # include start-stop
                            for sa in range(0, L_S[1]):
                                fa[0,sup,sap,0,su,sa] = f(ep, sup, sap, e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
                                # TODO: fix this, avoid hard coding
                fid = gm.addFunction(fa)
                l = [(i-1)*(len(L_S) + 1) + x for x in [0, 1, 2, 3, 4, 5]]
                gm.addFactor(fid,l)

    if METRIC:
        # metric
        current_metric_index = 0
        for f in F_M:
            fa = np.zeros([L_S[0], L_S[1], 1], dtype=float) # metric-su-sa TODO: fix this
            for su in range(2, L_S[0]): # skip start-stop
                for sa in range(2, L_S[1]):
                    E_ = E[1:-1].astype(np.float32) # skip start-stop and convert E to float 
                    fa[su, sa, 0] = f(E_, su, sa) # skip start-stop
            # normalize fa
            if (fa.sum() != 0):
                fa/=fa.sum()
            # w=3
            # fa*=w
            fid = gm.addFunction(fa)
            # TODO: better way to come up with this
            last_su = N_event_and_state-(len(L_S) + 1)  - 2 # skip start-stop and 
            last_sa = N_event_and_state-(len(L_S) + 1)  - 1 # skip start-stop and 
            current_metric = N_event_and_state - 3 + current_metric_index
            # gm.addFactor(fid,[last_su, last_sa, current_metric])
            current_metric_index = current_metric_index + 1
    
    param = opengm.InfParam(steps=1000, damping=0.5)
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
    for i in range(1, N-1):
    # for i in range(0, N):
        e = E[i]
        su = int(Z[i*3+1:i*3+2])
        sa = int(Z[i*3+2:i*3+3])
        print('{}\t\t\t\t{}\t{}'.format(SE(e), SU(su), SA(sa)))

def main():
    from tables import Events as SE, UserStates as SU, AttackStates as SA
