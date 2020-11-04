#!/usr/bin/env python
# -*- compile-command: "cd .. && make test_variation" -*-
# Time-stamp: <2014-03-06 12:27:23 phuong>

import sys, os
import numpy as np
import pdb
import pudb
import time
import pandas as pd

try:
    import cPickle as pickle
except:
    import pickle

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm
from tables import Events as SE, UserStates as SU, AttackStates as SA
from user_profile import UserProfile, User_Profile as UP
import functions

def test_factg():
        # user profile - (event - metric(s) - state)
        gm = opengm.graphicalModel(l)
