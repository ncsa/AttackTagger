#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-02-05 20:23:31 phuong>

import numpy as np
from tables import N_Events, N_UserStates, N_AttackStates, Events as SE, UserStates as SU, AttackStates as SA

state_transition = np.array([[0.8, 0.1, 0.1],
                             [0.1, 0.45, 0.45],
                                [0, 0, 1]
                         ])

def entropy(X):
    """ np array, dtype=float
    """
    probs = [np.mean(X == c) for c in set(X)]
    return np.sum(-p * np.log2(p) for p in probs)

def linearlize(su, sa):
    a = np.array([su/float(N_UserStates) + sa/float(N_AttackStates)], dtype=float)
    return a.sum()/len(a)

#

def fes_benign(e, su, sa):
    if su == int(SU.benign) and sa == int(SA.benign):
        return 1
    return -1

def fes_suspicious(e, su, sa):
    if su == int(SU.suspicious) and sa != int(SA.benign) and sa!=int(SA.execute_payload):
        return sa/float(N_AttackStates)
    return 0

def fes_malicious(e, su, sa):
    if su == int(SU.malicious) and sa !=int(SA.benign):
        return sa/float(N_AttackStates)
    return 0

def fes_delete_malicious(e, su, sa):
    if e == int(SE.delete) and su == int(SU.malicious) and sa == int(SA.execute_payload):
        return 1
    return 0

def fes_download_benign(e, su, sa):
    if e == int(SE.download) and su == int(SU.benign)  and sa == int(SA.benign):
        return 1
    return 0

def fes_download_sensitive_suspicious(e, su, sa):
    if e == int(SE.download_sensitive) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
        return 1
    return 0

def fes_failed_password_suspicious(e, su, sa):
    if e == int(SE.ALERT_FAILED_PASSWORD) and su == int(SU.suspicious)  and sa == int(SA.prepare_compromise):
        return 1
    return 0

def fes_anomalous_host_suspicious(e, su, sa):
    if e == int(SE.ALARM_ANOMALOUS_HOST) and su == int(SU.suspicious)  and sa == int(SA.prepare_compromise):
        return 1
    return 0

def fes_command_anomaly_suspicious(e, su, sa):
    if e == int(SE.ALARM_COMMAND_ANOMALY) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
        return 1
    return 0

def fes_multiple_login_suspicious(e, su, sa):
    if e == int(SE.ALARM_MULTIPLE_LOGIN) and su == int(SU.suspicious)  and sa == int(SA.compromised):
        return 1
    return 0

def fes_correlated_alert_suspicious(e, su, sa):
    if e == int(SE.ALERT_CORRELATED) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
        return 1
    return 0

def fes_read_host_info_suspicious(e, su, sa):
    if e == int(SE.read_host_configuration) and su == int(SU.suspicious) and sa == int(SA.gather_information):
        return 1
    return 0

def fes_sudo_suspicious(e, su, sa):
    if e == int(SE.ALERT_SUDO_BRUTEFORCE) and su == int(SU.suspicious) and sa == int(SA.prepare_compromise):
        return 1
    return 0

# FES malicious
def fes_disable_logging_malicious(e, su, sa):
    if e == int(SE.ALERT_DISABLE_LOGGING) and su == int(SU.malicious)  and sa == int(SA.clear_traces):
        return 1
    return 0

def fes_illegal_user_activity_malicious(e, su, sa):
    if e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and su == int(SU.malicious)  and sa == int(SA.prepare_attack):
        return 1
    return 0

def fes_rootkit_malicious(e, su, sa):
    if e == int(SE.ALERT_ROOTKIT_PHALANX) and su == int(SU.malicious) and sa == int(SA.prepare_attack):
        return 1
    return 0

######### FSS_SPECIAL_START_STOP ######
def fss_start_login_benign(e, su, sa):
    if e == int(SE.login) and su == int(SU.benign) and sa == int(SA.benign):
        return 1
    return 0


##### FSS #######
def fss_malicious(ep, sup, sap, e, su, sa):
    return state_transition[int(sup), int(su)]

#specialized
def fss_failed_password_success_login_suspicious(ep, sup, sap, e, su, sa):
    if su == int(SU.suspicious) \
       and sa == int(SA.compromised) \
       and e == int(SE.login) \
       and ep == int(SE.ALERT_FAILED_PASSWORD):
        return 1
    return 0

def fss_request_resource_suspicious(ep, sup, sap, e, su, sa):
    if su == int(SU.suspicious) \
       and sa == int(SA.execute_payload) \
       and e == int(SE.ALERT_REQUEST_ACCESS_RESOURCE):\
        return 1
    return 0

def fss_illegal_user_activity_malicious(ep, sup, sap, e, su, sa):
    # if ep == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and sup == int(SU.suspicious) and sap==int(SA.prepare_attack)\
    #    and e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and su == int(SU.malicious) and sa==int(SA.execute_payload):
    #     return 1
    if sup == int(SU.suspicious) and e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and su == int(SU.malicious) and sa==int(SA.execute_payload):
        return 1
    return 0

#specialized
def fss_rootkit_malicious(ep, sup, sap, e, su, sa):
    if su == int(SU.malicious) \
       and sa == int(SA.execute_payload) \
       and ep == int(SE.ALERT_ROOTKIT_PHALANX):
        return 1
    return 0

# metrics

def fm_entropy(E, su, sa):
    from scipy.misc import logsumexp
    return entropy(E)*linearlize(su,sa)

def fm_consecutive_event(E, su, sa):
    return 3*linearlize(su,sa)

F_ES = [
        # fes_benign, fes_suspicious, fes_malicious,
        # fes_login_benign, fes_download_benign,
        fes_anomalous_host_suspicious,
        fes_command_anomaly_suspicious,
        fes_failed_password_suspicious,
        fes_multiple_login_suspicious,
        fes_correlated_alert_suspicious,
    # malicious
        fes_illegal_user_activity_malicious,
        fes_disable_logging_malicious,
        fes_rootkit_malicious,
    fes_read_host_info_suspicious,
    fes_sudo_suspicious,
]

F_SS_START = [fss_start_login_benign]
F_SS_STOP = []

F_SS = [
        fss_malicious, # state transition of users
        fss_failed_password_success_login_suspicious,
        fss_rootkit_malicious,
        fss_request_resource_suspicious
        ]

F_M = [fm_entropy,
       fm_consecutive_event]


def fss_delete_malicious(ep, sup, sap, e, su, sa):
    # if e == int(SE.delete) \
    #    # and ep == int(SE.compile) \
    #    and su == int(SU.malicious) and sa == int(SA.execute_payload):
    #     return 1
    # return 0
    
    # if e == int(SE.delete) and ep == int(SE.compile) \
    #    and sup == int(SU.suspicious) and sap == int(SA.prepare_attack) \
    #    and su == int(SU.malicious) and sa == int(SA.execute_payload):
    if e == int(SE.delete) \
       and sup == int(SU.suspicious) \
       and su == int(SU.malicious) and sa == int(SA.execute_payload):
        return 1
    return 0

def fss_state_transition(ep, sup, sap, e, su, sa):
    return state_transition[int(sup), int(su)]

def fes_login_benign(e, su, sa):
    if e == int(SE.login) and su == int(SU.benign)  and sa == int(SA.benign):
        return 1
    return 0

def fes_compile_suspicious(e, su, sa):
    if e == int(SE.compile) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
        return 1
    return 0

F_ES_TEST = [
    fes_login_benign,
    fes_compile_suspicious
             ]

F_SS_TEST = [fss_delete_malicious]

F_M_TEST = [lambda E, i: 0, lambda E, i: 1]

def get_functions():
#     return (F_ES_TEST, F_SS_TEST, F_M_TEST)
    return (F_ES, F_SS, F_M_TEST)

class PyCallback(object):
    def __init__(self):
        self.inBegin=False
        self.inEnd=False
        self.inVisit=False
    def begin(self,inference):
        self.inBegin=True
    def end(self,inference):
        self.inEnd=True
    def visit(self,inference):
        self.inVisit=True
