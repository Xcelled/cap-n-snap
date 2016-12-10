#-*- coding:utf-8 -*-

import os, json, plat, logging, hotkeys
from PyQt5.QtCore import QSettings
log = logging.getLogger(__name__)

class Config:
	def __init__(self, filename=None):
		# Get the config file location if one is specified.
		self.filename = filename or os.getenv('CAPNSNAP_CONFIG', None)
		self.qsettings = QSettings("Cap-n_Snap", "Cap-n_Snap")

		self.registrations = {
			'commands': {}
		}

		self.load(hotkeys=False)
	#enddef

	def load(self, hotkeys=True):
		if hotkeys: self.removeHotkeys()
		if self.filename:
			log.debug('Loading config from %s', self.filename)
			self.config = json.load(self.filename)
		else:
			log.debug('Loading config from %s', self.qsettings.fileName())
			self.qsettings.sync()
			self.config = json.loads(self.qsettings.value('settings', '{}'))
		#endif
		if hotkeys: self.applyHotkeys()
	#enddef

	def save(self):
		if self.filename:
			log.debug('Saving config to %s', self.filename)
			json.dump(self.filename, self.config)
		else:
			log.debug('Saving config to %s', self.qsettings.fileName())
			self.qsettings.setValue('settings', json.dumps(self.config))
			self.qsettings.sync()
		#endif
	#enddef

	def registerCommand(self, name, function):
		''' Register a command for use by a hotkey '''
		cmds = self.registrations['commands']
		if name in cmds:
			log.warning('Registering over existing command name %s', name)
		#endif

		cmds[name] = function
	#enddef

	def applyHotkeys(self):
		''' Apply all hotkeys defined in the config '''
		if not plat.Supports.hotkeys: return

		cmds = self.registrations['commands']
		for hotkey, command in self.config.get('hotkeys', {}).items():
			if command in cmds:
				hotkeys.default.register(hotkey, cmds[command])
			else:
				logging.error('Tried to register hotkey %s to unknown command %s', hotkey, command)
			#endif
		#endfor
	#enddef

	def removeHotkeys(self):
		''' Remove all hotkeys defined in the config '''
		if not plat.Supports.hotkeys: return

		cmds = self.registrations['commands']
		for hotkey, command in self.config.get('hotkeys', {}).items():
			hotkeys.default.unregister(hotkey)
		#endfor
	#enddef

#endclass

default = Config()
