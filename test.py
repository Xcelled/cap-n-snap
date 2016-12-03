import logging
import Colorer
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

import sys
from PyQt5.QtWidgets import QApplication
import screenshot, plugins

app = QApplication(sys.argv)

plugs = plugins.PluginManager()
plugs.load('plugins')