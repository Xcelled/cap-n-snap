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
	$apt install qtbase5-private-dev python3-pyqt5 pyqt5-dev # libqxt-dev ??
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

# Install pip dependencies.
$pip install PyGlobalShortcut
if [ $? -ne 0 ]; then
	echo "ERROR: Could not install necessary packages."
	exit 2
elif [ $found ]; then
	# If we're using system packages, we don't want the pip version of PyQt5 that PyGlobalShortcut might install.
	$pip remove PyQt5
fi

# Test import.
python3 -c 'import pygs'
if [ $? -ne 0 ]; then
	echo "ERROR: PyGlobalShortcut not importing correctly, see error output above for details."
	exit 3
fi

# TODO: Install this.

echo "Installation complete."
