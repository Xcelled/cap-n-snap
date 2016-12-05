#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import Colorer
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)

import sys, os
from PyQt5.QtWidgets import QApplication
import screenshot
from ui.selector import Selector

# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))

app = QApplication(sys.argv)

x, y, w, h = screenshot._getDesktopBounds()
x, y, w, h = 100, 100, 500, 500
pixmap = screenshot._captureRegion(x, y, w, h, 0)
sel = Selector(x, y, w, h, pixmap)
app.processEvents()
sel.show()

app.exec_()