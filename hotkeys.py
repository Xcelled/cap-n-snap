import logging
log = logging.getLogger(__name__)

from system_hotkey import SystemHotkey
from collections import Counter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

import config

modMap = zip(
	[Qt.ShiftModifier, Qt.ControlModifier, Qt.AltModifier, Qt.MetaModifier],
	['shift'         , 'control'         , 'alt'         , 'super'        ]
)

allMods = int(Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)

def seqToTuple(seq):
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

	def register(self, seq, cb):
		try: seq = QKeySequence(seq)
		except: pass
		t = seqToTuple(seq)
		log.debug('Registering hotkey {} => {}'.format(t, cb))
		self.hk.register(t, callback=cb)
	#enddef

	def unregister(self, seq):
		try: seq = QKeySequence(seq)
		except: pass
		t = seqToTuple(seq)
		log.debug('Removing hotkey {}'.format(t))
		self.hk.unregister(t)
	#enddef

	def registerCommand(self, name, function):
		''' Register a command for use by a hotkey '''
		if name in self.commands:
			log.warning('Registering over existing command name %s', name)
		#endif

		self.commands[name] = function
	#enddef

	# TODO: These don't care about modifier order and probably should.
	def add(self, seq, command):
		''' Add a new hotkey with with a command name intended to be saved to the config '''
		hks = config.default.get('hotkeys', {})
		if seq in hks:
			log.warning('Reassigning existing sequence %s', seq)
		#endif

		hks[seq] = command
		config.default.set('hotkeys', hks)
		config.default.save()

		if command in self.commands:
			self.register(seq, self.commands[command])
		else:
			log.warning('Saved hotkey %s to unknown command %s', seq, command)
		#endif
	#enddef

	def remove(self, seq):
		''' Remove a hotkey from the config '''
		hks = config.default.get('hotkeys', {})
		try: del hks[seq]
		except KeyError: pass
		else:
			self.unregister(seq)
		#endtry
	#enddef

	def applyHotkeys(self):
		''' Apply all hotkeys defined in the config '''
		for hotkey, command in config.default.get('hotkeys', {}).items():
			if command in self.commands:
				self.register(hotkey, self.commands[command])
			else:
				log.error('Tried to register hotkey %s to unknown command %s', hotkey, command)
			#endif
		#endfor
	#enddef

	def removeHotkeys(self):
		''' Remove all hotkeys defined in the config '''
		if not plat.Supports.hotkeys: return

		for hotkey, command in config.default.get('hotkeys', {}).items():
			self.unregister(hotkey)
		#endfor
	#enddef
#endef

default = HotkeyManager()
