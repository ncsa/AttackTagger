#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-07-28 13:03:40 phuong>

import numpy as np
from tables import N_Events, N_UserStates, N_AttackStates, Events as SE, UserStates as SU, AttackStates as SA
from user_profile import User_Profile as UP

state_transition = np.array([[0.8, 0.1, 0.1],
                             [0.1, 0.45, 0.45],
                                [0.1, 0.1, 0.9]
                         ])

def is_sensitive_uri(e):
    return e==int(SE.download_sensitive) or e == int(SE.ALERT_SENSITIVE_FTP_URI) or e == int(SE.ALERT_SENSITIVE_HTTP_URI)

class UserEventState():
    def fues_disable_logging_malicious(u, e, su, sa):
        return 0
    
class UserEventState2():
    def fues_disable_logging_malicious(u, e, su, sa):
        if u.get_attribute(UP.previously_compromised) and e == int(SE.ALERT_DISABLE_LOGGING) and su == int(SU.malicious)  and sa == int(SA.clear_traces):
            return 1
        return 0
    def fues_read_host_info_malicious(u, e, su, sa):
        if u.get_attribute(UP.previously_compromised) and e == int(SE.read_host_configuration) and su == int(SU.suspicious)  and sa == int(SA.gather_information):
            return 1
        return 0
    def fues_sudo_bruteforce(u, e, su, sa):
        if u.get_attribute(UP.previously_compromised) and e == int(SE.ALERT_SUDO_BRUTEFORCE) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
class EventState():
    def fes_hosting_hidden_spam_malicious(e, su, sa):
        return 0
    
class EventState2():
    def fes_hosting_hidden_spam_malicious(e, su, sa):
        if e == int(SE.ALERT_HOSTING_HIDDEN_SPAM) and su == int(SU.malicious)  and sa == int(SA.execute_payload):
            return 1
        return 0
    def fes_multiple_login_suspicious(e, su, sa):
        if e == int(SE.ALARM_MULTIPLE_LOGIN) and su == int(SU.suspicious)  and sa == int(SA.prepare_compromise):
            return 1
        return 0
    def fes_watched_country_login(e, su, sa):
        if e == int(SE.ALERT_WATCHED_COUNTRY_LOGIN) and su == int(SU.suspicious)  and sa == int(SA.prepare_compromise):
            return 1
        return 0
    def fes_alert_known_bad_download_suspicious(e, su, sa):
        if e == int(SE.ALERT_KNOWN_BAD_DOWNLOADS) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    def fes_alert_new_authorized_key_suspicious(e, su, sa):
        if e == int(SE.new_authorized_keys) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
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
    def fes_disable_logging_malicious(e, su, sa):
        if e == int(SE.ALERT_DISABLE_LOGGING) and su == int(SU.suspicious)  and sa == int(SA.clear_traces):
            return 1
        return 0
    def fes_rootkit_phalanx(e, su, sa):
        if e == int(SE.ALERT_ROOTKIT_PHALANX) and su == int(SU.malicious)  and sa == int(SA.execute_payload):
            return 1
        return 0
    def fes_malware_hash_malicious(e, su, sa):
        if e == int(SE.ALERT_MALWARE_HASH_REGISTRY_MATCH) and su == int(SU.malicious)  and sa == int(SA.execute_payload):
            return 1
        return 0
    def fes_illegal_activity_malicious(e, su, sa):
        if e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and su == int(SU.malicious)  and sa == int(SA.execute_payload):
            return 1
        return 0
    def fes_change_credential_suspicious(e, su, sa):
        if e == int(SE.ALERT_CHANGE_CREDENTIAL) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    def fes_change_credential_suspicious(e, su, sa):
        if e == int(SE.ALERT_SUDO_BRUTEFORCE) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    def fes_over_loaded_overlimit(e, su, sa):
        if e == int(SE.overloaded_over_limit) and su == int(SU.malicious)  and sa == int(SA.execute_payload):
            return 1
        return 0

class StateState():
    def fss_start_benign(ep, sup, sap, e, su, sa):
        return 0
        if (ep == int(SE.start) and su == int(SU.benign) and sa == int(SA.benign)):
            return 1
        return 0
    
    def fss_stop_malicious(ep, sup, sap, e, su, sa):
        return 0
        if (e == int(SE.stop) and sup == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0

    def fss_request_access_resource_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_REQUEST_ACCESS_RESOURCE) and sup == int(SU.suspicious) :
            return 1
        return 0
    
    def fss_command_anomaly_command_anomaly_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALARM_COMMAND_ANOMALY) sup == int(SU.suspicious):
            return 1
        return 0
            
    def fss_watched_watched_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_WATCHED_COUNTRY_LOGIN) and sup == int(SU.suspicious):
            return 1
        return 0
    
    def fss_command_anomaly_anomalous_host_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALARM_COMMAND_ANOMALY) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_illegal_activity_command_anomaly_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_illegal_activity_anomalous_host_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_new_authorized_key_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.new_authorized_keys) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fes_illegal_activity_change_credential_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_CHANGE_CREDENTIAL) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_failed_password_suspicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.login) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_read_host_configuration_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.read_host_configuration) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_sudo_bruteforce_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_SUDO_BRUTEFORCE) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_failed_password_bruteforce_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_FAILED_PASSWORD) and sup == int(SU.suspicious)):
        # if (e == int(SE.ALERT_FAILED_PASSWORD) and su == int(SU.malicious) and sa == int(SA.prepare_attack)):
            return 1
        return 0
    
    def fss_sensitive_uri_malware_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_MALWARE_HASH_REGISTRY_MATCH) sup == int(SU.suspicious):
            return 1
        return 0
    # two sensitive URIs
    def fss_sensitive_uri_malware_malicious(ep, sup, sap, e, su, sa):
        if is_sensitive_uri(e) and sup == int(SU.suspicious):
            return 1
        return 0
    
    def fss_disable_logging_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_DISABLE_LOGGING) and sup == int(SU.suspicious):
            return 1
        return 0
        
class MetricState():
    @staticmethod 
    def f1(m, E, su, sa, i):
        return 0
    
class MetricState2():
    @staticmethod 
    def f1(m, E, su, sa, i):
        if (m>=3) and su==int(SU.malicious):
            return 1
        return 0
    
class MetricFunction():
    @staticmethod 
    def f1(E, n):
        count = 0
        for i in xrange(1,n):
            if E[i] == int(SE.ALARM_COMMAND_ANOMALY):
                count += 1
        return count
    
def get_functions():
    classes = [UserEventState2, EventState2, StateState]
    f = []
    for c in classes:
        l = [method for name, method in c.__dict__.iteritems() if callable(method)]
        f.append(l)
        
    metric_tuple = [(MetricFunction.f1, [MetricState.f1])]
    return (f[0], f[1], f[2], metric_tuple)
