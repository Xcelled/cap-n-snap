import logging
import Colorer
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

import sys
from PyQt5.QtWidgets import QApplication
import screenshot, plugins

app = QApplication(sys.argv)

class hostMock:
	def registerDestination(self, dest):
		print('Got new destination: {}: {}'.format(dest.name, dest.description))


plugs = plugins.PluginManager(hostMock())
plugs.load('plugins')