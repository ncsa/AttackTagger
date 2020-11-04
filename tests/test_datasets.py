#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-02-09 21:58:46 phuong>

import sys, os
import numpy as np
import pdb
import pudb;

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm
from tables import Events as SE, UserStates as SU, AttackStates as SA
import functions

def test_datasets_ncsa():
    import datasets
    for df, compromised_users in datasets.load_ncsa(): # for each incident
        print df.shape, compromised_users
