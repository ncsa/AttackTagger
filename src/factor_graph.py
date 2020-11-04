#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-02-19 13:12:40 phuong>
import sys, os
import numpy as np
from tables import Events as SE, UserStates as SU, AttackStates as SA
import functions

sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this
import opengm

class FactorGraph():
    def __init__(self, states, user_event_state_functions, event_state_functions, state_state_functions, metric_list):
        self.states = states
        self.metric_functions = [x[0] for x in metric_list]
        self.metric_list = metric_list
        self.user_event_state_functions = user_event_state_functions
        self.event_state_functions = event_state_functions
        self.state_state_functions = state_state_functions
        
        # weight
        self.w = None
        self.w_count = 0

        # num_factor
        self.num_factor = 0

    def buildgm_(self, events, u = None, w= None):
        self.u = u
        
        self.set_weight(w)
        
        # constants
        self.N_S = len(self.states) # number of states
        # print N_S

        # event array
        E_ = np.array([int(x) for x in events])
        N = len(E_) # length of events
        # print E, N_E

        # metric functions
        self.N_M = len(self.metric_functions) # length of metrics
        # print N_M

        # metrics array
        self.M = np.zeros(shape=(self.N_M, N))
        for i in range(0, N):
            for f in self.metric_functions:
                row, col = self.metric_functions.index(f), i
                if i >= 1:
                    self.M[row, col] = f(E_, i)
                else:
                    self.M[row, col] = 0

        # Shape of the graph:
        # 0: user profile
        # [1-event, 1-M metrics, SU, SA]
        U_ = np.array([1])
        E_ = np.array([1])
        M_ = np.ones(shape=(1, self.N_M))
        S_ = np.array(self.states)
        # print U_
        # print E_, M_, S_
        # raise SystemExit

        # variable list
        l = np.concatenate((U_, np.tile(np.concatenate((E_, M_.flatten(), S_.flatten())), N)))
        
        # user profile - (event - metric(s) - state)
        gm = opengm.graphicalModel(l)
        
        self.helper_()
        self.add_user_event_state(gm, events)
        self.add_event_state(gm, events)
        self.add_state_state(gm, events)
        self.add_metric_state(gm, events)
        
        # print "gm :",gm            
        # print "number of Variables : ",gm.numberOfVariables
        # print "number of Factors :", gm.numberOfFactors
        # print "is Acyclic :" , gm.isAcyclic()
        
        return gm

    def helper_(self):
        # shape of su, sa: [3,10]
        # cell shape: shape of a training sample includes: event, metrics, su, sa: [1, 1, 1, 1, 1, 3, 10]
        # this is for 1 event, 1*4 metrics, 3,10 for su, sa

        # variable indice of su, sa

        # cell shape of E, M, S
        self.cell_shape = [1] # E
        [self.cell_shape.append(1) for x in range(0, self.N_M)] # M
        [self.cell_shape.append(self.states[x]) for x in range(0, len(self.states))] # S
        # e.g., [1, 1, 3, 5] for 1 event, 1 metric, 3 for su, 5 for sa
        
        self.cell_shape_su_sa = []
        [self.cell_shape_su_sa.append(self.states[x]) for x in range(0, len(self.states))]
        # [3, 10] for su, sa
        # print len(self.states)
        # print self.cell_shape_su_sa
        
        # variable indices of E, M, S
        self.variable_indices = []
        [self.variable_indices.append(i) for i in range(0, len(self.cell_shape))]
        # e.g., 0, 1, 2, 3 for 1 event, 1 metric, 1 su, 1 sa

        self.variable_indices_su_sa = []
        base = 1 + self.N_M # 1 for event, N_M for metrics
        [self.variable_indices_su_sa.append(base+i) for i in range(0, len(self.states))]
        # 2,3 for 1 event and 1 metric
        # print self.N_M
        # print self.variable_indices_su_sa
        # raise SystemExit
        
        # variable indices of event and matric
        self.event_metric_indices = []
        [self.event_metric_indices.append(0) for i in range(0, 1+ self.N_M)]
        # 0, 0 for 1 event and 1 metric
        
    def add_factor(self, gm, fa, varlist):
        mul = 1
        
        if (self.w != None):
            mul = self.w[self.w_count]
            self.w_count += 1
            
        fid = gm.addFunction(mul*fa)
        gm.addFactor(fid, varlist)
        return gm

    def set_weight(self, w):
        self.w = w 
        self.w_count = 0

    def add_state_state(self, gm, E):
        N = len(E)
        # skip start/stop events
        begin = 1
        end = N
        # begin = 2
        # end = N-1
        for i in range(begin, end):
            e = E[i] 
            ep = E[i-1]
            for f in self.state_state_functions:
                a = np.zeros(self.cell_shape_su_sa*2)
                for sup in range(0, self.states[0]): # skip start-stop
                    for sap in range(0, self.states[1]):
                        for su in range(0, self.states[0]): # skip start-stop
                            for sa in range(0, self.states[1]):
                                # index = tuple(self.event_metric_indices + [sup, sap] + self.event_metric_indices + [su, sa])
                                index = tuple([sup, sap] + [su, sa])
                                a[index] = f(ep, sup, sap, e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
                varlist = self.variable_indices_su_sa + [x + len(self.cell_shape) for x in self.variable_indices_su_sa]
                varlist = [1 + (i-1)*(len(self.cell_shape)) + x for x in varlist]
                # print varlist
                # raise SystemExit
                gm = self.add_factor(gm, a, varlist)
                
    def add_event_state(self, gm, E, n = None, L = None):
        N = len(E)
        # skip start/stop events
        begin = 0
        end = N
        #begin = 1
        #end = N-1
        for i in range(begin, end):
            e = E[i] 
            for f in self.event_state_functions:
                a = np.zeros(self.cell_shape_su_sa)
                for su in range(0, self.states[0]): # skip start-stop
                    for sa in range(0, self.states[1]):
                        # index = tuple(self.event_metric_indices + [su, sa])
                        index = tuple([su, sa])
                        a[index] = f(e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
                # varlist = [1 + i*(len(self.cell_shape)) + x for x in self.variable_indices] # TODO: fix this :(
                varlist = [1 + i*(len(self.cell_shape)) + x for x in self.variable_indices_su_sa] # TODO: fix this :(
                gm = self.add_factor(gm, a, varlist)
                
    def add_user_event_state(self, gm, E):
        N = len(E)
        # skip start/stop events
        begin = 0
        end = N
        #begin = 1
        #end = N-1
        for i in range(begin, end):
            e = E[i] 
            #print 'E[', i, ']', E[i], '\n'
            for f in self.user_event_state_functions:
                a = np.zeros(self.cell_shape_su_sa)
                for su in range(0, self.states[0]): # skip start-stop
                    for sa in range(0, self.states[1]):
                        # index = tuple(self.event_metric_indices + [su, sa])
                        index = tuple([su, sa])
                        a[index] = f(self.u, e, su, sa) # fix e, e only has 1 state thus f[0, ...] 
                # varlist = [1 + i*(len(self.cell_shape)) + x for x in self.variable_indices] # TODO: fix this :(
                varlist = [1 + i*(len(self.cell_shape)) + x for x in self.variable_indices_su_sa] # TODO: fix this :(
                gm = self.add_factor(gm, a, varlist)
                
                
    def add_metric_state(self, gm, E):
        N = len(E)
        # skip start/stop events
        begin = 0
        end = N
        #begin = 1
        #end = N-1
        for i in range(begin, end):
            for m in self.metric_list:
                row = self.metric_functions.index(m[0])
                for f in m[1]:
                    a = np.zeros(self.cell_shape_su_sa)
                    for su in range(0, self.states[0]): # skip start-stop
                        for sa in range(0, self.states[1]):
                            index = tuple([su, sa])
                            m = self.M[row, i]
                            a[index] = f(m, E, su, sa, i) # fix e, e only has 1 state thus f[0, ...]  # event = E[i]
                    varlist = [1 + i*(len(self.cell_shape)) + x for x in self.variable_indices_su_sa] # TODO: fix this :(
                    gm = self.add_factor(gm, a, varlist)
                
    
    def predict(self, u , events, w = None):
        gm = self.buildgm_(events, u, w)
        param = opengm.InfParam(steps=50, damping=0.5)
        inf=opengm.inference.BeliefPropagation(gm,parameter=param, accumulator='maximizer')
        #inf=opengm.inference.Gibbs(gm)
        inf.infer()
        #for x in range(0,5):
        #    print inf.marginals(x)
        # raise SystemExit
        y_hat = inf.arg()
        return y_hat, self.id2label_(y_hat, events)

    def build_event_fv(self, E, Y, i):
        fv = []
        e = E[i] 
        for f in self.event_state_functions:
            su, sa = Y[i][0], Y[i][1]
            fv.append(f(e, su, sa))
        return fv
            
    def build_state_fv(self, E, Y, i):
        fv = []
        e = E[i] 
        ep = E[i-1]
        for f in self.state_state_functions:
            sup = Y[i][0]
            sap = 0, Y[i][1]
            su = Y[i][0]
            sa = Y[i][1]
            fv.append(f(ep, sup, sap, e, su, sa))
        return fv

    def build_fv(self, E, Y, i):
        fv_func = [self.build_event_fv, self.build_state_fv]
        fv = []
        for f in fv_func:
            fv += f(E, Y, i)
        return fv
    
    def transform(self, X, Y): # should be the full model with 0 for known variables
        return
        import numpy as np
        gm = self.buildgm_(X) # build w/o weight
        
        # TODO: dry
        N = len(X)
        
        U_ = np.array([0])
        E_ = np.array([0])
        M_ = np.zeros(shape=(1, self.N_M))

        l = U_
        for i in range(0, N):
            cell = np.concatenate((E_, M_.flatten(), np.array([Y[i][0], Y[i][1]])))
            l = np.concatenate((l, cell.flatten()))
        
        Y = l
        # 
        flist = []
        for f in gm.factorIds():
            f_variables = gm[f].variableIndices.__tuple__()
            l = [] # tuple of variables
            for v in f_variables:
                l.append(Y[v]) # append the value of the variable
            a = np.array(gm[f])
            flist.append(a[tuple(l)])
        return np.array(flist)
    
    def learn(self, X_train, Y_train):
        return
        N_SAMPLES = len(X_train)
        
        for i in range(0,N_SAMPLES):
            X_t = X_train[i] 
            Y_t = Y_train[i]
            print X_t, Y_t
            
            y_hat = predict(X_t, w)
            
            print y_hat

        #     y_hat = predict(X_t, w)

        #     y = [0,0,0] + list(Y_t)

        #     # print  y, y_hat
        #     # update w
        #     f_truth= transform(X_t, y)
        #     f_predicted= transform(X_t, y_hat)

        #     w = w + (f_truth - f_predicted)
        #     # print w

        # print w
        # y_hat = predict(X_test, w)
        # print y_hat 
        
    def id2label_(self, Z, E):
        N = len(E)
        su_offset = 1 + self.N_M
        sa_offset = su_offset + 1
        label = []
        for i in range(0, N): # skip start-stop
            e = E[i]
            base = 1 + i*len(self.cell_shape)
            su = int(Z[base+su_offset])
            sa = int(Z[base + sa_offset])
            label.append((e, su, sa))
        return ResultLabel(label)

class ResultLabel(object):
    def __init__(self, label):
        self.label = label
    def __str__(self):
        s = ""
        for (e, su, sa) in self.label:
            s = s + '{}\t\t\t\t{}\t{}\n'.format(SE(e), SU(su), SA(sa))
        return s
    def __repr__(self):
        return self.__str__()
