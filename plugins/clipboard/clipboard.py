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

	def handles(self, data):
		return True # Clippy handles everything
	#enddef

	def store(self, data):
		QApplication.clipboard.setMimeData(data)
	#enddef
#enddef

class ClipboardSource:
	def __init__(self):
		pass
	#enddef

	def capture(self):
		return QApplication.clipboard.mimeData()
	#enddef
#endclass