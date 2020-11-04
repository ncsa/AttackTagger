#!/bin/bash

#must run script as root


if hash lsb_release 2>/dev/null; then
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
else
    yum install -y redhat-lsb-core
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
fi



##################
#Ubuntu Install
##################
if [ $OS == 'Ubuntu' ]; then
  echo "Running Ubuntu Install";

	## update apt-get
	apt-get update && apt-get upgrade -y
	
	# utils
	apt-get install -y wget git software-properties-common vim
	
	apt-get install -y openjdk-7-jdk
	
	# basic dev packages
	apt-get install -y autoconf libtool pkg-config flex bison autogen cmake
	apt-get install -y build-essential
	
	# python
	apt-get install libhdf5-serial-dev libboost-dev libboost-python-dev python-numpy -y
	apt-get install -y python3-setuptools python3-dev \
	                python3-numpy python3-scipy python3-matplotlib python3-lxml
	easy_install3 pip
	pip install flask-restful
	
	apt-get clean
	
	git clone https://github.com/opengm/opengm.git
	cd opengm
	git reset --hard 571e75abe66c73cc2a554e9e22563750c83509e2
	cmake -DWITH_BOOST=ON -DBUILD_PYTHON_WRAPPER=ON -DWITH_HDF5=ON
	make
	make install
	cd ..

##################
#CentOS Install
##################
elif [ $OS == 'CentOS' ]; then
  echo "Running CentOS Install";

	wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
	rpm --import http://apt.sw.be/RPM-GPG-KEY.dag.txt
	rpm -i rpmforge-release-0.5.3-1.el6.rf.*.rpm

	wget https://www.hdfgroup.org/ftp/HDF5/current/bin/RPMS/hdf5-devel-1.8.15.patch1-1.with.szip.encoder.el6.x86_64.rpm

	rpm --install --dbpath $HOME/rpm --prefix $HOME/usr hdf5-devel-1.8.15.patch1-1.with.szip.encoder.el6.x86_64.rpm 

	## update yum
	yum update && yum upgrade -y
	
	# utils
	#yum install -y wget git software-properties-common vim
	yum install -y wget git vim gcc gcc-c++
	
	#yum install -y openjdk-7-jdk
	
	# basic dev packages
	yum install -y autoconf libtool flex bison autogen cmake
	yum install -y hdf5-devel hdf5
	yum install -y zlib-devel
	yum install -y boost-devel.x86_64
	
	# python
	yum install -y python-devel python-nose python-setuptools
	easy_install pip

	pip install flask-restful
	pip install numpy
	pip install pandas
	pip install pudb
	pip install flufl.enum
	pip install kafka-python
	
	git clone https://github.com/opengm/opengm.git
	cd opengm
	git reset --hard 571e75abe66c73cc2a554e9e22563750c83509e2
	cmake -DWITH_BOOST=ON -DBUILD_PYTHON_WRAPPER=ON -DWITH_HDF5=ON
	make
	make install
	cd ..

	rm hdf5-devel-1.8.15.patch1-1.with.szip.encoder.el6.x86_64.rpm 
	rm rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm



##################
#Unrecognized Distro
##################
else 
  echo "Don't recognize Linux Distro '$OS'. Not Ubuntu or CentOS";
  exit 1;
fi
