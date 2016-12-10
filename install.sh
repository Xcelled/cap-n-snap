#!/bin/bash

## Install dependencies. ##

# Run as root!
if [ $(id -u) -ne 0 ]; then
    echo "$0 must be run as root"
    exit 1
fi

apt=`which apt-get`
yum=`which yum`
pac=`which pacman`
git=`which git`

pip=`which pip3 || which pip`
python=`which python3 || which python`

# Check Python version.
if [ `expr match "$($pip --version)" ".*ython 3"` == "0" ]; then
	echo "Cap'n Snap requires Python 3 and pip to install."
	exit 1
fi

if [ `expr match "$($python --version)" ".*ython 3"` == "0" ]; then
	echo "Cap'n Snap requires Python 3 and pip to install."
	exit 1
fi

if [ -z "$git" ]; then
	echo "git is required to install Cap'n Snap"
	exit 1
fi

# Try to install repo packages.
if [ -n "$apt" ]; then
	# This is for Ubuntu. If debian's different then well...
	# TODO: If we already have PyQt from pip, no need to get it again.
	$apt install qtbase5-private-dev python3-pyqt5 pyqt5-dev libxcb-render0-dev libffi-dev # libqxt-dev ??
	# TODO: If pyqt5 package not found, try pip?
elif [ -n "$yum" ]; then
	echo "yum is not currently supported"
	$(exit 1)
elif [ -n "$pac" ]; then
	echo "pacman is not currently supported"
	$(exit 1)
else
	echo "cannot determine package manager"
	$(exit 1)
fi

found=1
if [ $? -ne 0 ]; then
	echo "WARNING: Could not find necessary packages."
	found=
fi

# Install xcffib (linux specific)
$pip install xcffib
if [ $? -ne 0 ]; then
	echo "ERROR: Could not install xcffib"
	exit 2
fi

# Install pip dependencies.
$pip install -r requirements.txt
if [ $? -ne 0 ]; then
	echo "ERROR: Could not install necessary packages."
	exit 2
fi

# Install xpybutil
rm -rf xpybutil
$git clone https://github.com/BurntSushi/xpybutil.git
if [ $? -ne 0 ]; then
	echo "ERROR: Could not clone xpybutil"
	exit 2
fi
cd xpybutil
$python setup.py install
if [ $? -ne 0 ]; then
	echo "ERROR: Could not install xpybutil."
	exit 2
fi
cd ..
rm -rf xpybutil

# TODO: Install this.

echo "Installation complete."
