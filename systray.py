import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon

menu = QMenu()
sep = menu.addSeparator()
menu.addAction("Preferences")
menu.addAction("Exit", QApplication.exit)

icon = QIcon('img/icon.png')

tray = QSystemTrayIcon(icon)
tray.setToolTip("Cap'n Snap")

def show():
	tray.setContextMenu(menu)
	log.debug('Showing systray')
	tray.show()
#enddef

def hide():
	log.debug('Hiding systray')
	tray.hide()
#enddef

def showMessage(msg, title, **kwargs):
	log.debug('Showing systray message "{message}"', message=msg)
	tray.showMessage(title, msg, **kwargs)
#enddef

def addPluginItem(action):
	log.debug('Adding action to systray: {act}', act=action.text)
	menu.insertAction(sep, action)
#enddef

def addPluginMenu(new_menu):
	log.debug('Adding menu to systray: "{menu}"', menu=new_menu.title())
	menu.insertMenu(sep, new_menu)
#enddef
