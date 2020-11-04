#!/usr/bin/env python
# -*- compile-command: "cd .. && make test_nb" -*-
# Time-stamp: <2015-02-04 16:40:37 phuong>

import sys, os
import numpy as np
import pdb
import pudb
import time
import pandas as pd
from collections import defaultdict

try:
    import cPickle as pickle
except:
    import pickle

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm
from tables import Events as SE, UserStates as SU, AttackStates as SA, \
Events_NCSA, Events_
from user_profile import UserProfile, User_Profile as UP
import functions
import datasets


def extract_fv():
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()

def build_fv(df, u, compromised=False):
    df_user = df[df['user'] == u].sort_index()
    measurement = defaultdict()
    for row in df_user.iterrows():
        r = row[1]
        if str(r.event) in Events_NCSA:
            measurement[r.event] = 1
    return dict(measurement)
    
def load_ncsa_ds(dataset):
    # [X, Y, vec] = pickle.load(open("result/test_compare_other_method_.pickle", 'r'))
    # eval_result(X, Y, vec)
    # return
    import attack_sequencing
    import experiment
    col = {'incident', 'event', 'time'}
    df_result = pd.DataFrame(columns=col)
    X = []
    Y = []
    count = 0
    for incident, df, compromised_users in dataset: # for each incident
        for u in set(df.user):
            print("Loading {} in {} ...".format(u, incident))
            df_user = df[df['user'] == u].sort_index()
            if len(df_user) > 100 and u not in set(compromised_users):
                # print 'skip {} in incident {}, len event = {}'.format(u, incident, len(df_user))
                continue
            count = count + 1
            compromised=0
            if u in compromised_users:
                compromised=1
            x = build_fv(df, u)
            y = compromised
            X.append(x)
            Y.append(y)
        #     if (count == 2000):
        #         break
        # if (count == 2000):
        #     break
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    X_ = vec.fit_transform(X).toarray()
    pickle.dump([X_, Y, vec], open('result/test_compare_other_method_.pickle', 'wb'))
    return (X_, Y, vec)

def test_nb_main():
    eval_result()
    
def eval_result():
    from sklearn import cross_validation
    from sklearn import svm
    from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
    from sklearn import tree
    from sklearn.metrics import confusion_matrix
    from sklearn import dummy
    from collections import defaultdict
    from dummy_classifier import RuleClassifier, CountClassifier

    
    (X_train, Y_train, vec_train) = load_ncsa_ds(datasets.load_ncsa_train())
    (X_test, Y_test, vec_test) = load_ncsa_ds(datasets.load_ncsa())

    # X_ = []
    # Y_ = []
    # for i in xrange(0,len(Y)):
    #     if Y[i] == 1:
    #         X_.append(X[i])
    #         Y_.append(Y[i])
    classifiers = [
        svm.SVC(kernel='linear', C=1),
        svm.SVC(kernel='linear', C=100),
        svm.SVC(kernel='linear', C=1000),
        svm.SVC(kernel='linear', C=10000),
        # GaussianNB(),
        # MultinomialNB(),
        BernoulliNB(),
        tree.DecisionTreeClassifier(),
        dummy.DummyClassifier(strategy='stratified'),
        RuleClassifier(vec_train),
        ]
    
    d = defaultdict()
    for clf in classifiers:
        y_test_pred = clf.fit(X_train, Y_train).predict(X_test)
        cm = confusion_matrix(Y_test, y_test_pred)
        tp = 1.0*cm[1][1]/(cm[1][0] + cm[1][1])
        tn = 1.0*cm[0][0]/(cm[0][0] + cm[0][1])
        fp = 1.0*cm[0][1]/(cm[0][0] + cm[0][1])
        fn = 1.0*cm[1][0]/(cm[1][0] + cm[1][1])
        ac = 1.0*(cm[1][1] + cm[0][0] )/ 5027 # TODO: fix this
        d[str(clf)] = {
            'classifier': str(clf),
            'true_positive': (tp, cm[1][1]),
            'true_negative': (tn, cm[0][0]),
            'false_positive': (fp, cm[0][1]),
            'false_negative':(fn, cm[1][0])
        }
        d[str(clf)]['y_test_pred'] = y_test_pred
        print(d[str(clf)])
    
    pickle.dump(d, open('result/test_compare_other_method.pickle', 'wb'))
        
    # d = defaultdict()
    # for clf in classifiers:
    #     y_pred = clf.fit(X, Y).predict(X)
    #     y_true = Y
    #     cm = confusion_matrix(y_true, y_pred)
    #     d[str(clf)] = cm
    #     tp = 1.0*cm[1][1]/(cm[1][0] + cm[1][1])
    #     tn = 1.0*cm[0][0]/(cm[0][0] + cm[0][1])
    #     fp = 1.0*cm[0][1]/(cm[0][0] + cm[0][1])
    #     fn = 1.0*cm[1][0]/(cm[1][0] + cm[1][1])
    #     ac = 1.0*(cm[1][1] + cm[0][0] )/ 5027 # TODO: fix this
    #     print str(clf), cm, tp, tn, fp, fn, ac
        
    # cm = [[4965, 82], [8, 24]]
    # tp = 1.0*cm[1][1]/(cm[1][0] + cm[1][1])
    # tn = 1.0*cm[0][0]/(cm[0][0] + cm[0][1])
    # fp = 1.0*cm[0][1]/(cm[0][0] + cm[0][1])
    # fn = 1.0*cm[1][0]/(cm[1][0] + cm[1][1])
    # ac = 1.0*(cm[1][1] + cm[0][0] )/ 5027
    # print 'at', cm, tp, tn, fp, fn, ac
    # pickle.dump(d, open('result/test_compare_other_method.pickle', 'wb'))
