import logging
log = logging.getLogger(__name__)

from system_hotkey import SystemHotkey
from collections import Counter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

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
#endef

default = HotkeyManager()