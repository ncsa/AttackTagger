#!/usr/bin/env python
# -*- compile-command: "cd .. && make test_variation" -*-
# Time-stamp: <2014-02-25 16:44:47 phuong>
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

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

def main():
    import datasets
    import attack_sequencing
    import experiment
    from collections import defaultdict
    col = {'incident', 'event', 'time'}
    df_result = pd.DataFrame(columns=col)
    d = defaultdict()
    for incident, df, compromised_users in datasets.load_ncsa_kafka(): # for each incident
        print 'processing incident {}'.format(incident)
        users = set(df.user)
        for u in users:
            start_time = time.time()
            # from pdb import set_trace; set_trace()
            # add timestamp for stop and start
            df_user = df[df['user'] == u].sort_index()
            if len(df_user) > 100 and u not in set(compromised_users):
                print 'skip {} in incident {}, len event = {}'.format(u, incident, len(df_user))
                continue
            df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
            # build the event array for the user, converting raw events to number
            E = df_user_with_start_stop['event']
            up = UserProfile()
            y_hat, y_hat_pretty = attack_sequencing.sequence(up, E)
            elapsed_time = time.time() - start_time
            preemption_timeliness = experiment.eval_preemption_timeliness(df_user_with_start_stop,
                                                       [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
            detection_timeliness = experiment.eval_detection_timeliness(df_user_with_start_stop,
                                                       [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
            attack_duration = experiment.eval_attack_duration(df_user_with_start_stop,
                                                       [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
            accuracy = experiment.eval_accuracy_compromised([(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
            row = {'incident': incident,
                   'user': u,
                   'labeling_time': elapsed_time,
                   'num_event': len(E)-2,
                   'attack_duration': attack_duration,
                   'preemption_timeliness': preemption_timeliness,
                   'detection_timeliness': detection_timeliness,
                   'accuracy': accuracy,
                   'is_compromised': u in set(compromised_users)
            }
            print 'Processed {}, len {}'.format(u, len(df_user))
            if accuracy == 1 and u not in set(compromised_users):
                print 'misdetected {} in {}'.format(u, incident)
                print y_hat_pretty
            df_result = df_result.append(row, ignore_index=True)
    df_result.to_pickle('../result/ncsa_all.pickle')

if __name__ == '__main__':
    main()
