#!/usr/bin/env python3
#-*- coding:utf-8 -*-

DEBUG = True

import logging, loggingstyleadapter
import Colorer
logging.basicConfig(level=logging.WARN)
loggingstyleadapter.NAG = DEBUG
log = loggingstyleadapter.getLogger(__name__)

if DEBUG: logging.getLogger().setLevel(logging.DEBUG)

import sys, os, plat, config
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from plugins import PluginManager
from host import Host

if plat.Supports.hotkeys: import hotkeys

# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Add kill-switch for development testing
if DEBUG and plat.Supports.hotkeys:
	hotkeys.default.registerCommand('kill', app.exit)
	hotkeys.default._bind('ctrl+shift+k', 'kill')
#endif

plugHost = Host()

pm = PluginManager(plugHost)
pm.load(os.path.join(here, 'plugins'))

hotkeys.default.load()

app.exec_()
config.default.save()
