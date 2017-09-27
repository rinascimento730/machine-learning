#!/bin/bash

# set install version
PYTHON="3.6"
PYTHON_FULL="3.6.2"

#set PATH
SRC_TO="/usr/local/src"
PYTHON_AT="/opt/local"
PIP_AT="/opt/local"

# yum upgrade
sudo yum -y upgrade

# install dev tools
sudo yum -y groupinstall "Development tools"
sudo yum -y install git zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel scl-utils

# install boost-devel
if [ ! -e /etc/yum.repos.d/enetres.repo ]
then
    sudo wget http://repo.enetres.net/enetres.repo -O /etc/yum.repos.d/enetres.repo
    sudo yum -y localinstall http://repo.enetres.net/x86_64/boost-devel-1.59.0-1.x86_64.rpm
fi

# add Devtoolset-3 Repo
if [ ! -e /etc/yum.repos.d/rhscl-devtoolset-3-epel-6.repo ]
then
    cd  /etc/yum.repos.d/
    sudo wget --no-check-certificate https://copr-fe.cloud.fedoraproject.org/coprs/rhscl/devtoolset-3/repo/epel-6/rhscl-devtoolset-3-epel-6.repo
    sudo yum -y install devtoolset-3-gcc devtoolset-3-binutils
    sudo yum -y install devtoolset-3-gcc-c++ devtoolset-3-gcc-gfortran

    #scl enable devtoolset-3 bash
    echo 'source /opt/rh/devtoolset-3/enable' >> ~/.bash_profile
fi

# install MySQL
sudo yum -y install http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
sudo yum -y install mysql mysql-devel mysql-server mysql-utilities
sudo chkconfig mysqld on

# install PYTHON
if [ ! -e ${PYTHON_AT}/bin/python${PYTHON} ]
then
    # get PYTHON
    cd ${SRC_TO}
    sudo curl -O https://www.python.org/ftp/python/${PYTHON_FULL}/Python-${PYTHON_FULL}.tgz
    sudo tar zxf Python-${PYTHON_FULL}.tgz

    # install PYTHON
    cd Python-${PYTHON_FULL}
    sudo ./configure --prefix=${PYTHON_AT}
    sudo make && sudo make altinstall
fi

# enable python
if [ ! `echo  $PATH | grep ${PYTHON_AT}'/bin'` ]
then
  echo 'export PATH=$PATH:'${PYTHON_AT}'/bin' >> ~/.bash_profile
  source ~/.bash_profile
fi

# install pip3
if [ ! -e ${PIP_AT}/bin/pip${PYTHON} ]
then
	cd ${SRC_TO}
    # install pip
    sudo curl -O https://bootstrap.pypa.io/get-pip.py
    sudo ${PYTHON_AT}/bin/python${PYTHON} get-pip.py

    #install virtualenv
    sudo ${PIP_AT}/bin/pip${PYTHON} install virtualenv

    # install distribute
    sudo ${PIP_AT}/bin/pip${PYTHON} install -U setuptools
fi

# install beautifulsoup
sudo ${PIP_AT}/bin/pip${PYTHON} install beautifulsoup4

# install scikit-learn
sudo ${PIP_AT}/bin/pip${PYTHON} install scikit-learn

# install matplotlib
sudo ${PIP_AT}/bin/pip${PYTHON} install matplotlib

# install numpy
sudo ${PIP_AT}/bin/pip${PYTHON} install numpy

# install scipy
sudo ${PIP_AT}/bin/pip${PYTHON} install scipy

# install sphinx
sudo ${PIP_AT}/bin/pip${PYTHON} install sphinx

# install pydot
sudo ${PIP_AT}/bin/pip${PYTHON} install pydot

# install nose
sudo ${PIP_AT}/bin/pip${PYTHON} install nose

# install basemap
sudo ${PIP_AT}/bin/pip${PYTHON} install https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz

# install gensim
sudo ${PIP_AT}/bin/pip${PYTHON} install --upgrade gensim

# get oreilly sample source
if [ ! -e /vagrant/BuildingMachineLearningSystemsWithPython ] && [ -f /vagrant/Vagrantfile ]
then
    cd /vagrant
    git clone https://github.com/wrichert/BuildingMachineLearningSystemsWithPython.git
fi

# get PyRockSim
if [ ! -e /vagrant/PyRockSim ] && [ -f /vagrant/Vagrantfile ]
then
    cd /vagrant
    git clone https://github.com/pyjbooks/PyRockSim.git
fi

if [ ! -e ~/.config/matplotlib/ ]
then
    mkdir -p ~/.config/matplotlib/
fi

if [ ! -f ~/.config/matplotlib/matplotlibrc ]
then
    echo "backend : Agg" > ~/.config/matplotlib/matplotlibrc
fi

