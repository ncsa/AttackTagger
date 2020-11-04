# Bootstrap

This repo contains scripts to bootstrap dev env on Ubuntu Linux and Mac OSX

# Installation

On a fresh install of Ubuntu or Mac, clone this repository, then type the following commands:

Mac
	% ./install.sh -bm

Ubuntu
	% sudo ./install.sh -bl

To build Vagrant or Docker image, then type the following commands

Vagrant
	% vagrant up

Docker
	% docker build -t bootstrap .
or
	% make docker_build
	

# Features

## Linux
+ Dev packages at bootstrap/linux/
+ Python3 and packages at bootstrap/common/requirements.txt

## Mac
+ Brew casks at bootstrap/darwin/

## Both Mac and Linux
+ Python3 and packages at bootstrap/common/requirements.txt

# Under the hood

See install.sh

First it bootstraps dev env and libraries for each type of OS,  $BOOTSTRAP_OS_DIR/bootstrap.sh.
Second, it installs common files such as Python requirements files, $BOOTSTRAP_COMMON_DIR/bootstrap.sh
Finally, it runs Ansible playbook for each type of OS, for OSX it installs casks.

## Problems
+ Linux kernel header package does not work in Docker

## Dotfiles
+ Mac: /Users/<username>
+ Ubuntu: /home/<username>
+ Docker: /root
