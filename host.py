import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

from PyQt5.QtGui import QKeySequence
import hotkeys, plat, systray

class Host:
	def __init__(self):
		pass
	#enddef

	def registerDestination(self, destination):
		print("Don't forget to implement me (registerDestination)")
	#enddef

	def registerCommand(self, name, callback, defaultHotkey=None):
		hk = hotkeys.default
		hk.registerCommand(name, callback)
		if defaultHotkey and plat.Supports.hotkeys:
			if not hk.commandHasHotkey(name) and not hk.hasHotkey(defaultHotkey):
				hk.add(defaultHotkey, name)
			else:
				log.info('Not registering default hotkey for "{name}" (in use or already assigned)', name=name)
			#endif
		#endif
	#enddef

	def getHotkeyForCommand(self, cmd):
		if plat.Supports.hotkeys:
			return hotkeys.default.hotkeyForCommand(cmd)
		else:
			return QKeySequence()
		#endif
	#enddef

	def store(self, data, type, **kwargs):
		''' Stores the given data '''
		print('Implement me (store) for cool stuff!')
	#enddef

	def addMenuItem(self, action):
		''' Adds an action to the system tray menu '''
		return systray.addPluginItem(action)
	#enddef

	def addMenu(self, menu):
		''' Adds a submenu to the system tray menu '''
		return systray.addPluginMenu(menu)
	#enddef
#endclass