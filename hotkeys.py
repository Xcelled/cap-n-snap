import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

from system_hotkey import SystemHotkey, SystemRegisterError, UnregisterError, InvalidKeyError
from collections import Counter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

import config

modMap = list(zip(
	[Qt.ShiftModifier, Qt.ControlModifier, Qt.AltModifier, Qt.MetaModifier],
	['shift'         , 'control'         , 'alt'         , 'super'        ]
))

allMods = int(Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)

def seqToTuple(seq):
	''' Converts a QKeySequence to system_hotkey's Tuple format '''
	r = []
	key = 0 if seq.isEmpty() else seq[0] & ~allMods
	mods = 0 if seq.isEmpty() else seq[0] & allMods
	
	for mod, s in modMap:
		if seq[0] & mod: r.append(s)
	#endfor
	
	r.append(QKeySequence(key).toString().lower())

	return tuple(r)
#enddef

class HotkeyManager:
	''' Minimal interface adapter for global hotkeys '''
	def __init__(self):
		self.hk = SystemHotkey()
		self.commands = {}
	#enddef

	def load(self):
		config.default.beforeLoad(self.removeHotkeys)
		config.default.afterLoad(self.applyHotkeys)

		self.applyHotkeys()
	#enddef

	def _bind(self, seq, cb):
		''' Binds a hotkey to a callback function.

		seq can either be a QKeySequence or a string parseable by QKeySequence
		eg "ctrl+shift+k" '''
		try: seq = QKeySequence(seq)
		except: pass

		t = seqToTuple(seq)
		log.debug('Binding hotkey {hotkey} => {callback}', hotkey=t, callback=cb)
		
		try: self.hk.register(t, callback=lambda e:cb())
		except SystemRegisterError: log.exception('Failed to bind hotkey {}'.format(seq.toString()))
		else: return True

		return False
	#enddef

	def _unbind(self, seq, quiet=False):
		''' Removes a hotkey binding. If Quiet is true, will not warn if the binding doesn't exist '''
		try: seq = QKeySequence(seq)
		except: pass

		t = seqToTuple(seq)
		log.debug('Unbinding hotkey {hotkey}', hotkey=t)

		try: self.hk.unregister(t)
		except InvalidKeyError: 
			if not quiet: log.warn('Tried to unbind nonexistent hotkey {}'.format(seq.toString()))
		except UnregisterError as e: log.exception('Failed to unbind hotkey {}'.format(seq.toString()))
		else: return True

		return False
	#enddef

	def registerCommand(self, name, function):
		''' Register a command that the user can bind with a hotkey '''
		if name in self.commands:
			log.warning('Registering over existing command name {command}', command=name)
		#endif

		self.commands[name] = function

		log.debug('Registered command {} for {}'.format(name, function))
	#enddef

	# TODO: These should directly use QKeySequence in the config
	def commandHasHotkey(self, command):
		''' Checks if the given command has a hotkey registered for it '''
		return command in config.default.get('hotkeys', {}).values()
	#enddef

	def hasHotkey(self, seq):
		try: seq = QKeySequence(seq)
		except: pass

		return seq.toString in config.default.get('hotkeys', {})
	#enddef
	def add(self, seq, command):
		''' Add a new hotkey with with a command name intended to be saved to the config '''
		try: seq = QKeySequence(seq)
		except: pass

		seq = seq.toString() # TODO: Removed this (use kyseq directly). UPDATE LOGS when you do (toString)

		hks = config.default.get('hotkeys', {})
		if seq in hks:
			log.warning('Reassigning existing sequence {hotkey}', hotkey=seq)
		#endif

		hks[seq] = command
		config.default.set('hotkeys', hks)
		config.default.save() # TODO: Move this to settings UI?

		log.debug('Attempting to bind %s', seq)

		if command in self.commands:
			return self._bind(seq, self.commands[command])
		else:
			log.warning('Saved hotkey {hotkey} to unknown command {command}', hotkey=seq, command=command)

		return True
		#endif
	#enddef

	def remove(self, seq):
		''' Remove a hotkey from the config '''
		hks = config.default.get('hotkeys', {})
		try: del hks[seq]
		except KeyError: pass
		else:
			return self._unbind(seq)

		return False
		#endtry
	#enddef

	def applyHotkeys(self):
		''' Apply all hotkeys defined in the config '''
		toRemove = []
		for hotkey, command in config.default.get('hotkeys', {}).items():
			if command in self.commands:
				self._bind(hotkey, self.commands[command])
			else:
				toRemove.append(hotkey)
				log.error('Tried to bind hotkey {hotkey} to unknown command {command}', hotkey=hotkey, command=command)
			#endif
		#endfor

		for hotkey in toRemove: self.remove(hotkey)
	#enddef

	def removeHotkeys(self):
		''' Remove all hotkeys defined in the config '''
		if not plat.Supports.hotkeys: return

		for hotkey, command in config.default.get('hotkeys', {}).items():
			self._unbind(hotkey)
		#endfor
	#enddef
#endef

default = HotkeyManager()
