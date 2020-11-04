#!/usr/bin/env python
# -*- compile-command: "cd .. && make test_variation" -*-
# Time-stamp: <2014-02-25 16:44:47 phuong>

import sys, os
import numpy as np
import pdb
import pudb
import time
import pandas as pd
import traceback
from multiprocessing.pool import Pool
import multiprocessing
pd.options.mode.chained_assignment = None

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
import datasets
import attack_sequencing
import experiment

def test_factg():
    """
    result: list of incident_results
    [
    (user, accuraty (0 - not detected or 1 - detected), detection timeliness in second
    ]
    """
    import datasets
    import attack_sequencing
    import experiment
    col = {'incident', 'event', 'time'}
    df_result = pd.DataFrame(columns=col)
    for incident, df, compromised_users in datasets.load_ncsa(): # for each incident
        for u in set(compromised_users):
            start_time = time.time()
            # from pdb import set_trace; set_trace()
            # add timestamp for stop and start
            df_user = df[df['user'] == u].sort_index()
            df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
            # build the event array for the user, converting raw events to number
            E = df_user_with_start_stop['event']
            up = UserProfile()
            y_hat, y_hat_pretty = attack_sequencing.sequence(up, E)
            elapsed_time = time.time() - start_time
            print y_hat_pretty
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
            }
            df_result = df_result.append(row, ignore_index=True)
            detection_timeliness = experiment.eval_detection_timeliness(df_user_with_start_stop,
                                                       [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
            accuracy = experiment.eval_accuracy_compromised([(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
    df_result.to_pickle('result/ncsa.pickle')
    return df_result


def test_attack_variation():
    import itertools
    import datasets
    import attack_sequencing
    import experiment
    col = {'incident', 'user', 'accuracy_list'}
    df_result = pd.DataFrame(columns=col)
    for incident, df, compromised_users in datasets.load_ncsa_variation(): # for each incident
        for u in compromised_users:
            accuracy_list = []
            l = [1215875498, 1215875506, 1215875584, 1215875607]
            for i in itertools.permutations(l):
                df_new = df.copy()
                l_0 = [df_new.index[0], df_new.index[1]]
                new_index = l_0 + list(i)
                df_new = df_new.reindex(new_index)

                start_time = time.time()
                # from pdb import set_trace; set_trace()
                # add timestamp for stop and start
                df_user = df_new[df_new['user'] == u]
                df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
                # # build the event array for the user, converting raw events to number
                E = df_user_with_start_stop['event']
                up = UserProfile()
                y_hat, y_hat_pretty = attack_sequencing.sequence(up, E)
                elapsed_time = time.time() - start_time
                accuracy = experiment.eval_accuracy_num_event_detected([(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
                accuracy_list.append(accuracy)

                row = {'incident': incident,
                       'user': u,
                       'accuracy_list': accuracy_list}
                df_result = df_result.append(row, ignore_index=True)
                print accuracy

    df_result.to_pickle('result/ncsa_variation.pickle')
    return df_result



# Shortcut to multiprocessing's logger
def error(msg, *args):
    return multiprocessing.get_logger().error(msg, *args)

class LogExceptions(object):
    def __init__(self, callable):
        self.__callable = callable
        return

    def __call__(self, *args, **kwargs):
        try:
            result = self.__callable(*args, **kwargs)

        except Exception as e:
            # Here we add some debugging help. If multiprocessing's
            # debugging is on, it will arrange to log the traceback
            error(traceback.format_exc())
            # Re-raise the original exception so the Pool worker can
            # clean up
            raise

        # It was fine, give a normal answer
        return result
    pass

class LoggingPool(Pool):
    def apply_async(self, func, args=(), kwds={}, callback=None):
        return Pool.apply_async(self, LogExceptions(func), args, kwds, callback)


def test_factg_all():
    import datasets
    import attack_sequencing
    import experiment
    from collections import defaultdict
    from multiprocessing import Pool, cpu_count

    os.system('clear')
    result_col = {'event'}
    df_pickle = pd.DataFrame(columns=result_col)
    queue_col = {'timestamp', 'user', 'event', 'su', 'sa'}
    df_queue = pd.DataFrame(columns=queue_col)
    d = defaultdict()
    kafka = datasets.KafkaLogger()
    if (kafka.consumer is None):
        print 'consumer is None'
        return

    pool = Pool(processes=cpu_count())
    #multiprocessing.log_to_stderr()
    #pool = LoggingPool(processes=cpu_count())
    while 1:
        df = kafka.load_ncsa_kafka() # for each incident

        df.sort_index(inplace=True)
        print 'new_events:\n', df, '\n'

        df_queue = df_queue.append(df)

        ## get rid of duplicate events here, Keep most recent duplicate
        df_queue = df_queue.loc[df_queue.event.shift(-1) != df_queue.event]

        #take last 20 events
        df_queue = df_queue.tail(20)

        #print 'df_queue:\n', df_queue, '\n'

        users = set(df_queue.user)
        for u in users:
            pool.apply_async(process_user, [u, df_queue], callback=process_user_callback)

def process_user_callback(result):
		(y_hat, y_hat_pretty) = result
    #print(y_hat_pretty)

def process_user(u, df_queue):
    start_time = time.time()
    # from pdb import set_trace; set_trace()
    # add timestamp for stop and start
    df_user = df_queue[df_queue['user'] == u].sort_index()
    df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
    print 'df_user_with_start_stop:\n', df_user_with_start_stop, '\n'
    # build the event array for the user, converting raw events to number
    E = df_user_with_start_stop['event']
    up = UserProfile()
    #print 'before sequencing:\n', df_user_with_start_stop, '\n'
    y_hat, y_hat_pretty = attack_sequencing.sequence(up, E)
    #print 'after sequencing:\n', df_user_with_start_stop, '\n'
    elapsed_time = time.time() - start_time
    preemption_timeliness = experiment.eval_preemption_timeliness(df_user_with_start_stop,
                                                [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
    detection_timeliness = experiment.eval_detection_timeliness(df_user_with_start_stop,
                                                [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
    attack_duration = experiment.eval_attack_duration(df_user_with_start_stop,
                                                [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
    accuracy = experiment.eval_accuracy_compromised([(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
    row = {
            'user': u,
            'labeling_time': elapsed_time,
            'num_event': len(E) - 1,
            'attack_duration': attack_duration,
            'preemption_timeliness': preemption_timeliness,
            'detection_timeliness': detection_timeliness,
            'accuracy': accuracy,
    }
    #print 'Processed {}, len {}'.format(u, len(df_user)) + '\n'
    print y_hat_pretty
    #print '\n===\n'
    #print y_hat
    print '\n---------------------------------------------------------------------------\n'
    return (y_hat, y_hat_pretty)


#def test_factg_all():
#    import datasets
#    import attack_sequencing
#    import experiment
#    from collections import defaultdict
#    col = {'incident', 'event', 'time'}
#    df_result = pd.DataFrame(columns=col)
#    d = defaultdict()
#    while 1:
#      for incident, df, compromised_users in datasets.load_ncsa_kafka(): # for each incident
#          print 'processing incident {}'.format(incident)
#          users = set(df.user)
#          for u in users:
#              start_time = time.time()
#              # from pdb import set_trace; set_trace()
#              # add timestamp for stop and start
#              df_user = df[df['user'] == u].sort_index()
#              if len(df_user) > 100 and u not in set(compromised_users):
#                  print 'skip {} in incident {}, len event = {}'.format(u, incident, len(df_user))
#                  continue
#              df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
#              # build the event array for the user, converting raw events to number
#              E = df_user_with_start_stop['event']
#              up = UserProfile()
#              y_hat, y_hat_pretty = attack_sequencing.sequence(up, E)
#              elapsed_time = time.time() - start_time
#              preemption_timeliness = experiment.eval_preemption_timeliness(df_user_with_start_stop,
#                                                         [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
#              detection_timeliness = experiment.eval_detection_timeliness(df_user_with_start_stop,
#                                                         [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
#              attack_duration = experiment.eval_attack_duration(df_user_with_start_stop,
#                                                         [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
#              accuracy = experiment.eval_accuracy_compromised([(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
#              row = {'incident': incident,
#                     'user': u,
#                     'labeling_time': elapsed_time,
#                     'num_event': len(E)-2,
#                     'attack_duration': attack_duration,
#                     'preemption_timeliness': preemption_timeliness,
#                     'detection_timeliness': detection_timeliness,
#                     'accuracy': accuracy,
#                     'is_compromised': u in set(compromised_users)
#              }
#              print 'Processed {}, len {}'.format(u, len(df_user))
#              if accuracy == 1 and u not in set(compromised_users):
#                  print 'misdetected {} in {}'.format(u, incident)
#                  print y_hat_pretty
#              df_result = df_result.append(row, ignore_index=True)
#    df_result.to_pickle('result/ncsa_all.pickle')
#    return df_result
