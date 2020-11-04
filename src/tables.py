from flufl.enum import IntEnum

def _enumiter():
    start = 0
    while True:
        yield start
        start = start + 1

Events_ = ['start', 'stop', 'login', 'download',
           'download_sensitive', 'compile','delete',
           'read_host_configuration',
           'read_user_list',
           'ssh_connect',
           'read_documents',
           'ALERT_KNOWN_BAD_DOWNLOADS',
           'new_authorized_keys',
           'ALERT_PREVIOUSLY_COMPROMISED',
           'ALERT_INVALID_MIME_EXT',
           'SSH_BAD_PROTOCOL_VERSION',
           'ALERT_HOSTING_HIDDEN_SPAM',
           'ALERT_HOSTING_ADS', # 20110606
           'ALERT_SENSITIVE_HTTP_URI',
           'ALERT_OPEN_PROXY',
           'ALERT_MISMATCH_FILE_HOST_DL', # download exe on ubuntu
           'ALERT_INTERNAL_ADDRESS_SCAN', 'ALARM_COMMAND_ANOMALY',
           'ALERT_ILLEGAL_IP_ACTIVITY', 'ALERT_ILLEGAL_USER_ACTIVITY',
           'ALERT_OLD_INACTIVE_ACCOUNT',
           'ALARM_MULTIPLE_LOGIN',
           'ALARM_ANOMALOUS_HOST', 'ALERT_FAILED_PASSWORD',
           'ALERT_SPAM_EMAIL_CLICK',
           'ALERT_DEGRADE_PERFORMANCE',
           'ALERT_HOST_JUMP', 
           'ALERT_LOGIN_USING_EXPIRED_ACCOUNT',
           'ALERT_SENSITIVE_FTP_URI',
           'ALERT_DISABLE_LOGGING',
           'ALERT_HTTP_HOT_CLUSTER_CONN',
           'ALERT_WATCHED_COUNTRY_LOGIN',
           'ALERT_ROOTKIT_PHALANX',
           'ALERT_CORRELATED',
           'ALERT_REQUEST_ACCESS_RESOURCE',
           'ALERT_SUDO_BRUTEFORCE',
           'ALERT_SSH_BRUTEFORCE',
           'ALERT_CHANGE_CREDENTIAL',
           'ALERT_MALWARE_HASH_REGISTRY_MATCH',
           'ALERT_NEW_IRC_CONNECTION',
           'ALERT_NEW_IRC_DOWNLOAD',
           'ALERT_NEW_HIDDEN_FILE_TMP_LOCATION', # /var/tmp
           'ALERT_INSTALL_BOT',
           'ALERT_NEW_SYSADMIN_ACCOUNT',
           'ALARM_COLLECT_SYSTEM_INFO',
           'ALERT_FOREIGN_CONVERSATION', # 080923, romainan
           'ALERT_REPLACE_SYSTEM_SERVICE',
           'ALARM_COLLECT_SHELL_HISTORY',
           'ALERT_VIEW_PASSWORD_FILE',
           'ALARM_WEAK_PASSWORD_LOGIN',
           'ALERT_HIGH_NETWORKFLOWS',
           'ALERT_SUDO_ESCALATE_PRIV',
           'ALERT_WEIRD_DIRECTORY_NAME',
           'ALERT_WEIRD_URL_NAME', # contains number, strings, l33t style, sploit
           'ALERT_WEIRD_ACCOUNT_NAME',
           'ALERT_HIGH_RISK_DOMAIN', # dynamic dns
           'ALERT_MALICIOUS_URL', # contain c99 shell, eggdrop
           'ALERT_MALICIOUS_FILE_NAME',
           'ALERT_NEW_SENSITIVE_CONNECTION', # connect to .de, .cn, .dyndns hosts
           'ALERT_DOS_SYNFLOOD',
           'ALERT_DOS',
           'ALERT_NEW_HTTP_FTP_SERVER', # serving warez
           'ALERT_NEW_SERVICE', # serving warez
           'ALERT_BOT_CC', # command and control
           'ALERT_DISABLE_HISTORY',
           'ALERT_CLEAR_HISTORY',
           'ALERT_HOSTING_HIDDEN_SPAM',
           'ALERT_ROOT_LOGIN',
           # start backward from 2011
           # 'NEW_UNKNOWN_SERVICE',
           'HTTP_UNUSUAL_PORT', # different from 80/8080
           'FTP_UNUSUAL_USERNAME', # h4x0r username
           'FTP_UNUSUAL_FILE', # h4x0r file
           'WEIRD_IRC_SERVER', # undernet
           'ALERT_NEW_USER',
           'ALERT_PORN_DOWNLOAD',

           #New events
           'ALERT_DOWNLOAD_SECURITY_TOOLS',
           'ALERT_ANOMALOUS_SSH_LOGIN',
           'ALERT_DOWNLOAD_SENSITIVE_EXTENSION',
           'ALERT_COMPILING_CODE',
           'ALERT_PRIVILEGE_ESCALATION',
           'ALERT_CHANGING_SYSTEM_FILES',
           'ALERT_GET_LOGGEDIN_USERS',
]

Events_NCSA = [
           'ALERT_KNOWN_BAD_DOWNLOADS',
           'ALERT_HOSTING_HIDDEN_SPAM',
           'ALERT_SENSITIVE_HTTP_URI',
           'ALERT_INTERNAL_ADDRESS_SCAN', 'ALARM_COMMAND_ANOMALY',
           'ALERT_ILLEGAL_IP_ACTIVITY', 'ALERT_ILLEGAL_USER_ACTIVITY',
           'ALARM_MULTIPLE_LOGIN', 'ALARM_ANOMALOUS_HOST',
           'ALERT_SENSITIVE_FTP_URI',
           'ALERT_MALWARE_HASH_REGISTRY_MATCH',
           'ALERT_NEW_IRC_CONNECTION',
]

User_States_ = ['benign', 'suspicious', 'malicious']
Attack_States_ = ['benign', 'gather_information', 'prepare_compromise', 'compromised', 'prepare_attack', 'escalate_privilege', 'establish_backdoor', 'spread', 'execute_payload', 'clear_traces']

Events = IntEnum('Events', zip(Events_, _enumiter()))
UserStates = IntEnum('User_States', zip(User_States_, _enumiter()))
AttackStates = IntEnum('Attack_States', zip(Attack_States_, _enumiter()))

N_Events = len(Events_)
N_UserStates = len(User_States_)
N_AttackStates= len(Attack_States_)
