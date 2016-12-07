#!/usr/bin/env python3
#-*- coding:utf-8 -*-

DEBUG = True

import logging
import Colorer
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)

import sys, os, plat
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication

log.info('Detected OS as {}'.format('Linux' if plat.LINUX else ('Windows' if plat.Windows else 'Mac')))

if plat.Supports.Hotkeys: from system_hotkey import SystemHotkey

# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))

app = QApplication(sys.argv)

# Add kill-switch for development testing
if DEBUG and plat.Supports.Hotkeys:
	kill = SystemHotkey()
	kill.register(('control', 'shift', 'k'), callback=lambda e:app.exit())
#endif

app.exec_()