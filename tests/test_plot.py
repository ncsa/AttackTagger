#!/usr/bin/env python
# -*- compile-command: "cd .. && make test" -*-
# Time-stamp: <2014-02-24 15:37:54 phuong>

import sys, os
sys.path.append('src')

import pandas as pd
import plot

def test_plot_from_result():
   df = pd.read_pickle("result/ncsa_all.pickle")
   plot.plot_result(df)
   
   #df = pd.read_pickle("result/ncsa_variation.pickle")
   #plot.plot_variation(df)
