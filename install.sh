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

# Try to install repo packages.
if [ -n "$apt" ]; then
	# This is for Ubuntu. If debian's different then well...
	# TODO: If we already have PyQt from pip, no need to get it again.
	$apt install qtbase5-private-dev python3-pyqt5 pyqt5-dev # libqxt-dev ??
	# TODO: If pygt5 package not found, try pip?
elif [ -n "$yum" ]; then
	echo "yum is not currently supported"
	$(exit 1)
elif [ -n "$pac" ]; then
	echo "pacman is not currently supported"
	$(exit 1)
else
	echo "cannot determine package manager"
	$(exit 1)
#endif

found=1
if [ $? -ne 0 ]; then
	echo "WARNING: Could not find necessary packages."
	found=
fi

# Install python-xlib (linux specific)
$pip install python-xlib
if [ $? -ne 0 ]; then
	echo "ERROR: Could not install python-xlib"
	exit 2
fi

# Install pip dependencies.
$pip install -r requirements.txt
if [ $? -ne 0 ]; then
	echo "ERROR: Could not install necessary packages."
	exit 2
fi

# TODO: Install this.

echo "Installation complete."
