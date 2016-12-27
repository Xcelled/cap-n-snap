''' cap n snap plugin to capture the screen '''
from . import screenshot
from PyQt5.QtCore import QMimeData, QMimeDatabase
from PyQt5.QtWidgets import QMenu

mimedb = QMimeDatabase()
pngType = mimedb.mimeTypeForName('image/png') # TODO: More...

class ScreenshotPlugin:
	def __init__(self, host):
		self.host = host
		host.registerCommand('screenshot_desktop', self.captureDesktop, "shift+alt+1")
		host.registerCommand('screenshot_selection', self.captureRegion, "shift+alt+2")
		host.registerCommand('screenshot_window', self.captureWindow, "shift+alt+3")
		host.registerCommand('screenshot_screen', self.captureScreen, "shift+alt+4")

		menu = QMenu('Screenshot...')
		menu.addAction('Desktop', self.captureDesktop, host.getHotkeyForCommand('screenshot_desktop'))
		menu.addAction('Selection', self.captureRegion, host.getHotkeyForCommand('screenshot_selection'))
		menu.addAction('Window', self.captureWindow, host.getHotkeyForCommand('screenshot_window'))
		menu.addAction('Screen', self.captureScreen, host.getHotkeyForCommand('screenshot_screen'))

		host.addMenu(menu)
		self.menu = menu
	#enddef

	def sendToHost(self, img):
		mimeData = QMimeData()
		mimeData.setImageData(img)
		self.host.store(mimeData, pngType)
	#enddef

	def captureDesktop(self): self.sendToHost(screenshot.captureDesktop())
	def captureWindow(self): self.sendToHost(screenshot.captureWindow(False))
	def captureScreen(self): self.sendToHost(screenshot.captureScreen())
	def captureRegion(self):
		img = screenshot.captureRegion()
		if img: self.sendToHost(img)
	#enddef
#endclass

plugin = None

def init(host):
	global plugin
	plugin = ScreenshotPlugin(host)
#enddef

info = {
	'name' : 'Screenshot',
	'version' : 1.0
}
