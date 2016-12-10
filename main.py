#!/usr/bin/env python3
#-*- coding:utf-8 -*-

DEBUG = True

import logging
import Colorer
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)

if DEBUG: logging.getLogger().setLevel(logging.DEBUG)

import sys, os, plat
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from plugins import PluginManager

if plat.Supports.hotkeys: import hotkeys

# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))

app = QApplication(sys.argv)

# Add kill-switch for development testing
if DEBUG and plat.Supports.hotkeys:
	hotkeys.default.register('ctrl+shift+k', lambda e:app.exit())
#endif

class HostMock:
	def registerDestination(self, x): pass

pm = PluginManager(HostMock())
pm.load(os.path.join(here, 'plugins'))

app.exec_()