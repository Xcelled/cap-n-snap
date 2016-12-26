from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon

menu = QMenu()
sep = menu.addSeparator()
menu.addAction("Preferences")
menu.addAction("Exit", QApplication.exit)

icon = QIcon('img/icon.png')

tray = QSystemTrayIcon(icon)
tray.setToolTip("Cap'n Snap")
tray.setContextMenu(menu)

def show():
	tray.show()
#enddef

def hide():
	tray.hide()
#enddef

def showMessage(msg, title, **kwargs):
	tray.showMessage(title, msg, **kwargs)
#enddef