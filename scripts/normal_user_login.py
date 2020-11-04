import os
import sys

ROOTDIR = '/tmp'
OUTDIR= '/tmp'

def process_file(fname):
    import csv
    from collections import defaultdict
    d = defaultdict()
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            d[row[3]] = row[0]
    return d

def output_timeline(d):
    timeline = ''
    for k,v in dict(d).iteritems():
        timeline += '{},{},{}\n'.format(v, k, 'login')
    return timeline

def write_timeline(f, d):
    fo = open(f, "w")
    fo.write(d)
    fo.close()

for folder, subs, files in os.walk(ROOTDIR):
    for filename in files:
        if filename.startswith('fulllog') and filename.endswith('timeline'):
            fullpath = os.path.join(folder, filename)
            d = process_file(fullpath)
            timeline = output_timeline(d)
            # write to file
            new_file = os.path.join(OUTDIR, filename)
            write_timeline(new_file, timeline)
            # fo = open("foo.txt", "wb")
            # fo.write( "Python is a great language.\nYeah its great!!\n");

            # # Close opend file
            # fo.close()

