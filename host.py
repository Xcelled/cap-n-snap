import logging
log = logging.getLogger(__name__)

import hotkeys

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
		if defaultHotkey:
			if not hk.commandHasHotkey(name) and not hk.hasHotkey(defaultHotkey):
				hk.add(defaultHotkey, name)
			else:
				log.info('Not registering default hotkey for %s (in use or already assigned)', name)
			#endif
		#endif
	#enddef

	def store(self, data, type, **kwargs):
		''' Stores the given data '''
		print('Implement me (store) for cool stuff!')
	#enddef
#endclass