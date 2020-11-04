# AttackTagger

A Factor Graph based framework for preemptive intrusion detection.

See: https://publish.illinois.edu/science-of-security-lablet/files/2014/06/Preemptive-Intrusion-Detection-Theoretical-Framework-and-Real-World-Measurements.pdf
And: https://arxiv.org/pdf/1903.08826.pdf

# Testing AttackTagger

+ To test AttackTagger:
	make test_factg_all
It should take about an hour for 24 incidents (~5000 unique user accounts)

+ Plot result:
	make plot
Check the result in the fig directory

+ Analyze attack detection time for individual incident
   ipython notebook fg.ipynb

# Feeding Data

AttackTagger needs to train on data in order to be useful.  A training data set is provided but
it is recommended to build your own.  

Feeding data into AttackTagger from your systems can be accompished with Kafka or using our Zeek ZeroMQ
writer developed for AttackTagger:

https://github.com/ncsa/bro-zeromq-writer
