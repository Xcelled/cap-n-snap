import pkgutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage

class ClipboardDestination:
	def __init__(self):
		self.name = 'Clipboard'
		self.description = 'Copies to the clipboard'
		
		icon = pkgutil.get_data(__name__, 'icon.png')
		self.icon = QImage.fromData(icon)
	#enddef

	def handles(self, type):
		return True # Clippy handles everything
	#enddef

	def store(self, data, type, **kwargs):
		QApplication.clipboard.setMimeData(data)
	#enddef
#enddef