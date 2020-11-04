# AttackTagger

A Factor Graph based framework for preemptive intrusion detection.

See: https://publish.illinois.edu/science-of-security-lablet/files/2014/06/Preemptive-Intrusion-Detection-Theoretical-Framework-and-Real-World-Measurements.pdf
And: https://arxiv.org/pdf/1903.08826.pdf

# Development environment installation

Development environment for this project is contained in a VM for repeatability.
We use vagrant + virtualbox as our VM provider and run experiments on a Ubuntu VM.
Follow these steps to build your own development environment.

## Install vagrant + virtualbox 

Specific instructions depend on your host OS. 

## Clone the bootstrap repo and vagrant scripts in the factor-graph-analysis repo

1. Clone the bootstrap repo to your local directory.
The bootstrap repo is a set of scripts that setup basic development environment for Ubuntu,
including git, cmake, boost library, linux kernel headers, etc.
You should have read access to this repository if you've given us your public key.

	git clone git@bitbucket.org:pmcao/bootstrap.git

2. Clone the factor-graph-analysis to your local directory and change directory to the vagrant directory.

	git clone git@bitbucket.org:pmcao/factor-graph-analysis.git
	cd factor-graph-analysis/vagrant

+ Edit line "config.vm.synced_folder "../bootstrap", "/bootstrap" in the Vagrantfile, change "../bootstrap" to your local bootstrap repo (that you've cloned in previous step)
+ From vagrant directory, boot up a test vagrant box
	vagrant up 

It should now build the opengm library automatically. If you are seeing any error, ssh into the vagrant test box and inspect the build error
	vagrant ssh
	
# Experiment
+ Perform experiment (attack detection):
	make test_ncsa_all
It should take about an hour for 24 incidents (~5000 unique user accounts)

+ Plot result:
	make plot
Check the result in the fig directory

+ Analyze attack detection time for individual incident
   ipython notebook fg.ipynb
