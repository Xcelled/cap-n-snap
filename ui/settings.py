import os
from PyQt5 import uic

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))

SettingsUI, SettingsBase = uic.loadUiType(os.path.join(path, 'settings.ui'))

class SettingsWindow(SettingsBase, SettingsUI):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
	#enddef
#endclass
