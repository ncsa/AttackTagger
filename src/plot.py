#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import rc
from os.path import expanduser
from pandas import DataFrame
from collections import defaultdict

BASE_PATH = expanduser('./fig')

def plot_detection_timeliness_hist_1hr(X):
   plt.clf()
   t = np.arange(min(X), max(X)+1, 60) # 6 hours period
   plt.hist(X)
   plt.ylabel(r'frequency')
   plt.xlabel(r'time (minute)')
   plt.xticks(t)
   # plt.title(r"\TeX\ is Number "
   #                r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",
   #                fontsize=16, color='gray')
   plt.tight_layout()
   fig = plt.gcf()
   fig.savefig('{}/{}'.format(BASE_PATH,
                              'graph_detection_timeliness_hist_1hr.pdf'))

def plot_detection_timeliness_hist(X):
   X /= 3600
   plt.clf()
   t = np.arange(min(X), max(X)+1, 12) # 6 hours period
   plt.hist(X)
   plt.ylabel(r'frequency')
   plt.xlabel(r'time (hr)')
   plt.xticks(t)
   # plt.title(r"\TeX\ is Number "
   #                r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",
   #                fontsize=16, color='gray')
   plt.tight_layout()
   fig = plt.gcf()
   fig.savefig('{}/{}'.format(BASE_PATH,
                              'graph_detection_timeliness_hist.pdf'))

def plot_detection_timeliness(X):
   X /= 3600
   plt.clf()
   t = np.arange(min(X), max(X)+1, 12) # 6 hours period
   X_ = np.sort(X)
   X_ /= X_.sum()
   CY = np.cumsum(X_)
   plt.plot(np.sort(X),CY,'r')
   plt.ylabel(r'empirical cdf')
   plt.xlabel(r'time (hr)')
   plt.xticks(t)
   # plt.title(r"\TeX\ is Number "
   #                r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",
   #                fontsize=16, color='gray')
   plt.tight_layout()
   fig = plt.gcf()
   fig.savefig('{}/{}'.format(BASE_PATH,
                              'graph_detection_timeliness.pdf'))

def plot_detection_accuracy(X):
   plt.clf()
   df2 = DataFrame(X, columns=['detected', 'not detected'])
   ax = df2.plot(kind='bar', stacked=True, color='k');
   ax.set_ylabel('# compromised user')
   ax.set_xlabel('incident id')
   plt.tight_layout()
   plt.yticks([1,2,3,4])
   for container in ax.containers:
        if container.get_label() == 'detected':
            plt.setp(container, color='0.75')
        else:
            plt.setp(container, color='0')
   # ax.legend()
   plt.legend(loc='upper left')
   fig = plt.gcf()
   fig.savefig('{}/{}'.format(BASE_PATH,
                               'graph_detection_accuracy.pdf'))
    

# def plot_sequencing_accuracy(X, idx, name):
#    """
#    length of the array must equal length of the idx
#    """
#    df2 = DataFrame(X, index=idx,columns=['correct', 'incorrect'])
#    df2.plot(kind='bar', stacked=True)

#    fig = plt.gcf()
#    fig.savefig('{}/{}'.format(BASE_PATH,
#                                'graph_sequencing_accuracy_%s.pdf' % name))

    
def plot_sequencing_accuracy(conf_arr, idx, name, fontsize=12):
    norm_conf = []
    for i in conf_arr:
            a = 0
            tmp_arr = []
            a = sum(i,0)
            for j in i:
                    tmp_arr.append(float(j)/float(a))
            norm_conf.append(tmp_arr)
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.xaxis.tick_top()
    [ax.grid(False) for ax in fig.axes]
    res = ax.imshow(np.array(norm_conf), origin='upper', cmap=plt.cm.jet_r, interpolation='nearest')
    for i, cas in enumerate(conf_arr):
        for j, c in enumerate(cas):
            plt.text(i, j, c, horizontalalignment='center', verticalalignment='center',fontsize=fontsize, color='white')
    cb = fig.colorbar(res)
    width = len(conf_arr)
    height = len(conf_arr[0])
    plt.xticks(range(width), idx[:width])
    plt.yticks(range(height), idx[:height])
    fig.savefig('{}/{}'.format(BASE_PATH,
                               'graph_sequencing_accuracy_%s.pdf' % name))

def plot_detection_accuracy_helper(result):
    # detection accuracy
    d = defaultdict()
    for row in result.iterrows():
       r = row[1]
       if (d.has_key(r.incident) == False):
          d[r.incident] = defaultdict()
          
       if (d[r.incident].has_key('hit') == False):
          d[r.incident]['hit'] = 0
          
       if (d[r.incident].has_key('miss') == False):
          d[r.incident]['miss'] = 0

       if r.accuracy == 1:
          d[r.incident]['hit'] += 1
       else:
          d[r.incident]['miss'] += 1
          
    detection_accuracy = []
    for incident in d:
       detection_accuracy.append([d[incident]['hit'], d[incident]['miss']])
    
    plot_detection_accuracy(np.array(detection_accuracy, dtype=int))
    
def plot_detection_timeliness_helper(result):
    # detection accuracy
   plot_detection_timeliness(np.array(result.detection_timeliness, dtype=float))
   # print zip(result.num_event, result.labeling_time)
   # print result.detection_timeliness, result.preemption_timeliness, result.attack_duration
    
def plot_preemption_cdf(df):
    df_filtered = df[df['accuracy'] == 1]
    df = df_filtered
    # raise SystemExit
   
    plt.clf()
    
    X = np.array([x/3600 if x >=0 and x/3600 < 48 else 48 for x in df.preemption_timeliness], dtype=float)
    try:
      plt.hist(X, cumulative=True, label='preemption', color='0')
    except ValueError:
      pass
    
    plt.ylim(14,24)
    plt.xlabel('preemption timeliness (hr)')
    plt.ylabel('cumulative count')
    plt.legend(loc='upper left')
    fig = plt.gcf()
    [ax.grid(False) for ax in fig.axes]
    fig.savefig('{}/{}'.format(BASE_PATH,
                               'graph_preemption_cdf.pdf'))
    
def plot_detection_cdf(df):
    df_filtered = df[df['accuracy'] == 1]
    df = df_filtered
    # raise SystemExit
   
    plt.clf()
    
    X = np.array([x/3600 if x >=0 and x/3600 < 48 else 48 for x in df.detection_timeliness], dtype=float)
    try:
      ax = plt.hist(X, cumulative=True, label='detection', color='0')
    except ValueError:
      pass
    
    plt.ylim(14,24)
    plt.xlabel('detection timeliness (hr)')
    plt.ylabel('cumulative count')
    plt.legend(loc='upper left')
    fig = plt.gcf()
    [ax.grid(False) for ax in fig.axes]
    fig.savefig('{}/{}'.format(BASE_PATH,
                               'graph_detection_cdf.pdf'))
    
def plot_detection_and_preemption_timeline(df):
    plt.clf()
    timeline = []
    for row in df.iterrows():
        r = row[1]
        if r.detection_timeliness!= -1:
            sum = r.detection_timeliness + r.preemption_timeliness
            if (sum != 0):
                ratio = r.detection_timeliness/sum
                timeline.append(ratio)
            else:
                timeline.append(1)

    fig, ax = plt.subplots()

    count = 0
    for user in timeline:
       if count == 0:
          plt.bar(left=0, width=user, height=0.8, bottom=count, color='0.75', label='not_malicious')
          plt.bar(left=user, width=1.02-user, height=0.8, bottom=count, color='0', label='malicious')
       else:
          plt.bar(left=0, width=user, height=0.8, bottom=count, color='0.75')
          plt.bar(left=user, width=1.02-user, height=0.8, bottom=count, color='0')
       count = count + 1
    ax.set_yticks(np.arange(0, len(timeline), 5), minor=False)
    ax.set_xticks(np.arange(0, 2), minor=False)
    ax.grid(False)
    
    # for container in ax.containers:
    #      if container.get_label() == 'malicious':
    #          plt.setp(container, hatch='xxx')
    #      else:
    #          plt.setp(container, hatch='ooo')
    # ax.legend()
    
    plt.axis([0,1.03,-1,len(timeline)])
    plt.xlabel('time (normalized)')
    plt.ylabel('user id')
    plt.legend(loc='upper left')
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig('{}/{}'.format(BASE_PATH,
                               'graph_detection_and_preemption_timeline.pdf'))
    
def plot_labeling_time(df):
    plt.clf()
    plt.scatter(df.num_event, df.labeling_time)
    pars= np.polyfit(df.num_event, df.labeling_time, 1)
    fitted_y = np.polyval(pars,df.num_event)
    plt.plot(df.num_event, fitted_y, 'r--')
    plt.xlabel('number of events')
    plt.ylabel('labeling time (s)')

    # t = np.array(df.num_event)
    # xn = np.array(df.labeling_time)
    # #Linear regressison -polyfit - polyfit can be used other orders polys
    # (ar,br)=polyfit(t,xn,1)
    # xr=polyval([ar,br],t)
    # #compute the mean square error

    # t = (xr-xn)**2
    # n = len(t)
    # err=sqrt(t.sum()/n)
    # print len(t), err


    # print df.accuracy
    
    fig = plt.gcf()
    fig.savefig('{}/{}'.format(BASE_PATH,
                               'graph_labeling_time.pdf'))
    
def plot_result(result):
    """
    result: list of incident_results
    [
    (user, accuraty (0 - not detected or 1 - detected), detection timeliness in second
    ]
    """
    plot_detection_accuracy_helper(result)
    plot_detection_cdf(result)
    plot_preemption_cdf(result)
    plot_detection_and_preemption_timeline(result)
    plot_labeling_time(result)

    # # detection timeliness
    # detection_timeliness = []
    # for incident in result:
    #    for incident_result in incident:
    #       timeliness = incident_result[2]
    #       if (timeliness > 0):
    #         detection_timeliness.append(timeliness) # timeliness

    # plot_detection_timeliness(np.array(detection_timeliness, dtype=float))
    # plot_detection_timeliness_hist(np.array(detection_timeliness, dtype=float))
    # plot_detection_timeliness_hist_1hr(np.array([ x < 3600 for x in detection_timeliness], dtype=float))

def plot_variation(df):
  plt.clf()
  plt.hist(df.accuracy_list[0], color='k')
  plt.xlabel('detect at event number')
  plt.ylabel('count')
  plt.xticks([3, 4, 5, 6]) # TODO FIX THIS
  fig = plt.gcf()
  fig.savefig('{}/{}'.format(BASE_PATH,
                           'graph_variation.pdf'))
