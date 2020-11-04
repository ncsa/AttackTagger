#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-02-05 16:13:12 phuong>

import sys, os
import numpy as np

sys.path.append('src')
sys.path.append('/home/phuong/w/opengm-2.3/src/interfaces/python') #TODO: fix this

import opengm
from tables import Events as SE, UserStates as SU, AttackStates as SA
import functions

def test_graphcrf():
    import attack_sequencing 
    # test events
    E = [
        SE.start,
        SE.login,
        SE.compile,
        SE.delete,
        SE.stop
        ]
    # test labels
    L = [
(SU.benign, SA.benign),
        (SU.benign, SA.benign),
        (SU.benign, SA.benign),
        (SU.suspicious, SA.prepare_attack),
        (SU.benign, SA.benign),
        ]
    y_hat, y_hat_pretty = attack_sequencing.sequence(E)
    print y_hat
    print y_hat_pretty

def test_experiment():
    import experiment
    experiment.experiment()
