# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pandas as pd
from os.path import expanduser

import os
import json
import threading
import time
import logging as log 
import io

log.basicConfig(level=log.DEBUG,)   

KAFKA_TOPIC="auditd"

from functools import wraps
from kafka import KafkaConsumer



TEST_INCIDENT_PATH = expanduser('../incidents/test')
TRAIN_INCIDENT_PATH = expanduser('../incidents/train')

train_incident_list = {
    "20080907.timeline":["amorris", "nurmi", "drlead"],
    "20080117-01.timeline": ["globus"],
    "20080209-01.timeline": ["u"],
    "20080213-02.timeline": ["pkirack1"],
    "20080222-01.timeline": ["user42"],
    "20080304-01.timeline": [],
    "20080325-01.timeline": ["joseph"],
    "20080410-01.timeline": ["user"],
    "20080421-01.timeline": ["user"],
    "20080510-01.timeline": ["user"],
    "20080519-01.timeline": ["user"],
    "20080527-01.timeline": ["u"],
    "20080530-01.timeline": ["u"],
    "20080616-01.timeline": ["u"],
    "20080619-01.timeline": ["u"],
    "20080619-02.timeline": ["u"],
    "20080712.timeline":["smisra"],
    "20080715-02.timeline": ["u"],
    "20080717-01.timeline": ["u"],
    "20080726-01.timeline": ["u"],
    "20080729-01.timeline": ["u"],
    "20080816-01.timeline": ["u"],
    "20080819-01.timeline": ["u"],
    "20080819-02.timeline": ["u"],
    "20080830-01.timeline": ["u"],
    "20080907-01.timeline": ["u"],
    "20080923-01.timeline": ["u"],
    "20081006-01.timeline": ["u"],
    "20081030-01.timeline": ["u"],
    "20081103-01.timeline": ["u"],
    "20081107-01.timeline": ["u"],
    "20081130.timeline":["cdetar", "rplante", "fpierfed", "daues"],
    "20090209.timeline":["wolfson"],
    "20090115-01.timeline": ["u"],
    "20090221-01.timeline": ["u"],
    "20090318-01.timeline": ["u"],
    "20090402-01.timeline": ["u"],
    "20090416-01.timeline": ["u"],
    "20090421-01.timeline": ["u"],
    "20090422-01.timeline": ["u"],
    "20090514-01.timeline": ["u"],
    "20090516-01.timeline": ["u"],
    "20090528-01.timeline": ["u"],
    "20090714-01.timeline": ["u"],
    "20090813.timeline":["wolfson", "boxu"],
    "20090818.timeline":["mklocek2"],
    "20090819.timeline": ["kmilner", "tera3d"],
    "20090831-01.timeline": [],
    "20090908.timeline": ["pakshing"],
    "20090916-01.timeline": [],
    "20090930-01.timeline": [],
    "20091006-01.timeline": [],
}

test_incident_list = {
    # "20090209.timeline":["wolfson"],
    # "20081130.timeline":["cdetar", "rplante", "fpierfed", "daues"],
    # "20080907.timeline":["amorris", "nurmi", "drlead"],
    # "20080712.timeline":["smisra"],
    # "20080619.timeline":["smisra"],
    # "20090819.timeline": ["kmilner", "tera3d"],
    # "20090908.timeline": ["pakshing"],
    # "20090818.timeline":["mklocek2"],
    # "20090813.timeline":["wolfson", "boxu"],
    # "20100513.timeline":["amritkar"],
    # "20100416.timeline":["ancher"],
    # "20101029.timeline":["bkzierv"],
    # "20120509.timeline":["10.10.222.232"],
    # "20120513.timeline":["10.10.226.222"],
    # "20120702.timeline":["10.10.249.13"],
    # "20120830.timeline":["10.10.249.76"],
    # "20121128.timeline":["10.10.249.76"],
    # "20121206.timeline":["10.10.249.13"],
    # "20121004.timeline":["10.10.225.189"],
    # "20121102.timeline":["10.10.227.100"],
    # "20121102-2.timeline":["10.10.242.230"],
    # "20121226.timeline":["10.10.225.131"],
    # "20130207-2.timeline":["10.10.220.52"],
    # "20130207.timeline":["prothwin7.ncsa.uiuc.edu"],
    # "20130221.timeline":["cristina"],
    #
    # "20110317-01.timeline": ["u"],
    # 
    # testing start
    #"20100107-01.timeline": [],
    #"20100116-01.timeline": ["u"],
    #"20100116-02.timeline": [],
    #"20100307-01.timeline": ["u"],
    #"20100307-02.timeline": ["u"],
    #"20100319-01.timeline": ["u"],
    #"20100325-01.timeline": ["u"],
    #"20100325-02.timeline": [],
    #"20100331-01.timeline": ["u"],
    #"20100408-01.timeline": ["u"],
    #"20100413-01.timeline": ["u"],
    #"20100415-01.timeline": ["u"],
    #"20100416.timeline": ["ancher"],
    "20100513.timeline": ["amritkar"]
    #"20100513-01.timeline": ["u"],
    #"20100513-02.timeline": ["u"],
    #"20100612-01.timeline": ["u"],
    #"20100614-01.timeline": ["u"],
    #"20100621-01.timeline": ["u"],
    #"20100924-01.timeline": ["u"],
    #"20100926-01.timeline": ["u"],
    #"20101006-01.timeline": ["u"],
    #"20101007-01.timeline": ["u"],
    #"20101025-01.timeline": ["u"],
    #"20101025-02.timeline": ["u"],
    #"20101029.timeline": ["bkzierv"],
    #"20101103-01.timeline": ["u"],
    #"20101119-01.timeline": ["u"],
    #"20101120-01.timeline": ["u"],
    #"20101129-01.timeline": ["u"],
    #"20101224-01.timeline": ["u"],
    #"20101226-01.timeline": ["u"],
    #"20110102-01.timeline": ["u"],
    #"20110106-01.timeline": ["u"],
    #"20110110-01.timeline": ["u"],
    #"20110127-01.timeline": ["u"],
    #"20110203-01.timeline": ["u"],
    #"20110207-01.timeline": ["u"],
    #"20110207-02.timeline": ["u"],
    #"20110207-03.timeline": ["u"],
    #"20110212-01.timeline": ["u"],
    #"20110226-01.timeline": ["u"],
    #"20110308-01.timeline": ["u"],
    #"20110317-01.timeline": ["u"],
    #"20110606.timeline": ["u"],
    #"20110613.timeline": ["u"],
    #"20110617.timeline": ["u"],
    #"20110624.timeline": ["u"],
    #"20120509.timeline": ["10.10.222.232"],
    #"20120513.timeline": ["10.10.226.222"],
    #"20120702.timeline": ["10.10.249.13"],
    #"20120830.timeline": ["10.10.249.76"],
    #"20121004.timeline": ["10.10.225.189"],
    #"20121102.timeline":["10.10.227.100"],
    #"20121102-2.timeline":["10.10.242.230"],
    #"20121128.timeline":["10.10.249.76"],
    #"20121206.timeline":["10.10.249.13"],
    #"20121226.timeline":["10.10.225.131"],
    #"20130207-2.timeline":["10.10.220.52"],
    #"20130207.timeline":["prothwin7.ncsa.uiuc.edu"],
    #"20130221.timeline":["cristina"],
    #"20130411.timeline":["u"],
    #"20130506.timeline":["u"],
    #"20130523.timeline":["u"],
    #"20130801.timeline":["u"],
}

def add_start_stop_and_timestamp(df):
    #df.index = pd.to_datetime((df.index.values*1e9).astype(int)) # https://github.com/pydata/pandas/issues/3757
    #return df


    # import table.table as table
    #df_start_stop = pd.concat([df.head(1), df, df.tail(1)])
    df_start_stop = pd.concat([df.head(1), df])

    # TODO: this is not really efficient
    df_head = df_start_stop.head(1)
    df_head.event = 'start'
    df_head.user_state = 'benign'
    df_head.attack_state='benign'

    df_start_stop = pd.concat([df_head, df])
    
    #df_tail= df_start_stop.tail(1)
    #df_tail.event= 'stop'
    #df_tail.user_state = 'stop'
    #df_tail.attack_state='stop'

    # hack
    
    # convert epoch to datetime object in pandas
    df_start_stop.index = pd.to_datetime((df_start_stop.index.values*1e9).astype(int)) # https://github.com/pydata/pandas/issues/3757
    
    return df_start_stop


class KafkaConsume():
    def __init__(self):

        kafka = None
        consumer = None
    
        for attempt in xrange(0,3):
            try:
                consumer = KafkaConsumer(KAFKA_TOPIC,
                                         auto_offset_reset='earliest',
                                         enable_auto_commit=False,
                                         bootstrap_servers=['localhost:9092'])
            except:
                log.error("retrying kafka connection")
                time.sleep(1)
                continue
            break   
    
        if (consumer is None):
                log.critical("can't connect to kafka")
                print "can't connect to kafka"
                return
        self.consumer = consumer
        
        
    def get_data(self):
        consumer = self.consumer
        data = ''
        num_msg = 0
        while num_msg == 0:
          for message in consumer.get_messages(count=20,block=True,timeout=1):
              data += message.message.value + '\n'
              num_msg += 1
              #print message.message.value
          
        return data

    def close(self):
        self.consumer.close()
    
    def load_ncsa_kafka(self):
        """
        Return a list of tuples (df, compromised user)
        """

        drop_list = []
        data = self.get_data()
        #print data 
        df = pd.read_csv(io.BytesIO(data),
                           index_col='timestamp',
                           #names=['timestamp', 'user', 'event', 'su', 'sa', 'recv-ts'],
                           names=['timestamp', 'user', 'event', 'su', 'sa'],
                           skipinitialspace=True)
        #for index, row in enumerate(df.values):
        #    print 'index\n', index
        #    print 'df[index]\n', df.iloc[index]['event']
        #    if index > 0:
        #        if df.iloc[index]['event'] == df.iloc[index - 1]['event']:
        #            drop_list.append(index)
        #    print '*****'
        #df = df[df.index != drop_list]
        #print 'drop_list\n', drop_list
        #print 'df\n', df 

        return df
    
    
    
    #def load_ncsa_kafka():
    #    """
    #    Return a list of tuples (df, compromised user)
    #    """
    #    l = []
    #    data = kafka_worker()
    #    print data 
    #    print '\n\n\n\n\n'
    #    df = pd.read_csv(io.BytesIO(data),
    #                       index_col='timestamp',
    #                       names=['timestamp', 'user', 'event', 'su', 'sa'],
    #                       #names=['timestamp', 'user', 'event'],
    #                       skipinitialspace=True)
    #    #compromised = ["amritkar"]
    #    #l.append(("20100513.timeline", df, compromised))
    #    compromised = ["amritkar"]
    #    l.append(("realtime", df, compromised))
    #    return l

def load_ncsa():
    """
    Return a list of tuples (df, compromised user)
    """
    l = []
    for incident in test_incident_list:
        incident_path = '{}/{}'.format(TEST_INCIDENT_PATH, incident)
        df = pd.read_csv(incident_path,
                           index_col='timestamp',
                           names=['timestamp', 'user', 'event', 'su', 'sa'],
                           skipinitialspace=True)
        compromised = test_incident_list[incident]
        l.append((incident, df, compromised))
    return l


def load_ncsa_train():
    """
    Return a list of tuples (df, compromised user)
    """
    l = []
    for incident in train_incident_list:
        incident_path = '{}/{}'.format(TRAIN_INCIDENT_PATH, incident)
        df = pd.read_csv(incident_path,
                           index_col='timestamp',
                           names=['timestamp', 'user', 'event', 'su', 'sa'],
                           skipinitialspace=True)
        compromised = train_incident_list[incident]
        l.append((incident, df, compromised))
    return l
