#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import Colorer
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)

import sys
from PyQt5.QtWidgets import QApplication
import screenshot

app = QApplication(sys.argv)
