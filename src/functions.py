#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-12-03 22:16:41 phuong>

import numpy as np
from tables import N_Events, N_UserStates, N_AttackStates, Events as SE, UserStates as SU, AttackStates as SA
from user_profile import User_Profile as UP

# state_transition = np.array([[0.8, 0.1, 0.1],
#                              [0.1, 0.45, 0.45],
#                                 [0.1, 0.1, 0.9]
#                          ])

class UserEventState():
    #No User Profile functions right now, but need to define something for it to compile
    def fues_placeholder(u, e, su, sa):
        return 0

#    def fues_disable_logging_malicious(u, e, su, sa):
#        if u.get_attribute(UP.previously_compromised) and e == int(SE.ALERT_DISABLE_LOGGING) and su == int(SU.malicious)  and sa == int(SA.clear_traces):
#            return 1
#        return 0
#    def fues_read_host_info_malicious(u, e, su, sa):
#        if u.get_attribute(UP.previously_compromised) and e == int(SE.read_host_configuration) and su == int(SU.suspicious)  and sa == int(SA.gather_information):
#            return 1
#        return 0
#    def fues_sudo_bruteforce(u, e, su, sa):
#        if u.get_attribute(UP.previously_compromised) and e == int(SE.ALERT_SUDO_BRUTEFORCE) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
#            return 1
#        return 0
    
class EventState():
    def fes_hosting_hidden_spam_malicious(e, su, sa):
        if e == int(SE.ALERT_HOSTING_HIDDEN_SPAM) and su == int(SU.malicious)   and sa == int(SA.execute_payload):
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

    def fes_sudo_bruteforce_suspicious(e, su, sa):
        if e == int(SE.ALERT_SUDO_BRUTEFORCE) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_1(e, su, sa):
        if e == int(SE.ALERT_HOST_JUMP) and su == int(SU.suspicious)  and sa == int(SA.spread):
            return 1
        return 0
    
    def fes_2(e, su, sa):
        if e == int(SE.ALERT_LOGIN_USING_EXPIRED_ACCOUNT) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_3(e, su, sa):
        if e == int(SE.ALERT_HIGH_RISK_DOMAIN) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_4(e, su, sa):
        if e == int(SE.ALERT_MALICIOUS_URL) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_5(e, su, sa):
        if e == int(SE.ALERT_HIGH_NETWORKFLOWS) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_6(e, su, sa):
        if e == int(SE.ALERT_INVALID_MIME_EXT) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_7(e, su, sa):
        if e == int(SE.ALERT_HOST_JUMP) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_8(e, su, sa):
        if e == int(SE.ALERT_HTTP_HOT_CLUSTER_CONN) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_9(e, su, sa):
        if e == int(SE.ALERT_WEIRD_URL_NAME) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_10(e, su, sa):
        if e == int(SE.ALERT_WEIRD_ACCOUNT_NAME) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_11(e, su, sa):
        if e == int(SE.ALERT_SSH_BRUTEFORCE) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_12(e, su, sa):
        if e == int(SE.ALERT_MISMATCH_FILE_HOST_DL) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_13(e, su, sa):
        if e == int(SE.ALERT_INTERNAL_ADDRESS_SCAN) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_14(e, su, sa):
        if e == int(SE.ALERT_NEW_HIDDEN_FILE_TMP_LOCATION) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_15(e, su, sa):
        if e == int(SE.ALERT_FAILED_PASSWORD) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_16(e, su, sa):
        if e == int(SE.ALERT_WEIRD_URL_NAME) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_17(e, su, sa):
        if e == int(SE.ALERT_WEIRD_DIRECTORY_NAME) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_18(e, su, sa):
        if e == int(SE.ALERT_KNOWN_BAD_DOWNLOADS) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fes_19(e, su, sa):
        if e == int(SE.ALERT_SSH_BRUTEFORCE) and su == int(SU.suspicious)  and sa == int(SA.prepare_attack):
            return 1
        return 0

    #new functions by Eric
    def fes_20(e, su, sa):
        if e == int(SE.ALERT_COMPILING_CODE) and su == int(SU.suspicious) and sa == int(SA.prepare_attack):
            return 1
        return 0

    def fes_21(e, su, sa):
        if e == int(SE.ALERT_PRIVILEGE_ESCALATION) and su == int(SU.suspicious) and sa == int(SA.escalate_privilege):
            return 1
        return 0

    def fes_21_2(e, su, sa):
        if e == int(SE.ALERT_PRIVILEGE_ESCALATION) and su == int(SU.malicious) and sa == int(SA.escalate_privilege):
            return 1
        return 0


    def fes_22(e, su, sa):
        if e == int(SE.ALERT_CHANGING_SYSTEM_FILES) and su == int(SU.suspicious) and sa == int(SA.establish_backdoor):
            return 1
        return 0

    def fes_23(e, su, sa):
        if e == int(SE.ALERT_ANOMALOUS_SSH_LOGIN) and su == int(SU.suspicious) and sa == int(SA.prepare_attack):
            return 1
        return 0

    def fes_24(e, su, sa):
        if e == int(SE.ALERT_DOWNLOAD_SENSITIVE_EXTENSION) and su == int(SU.suspicious) and sa == int(SA.prepare_attack):
            return 1
        return 0

    def fes_start_benign(e, su, sa):
        if e == int(SE.start) and su == int(SU.benign) and sa == int(SA.benign):
            return 3
        return 0

    def fes_25(e, su, sa):
        if e == int(SE.read_host_configuration) and su == int(SU.suspicious)  and sa == int(SA.gather_information):
            return 1
        return 0

    def fes_25_2(e, su, sa):
        if e == int(SE.read_host_configuration) and su == int(SU.benign)  and sa == int(SA.benign):
            return 1
        return 0

    def fes_26(e, su, sa):
        if e == int(SE.ALERT_NEW_USER) and su == int(SU.suspicious) and \
            sa == int(SA.prepare_attack):
            return 1
        return 0

    def fes_27(e, su, sa):
        if e == int(SE.ALERT_GET_LOGGEDIN_USERS) and su == int(SU.suspicious) and \
            sa == int(SA.prepare_attack):
            return 1
        return 0

    def fes_28(e, su, sa):
        if e == int(SE.login) and su == int(SU.benign) and \
            sa == int(SA.benign):
            return 1
        return 0
    
class StateState():

    def fss_1(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_HIGH_RISK_DOMAIN) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_2(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_MALICIOUS_URL) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.malicious)):
            return 1
        return 0
    
    def fss_3(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_MALICIOUS_URL) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0

    def fss_4(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_DOWNLOAD_SECURITY_TOOLS) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0

#    def fss_5(ep, sup, sap, e, su, sa):
    
    def fss_6(ep, sup, sap, e, su, sa):
        if (e == int(SE.WEIRD_IRC_SERVER) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_7(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_HOST_JUMP) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_7(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_HIGH_RISK_DOMAIN) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious) and ep ==
            int(SE.ALERT_PREVIOUSLY_COMPROMISED)):
            return 1
        return 0
    
    def fss_8(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_NEW_USER) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0

    def fss_9(ep, sup, sap, e, su, sa):
        if (e == int(SE.new_authorized_keys) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious)):
            return 1
        return 0
    
    def fss_10(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_MALICIOUS_URL) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious) and ep==int(SE.ALERT_WEIRD_URL_NAME)):
            return 1
        return 0
    
    def fss_11(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_MALICIOUS_URL) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious) and ep==int(SE.ALERT_HIGH_RISK_DOMAIN)):
            return 1
        return 0

    def fss_12(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_INVALID_MIME_EXT) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious) and ep==int(SE.ALERT_INVALID_MIME_EXT)):
            return 1
        return 0
    
    def fss_13(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_SSH_BRUTEFORCE) and su == int(SU.malicious) and \
            sa == int(SA.prepare_attack) and sup == int(SU.suspicious) and ep==int(SE.ALERT_MALICIOUS_URL)):
            return 1
        return 0
   
#    def fss_stop_malicious(ep, sup, sap, e, su, sa):
#        #return 0
#        if (e == int(SE.stop) and sup == int(SU.malicious) and sa == int(SA.execute_payload)):
#            return 1
#        return 0

    def fss_request_access_resource_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_REQUEST_ACCESS_RESOURCE) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0
    
    def fss_command_anomaly_command_anomaly_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALARM_COMMAND_ANOMALY) and ep == int(SE.ALARM_COMMAND_ANOMALY) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0
    
    def fss_watched_multiple_login_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_WATCHED_COUNTRY_LOGIN) and ep == int(SE.ALARM_MULTIPLE_LOGIN) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.prepare_attack)):
            return 1
        return 0
    
    def fss_watched_watched_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_WATCHED_COUNTRY_LOGIN) and ep == int(SE.ALERT_WATCHED_COUNTRY_LOGIN) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.prepare_attack)):
            return 1
        return 0
    
    def fss_command_anomaly_anomalous_host_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALARM_COMMAND_ANOMALY) and ep == int(SE.ALARM_ANOMALOUS_HOST) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0
    
    def fss_illegal_activity_command_anomaly_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and ep == int(SE.ALARM_COMMAND_ANOMALY) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0
    
    def fss_illegal_activity_anomalous_host_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and ep == int(SE.ALARM_ANOMALOUS_HOST) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0

    
    def fss_illegal_activity_disable_logging(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and ep == int(SE.ALERT_DISABLE_LOGGING) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0
    
    def fss_new_authorized_key_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.new_authorized_keys) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.execute_payload)):
            return 1
        return 0
    
    def fes_illegal_activity_change_credential_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_CHANGE_CREDENTIAL) and ep == int(SE.ALERT_ILLEGAL_USER_ACTIVITY) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.compromised)):
            return 1
        return 0
    
    def fss_failed_password_suspicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.login) and ep == int(SE.ALERT_FAILED_PASSWORD) and su == int(SU.suspicious) and sup == int(SU.suspicious) and sa == int(SA.prepare_attack)):
            return 1
        return 0
    
#    def fss_read_host_configuration_malicious(ep, sup, sap, e, su, sa):
#        if (e == int(SE.read_host_configuration) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.gather_information)):
#            return 1
#        return 0
    
    def fss_read_host_configuration_suspicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.read_host_configuration) and sup == int(SU.benign) and su == int(SU.suspicious) and sa == int(SA.gather_information)):
            return 1
        return 0

    def fss_sudo_bruteforce_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_SUDO_BRUTEFORCE) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.prepare_attack)):
            return 1
        return 0
    
    def fss_failed_password_bruteforce_malicious(ep, sup, sap, e, su, sa):
        if (e == int(SE.ALERT_FAILED_PASSWORD) and ep == int(SE.ALERT_SUDO_BRUTEFORCE) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.prepare_attack)):
            return 1
        return 0
    
    def fss_sensitive_uri_malware_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_MALWARE_HASH_REGISTRY_MATCH) and ep == int(SE.ALERT_MALICIOUS_URL) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.prepare_attack):
            return 1
        return 0

    # two sensitive URIs
    def fss_sensitive_uri_malware_malicious(ep, sup, sap, e, su, sa):
        if ep == int(SE.ALERT_MALICIOUS_URL) and e == int(SE.ALERT_MALICIOUS_URL) and sup == int(SU.suspicious) and su == int(SU.malicious) and sa == int(SA.prepare_attack):
            return 1
        return 0
    
    def fss_disable_logging_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_DISABLE_LOGGING) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0
    
    def fss_disable_logging_anomalous_host_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_DISABLE_LOGGING) and su == int(SU.malicious) and ep == int(SE.ALARM_ANOMALOUS_HOST):
            return 1
        return 0
    
    # def fss_transition(ep, sup, sap, e, su, sa):
    #     if (ep == int(SE.start) or e == int(SE.stop)):
    #         return 0
    #     return 0
    #     return state_transition[int(sup), int(su)]

    def fss_1a(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_NEW_SERVICE) and ep == int(SE.ALERT_NEW_SERVICE) \
           and su == int(SU.suspicious):
            return 1
        return 0
    
    def fss_1b(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_NEW_SERVICE) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0

    #new functions by Eric
    def fss_compiling_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_COMPILING_CODE) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0

    def fss_privilege_escalation_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_PRIVILEGE_ESCALATION) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0

    def fss_privilege_escalation_suspicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_PRIVILEGE_ESCALATION) and su == int(SU.suspicious) and sup == int(SU.benign):
            return 1
        return 0

    def fss_changing_system_files_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_CHANGING_SYSTEM_FILES) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0
        
    def fss_anomalous_ssh_login_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_ANOMALOUS_SSH_LOGIN) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0
        
    def fss_download_sensitive_extension_malicious(ep, sup, sap, e, su, sa):
        if e == int(SE.ALERT_DOWNLOAD_SENSITIVE_EXTENSION) and su == int(SU.malicious) and sup == int(SU.suspicious):
            return 1
        return 0

class MetricState():
    @staticmethod 
    def f1(m, E, su, sa, i):
        return 0
#        if (m>=3) and su==int(SU.malicious):
#            return 1
#        return 0
    
class MetricFunction():
    @staticmethod 
    def f1(E, n):
        return 0
#        count = 0
#        for i in xrange(1,n):
#            if E[i] == int(SE.ALARM_COMMAND_ANOMALY):
#                count += 1
#        return count
    
def get_functions():
    classes = [UserEventState, EventState, StateState]
    f = []
    for c in classes:
        l = [method for name, method in c.__dict__.iteritems() if callable(method)]
        f.append(l)
        
    metric_tuple = [(MetricFunction.f1, [MetricState.f1])]
    return (f[0], f[1], f[2], metric_tuple)
