#!/usr/bin/env python
# -*- compile-command: "cd .. && make test_nb" -*-
# Time-stamp: <2015-01-20 17:52:58 phuong>

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
    num_compromised = 0
    num_benign = 0
    for incident, df, compromised_users in dataset: # for each incident
        for u in set(df.user):
            print("Loading {} in {} ...".format(u, incident))
            df_user = df[df['user'] == u].sort_index()
            if len(df_user) > 100 and u not in set(compromised_users):
                continue
            count = count + 1
            compromised=0
            if u in compromised_users:
                num_compromised=num_compromised + 1
                compromised=1
            else:
                num_benign = num_benign + 1
    print num_compromised, num_benign

def test_stats():
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

    load_ncsa_ds(datasets.load_ncsa_train())
    load_ncsa_ds(datasets.load_ncsa())
