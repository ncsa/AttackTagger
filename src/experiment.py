#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2015-01-11 22:09:33 phuong>
import sys, os
import numpy as np

import attack_sequencing
import datasets

from tables import N_Events, N_UserStates, N_AttackStates, Events as SE, UserStates as SU, AttackStates as SA

def experiment():
    for df, compromised_users in datasets.load_ncsa():
        # for each user
        for u in set(compromised_users):
            # add timestamp for stop and start
            df_user = df[df['user'] == u]
            df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
            # build the event array for the user, converting raw events to number
            E = df_user_with_start_stop['event']
            u = None
            y_hat, y_hat_pretty = attack_sequencing.sequence(u, E)
            print y_hat_pretty
            print eval_accuracy([(1,2)], [(1,4)])
            raise SystemExit

def eval_accuracy(Y, Y_hat): # TODO
    """ 0: if Y_hat contains malicious and Y also contains malicious then return 1
    """
    score = 0
    for sy,sy_hat in zip(Y, Y_hat):
        for i in xrange(0,2):
            if sy[i] == sy_hat[i]:
                score = score + 1
    return float(score)/(len(Y)*2)

def eval_accuracy_compromised(Y_hat):
    """ 0: if Y_hat contains malicious and Y also contains malicious then return 1
    """
    begin = 1
    end = len(Y_hat) - 1
    for i in xrange(begin, end):
        su = Y_hat[i][0]
        if (SU(su) == SU.malicious):
            return 1
    return 0

def eval_accuracy_num_event_detected(Y_hat):
    """ 0: if Y_hat contains malicious and Y also contains malicious then return 1
    """
    begin = 1
    end = len(Y_hat) - 1
    for i in xrange(begin, end):
        su = Y_hat[i][0]
        if (SU(su) == SU.malicious):
            return i
    return 0

def eval_preemption_timeliness(df, y_hat):
    """
    df: data frame of user event (including start-stop)
    y_hat: prediction of labels (list of tuples of int value including start-stop)
    output:
    -1: no detection
    0: detect when the user is malicious
    >0: time in seconds that detected
    """
    begin = None
    end = None
    count = 0
    for su, sa in y_hat:
        if (begin == None and su == int(SU.malicious)):
            begin = df.index[count]
        end = df.index[count]
        count += 1

    if (begin == None) and end != None: # detected malicious but not suspicious
        return 0
    if (begin == None) and end == None: # no detection
        return -1
    if (begin != None) and end == None: # if detect suspicious but can not conclude malicious
        return -1
    if end < begin: # if detect malicious before detect suspicious
        return 0
    # else: return detection time
    return (end - begin).total_seconds()

def eval_preemption_timeliness_old(df, y_hat):
    """
    df: data frame of user event (including start-stop)
    y_hat: prediction of labels (list of tuples of int value including start-stop)
    output:
    -1: no detection
    0: detect when the user is malicious
    >0: time in seconds that detected
    """
    begin = None
    end = None
    count = 0
    for su, sa in y_hat:
        if (begin == None and su == int(SU.suspicious)):
            begin = df.index[count]
        if (end == None and su == int(SU.malicious)):
            end = df.index[count]
        count += 1

    if (begin == None) and end != None: # detected malicious but not suspicious
        return 0
    if (begin == None) and end == None: # no detection
        return -1
    if (begin != None) and end == None: # if detect suspicious but can not conclude malicious
        return -1
    if end < begin: # if detect malicious before detect suspicious
        return 0
    # else: return detection time
    return (end - begin).total_seconds()

def eval_detection_timeliness(df, y_hat):
    """
    df: data frame of user event (including start-stop)
    y_hat: prediction of labels (list of tuples of int value including start-stop)
    output:
    -1: no detection
    0: detect when the user is malicious
    >0: time in seconds that detected
    """
    begin = None
    end = None
    count = 0
    begin = df.index[count]
    for su, sa in y_hat:
        if (end == None and su == int(SU.malicious)):
            end = df.index[count]
        count += 1

    if end == None: # if detect malicious before detect suspicious
        return -1 # no detection
    # else: return detection time
    return (end - begin).total_seconds()

def eval_detection_timeliness_idx(df, y_hat):
    """
    df: data frame of user event (including start-stop)
    y_hat: prediction of labels (list of tuples of int value including start-stop)
    output:
    -1: no detection
    0: detect when the user is malicious
    >0: time in seconds that detected
    """
    begin = None
    end = None
    count = 0
    begin = df.index[count]
    begin_idx = 0
    end_idx = 0
    for su, sa in y_hat:
        if (end == None and su == int(SU.malicious)):
            end = df.index[count]
            end_idx = count
        count += 1

    if end == None: # if detect malicious before detect suspicious
        return -1 # no detection
    # else: return detection time
    return end_idx - begin_idx

def eval_attack_duration(df, y_hat):
    """
    df: data frame of user event (including start-stop)
    y_hat: prediction of labels (list of tuples of int value including start-stop)
    output:
    -1: no detection
    0: detect when the user is malicious
    >0: time in seconds that detected
    """
    begin = None
    end = None
    count = 0
    begin = df.index[count]
    for su, sa in y_hat:
        end = df.index[count]
        count += 1
    # else: return detection time
    return (end - begin).total_seconds()

def plot_result(result):
    return
