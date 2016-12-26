import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

import config, plat

class HotkeyManagerBase:
	def __init__(self):
		super().__init__()
		self.commands = {}
	#enddef

	def load(self):
		config.default.beforeLoad(self.removeHotkeys)
		config.default.afterLoad(self.applyHotkeys)
	#enddef

	def registerCommand(self, name, function):
		''' Register a command that the user can bind with a hotkey '''
		if name in self.commands:
			log.warning('Registering over existing command name "{command}"', command=name)
		#endif

		self.commands[name] = function

		log.debug('Registered command "{name}" for {function}', name=name, function=function)
	#enddef

	def invokeCommand(self, commandName):
		func = self.commands.get(commandName, None)
		if func:
			log.debug('Got hotkey invocation for "{command}" => {func}', command=commandName, func=func)
			func()
		else:
			log.warn('Hotkey triggered unknown command "{command}"', command=commandName)
		#endif
	#enddef
#endclass

if plat.Supports.hotkeys:
	from system_hotkey import SystemHotkey, SystemRegisterError, UnregisterError
	from PyQt5.QtCore import Qt, QObject, pyqtSignal
	from PyQt5.QtGui import QKeySequence

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

	class ShkAdapterMixin(QObject):
		''' Minimal interface adapter for global hotkeys '''
		
		# This class may seem confusing at first. The complexity is due to Qt.
		# Qt's system doesn't like it when qt functions are preformed on anything
		# other than the main thread. This is a problem for system hotkey, which
		# always invokes callbacks on a different thread. So, this class sets up
		# a Qt signal and slot, and uses this to marshal the SHK callback onto
		# the main Qt thread, which then invokes the command bound to the hotkey.

		# Key points: _hotkeyPressed receives callback from SHK. It emits
		# _commandInvoked with the name of the command. _invokeCommand is
		# connected to this signal. It receives the command name, looks up
		# the *actual* command callback in the dictionary and invokes it.

		# Signal that indicates when a command-invoking hotkey was pressed
		_commandInvoked = pyqtSignal(str) 

		def __init__(self):
			super().__init__()
			self.hk = SystemHotkey(consumer=self._hotkeyPressed)
			self._commandInvoked.connect(self.invokeCommand)
		#enddef

		def _hotkeyPressed(self, event, hotkey, args):
			''' Adapts the global callback from system hotkey into a signal '''
			self._commandInvoked.emit(args[0][0])
		#enddef

		def load(self):
			super().load()

			self.applyHotkeys()
		#enddef

		def _bind(self, seq, cmd):
			''' Binds a hotkey to a command name.

			seq can either be a QKeySequence or a string parseable by QKeySequence
			eg "ctrl+shift+k" '''
			try: seq = QKeySequence(seq)
			except: pass

			t = seqToTuple(seq)
			log.debug('Binding hotkey "{hotkey}" => "{command}"', hotkey=seq.toString(), command=cmd)
			
			try: self.hk.register(t, cmd)
			except SystemRegisterError: log.exception('Failed to bind hotkey "{hotkey}"', hotkey=seq.toString())
			else:
				return True
			#endtry

			return False
		#enddef

		def _unbind(self, seq, quiet=False):
			''' Removes a hotkey binding. If Quiet is true, will not warn if the binding doesn't exist '''
			try: seq = QKeySequence(seq)
			except: pass

			t = seqToTuple(seq)
			log.debug('Unbinding hotkey "{hotkey}"', hotkey=seq.toString())

			try: self.hk.unregister(t)
			except UnregisterError: 
				if not quiet: log.warn('Tried to unbind nonexistent hotkey "{hotkey}"', hotkey=seq.toString())
			else:
				return True
			#endtry

			return False
		#enddef

		# TODO: These should directly use QKeySequence in the config

		def commandHasHotkey(self, command):
			''' Checks if the given command has a hotkey registered for it '''
			return not self.hotkeyForCommand(command).isEmpty()
		#enddef

		def hotkeyForCommand(self, command):
			for seq, cmd in config.default.get('hotkeys', {}).items():
				if cmd == command: return QKeySequence(seq)
			#endfor

			return QKeySequence()
		#enddef

		def hasHotkey(self, seq):
			try: seq = QKeySequence(seq)
			except: pass

			return seq.toString() in config.default.get('hotkeys', {})
		#enddef

		def add(self, seq, command):
			''' Add a new hotkey with with a command name intended to be saved to the config '''
			try: seq = QKeySequence(seq)
			except: pass

			seq = seq.toString() # TODO: Removed this (use kyseq directly). UPDATE LOGS when you do (toString)

			hks = config.default.get('hotkeys', {})
			if seq in hks:
				log.warning('Reassigning existing sequence "{hotkey}"', hotkey=seq)
			#endif

			hks[seq] = command
			config.default.set('hotkeys', hks)
			config.default.save() # TODO: Move this to settings UI?

			log.debug('Attempting to bind "{sequence}"', sequence=seq)

			if command not in self.commands:
				log.warning('Saved hotkey "{hotkey}" to unknown command "{command}"', hotkey=seq, command=command)
			#endif

			return True
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
			log.info('Applying hotkeys')
			toRemove = []
			for hotkey, command in config.default.get('hotkeys', {}).items():
				if command in self.commands:
					self._bind(hotkey, command)
				else:
					toRemove.append(hotkey)
					log.error('Tried to bind hotkey "{hotkey}" to unknown command "{command}"', hotkey=hotkey, command=command)
				#endif
			#endfor

			for hotkey in toRemove: self.remove(hotkey)
		#enddef

		def removeHotkeys(self):
			''' Remove all hotkeys defined in the config '''
			log.info('Removing all hotkeys')

			for hotkey, command in config.default.get('hotkeys', {}).items():
				self._unbind(hotkey)
			#endfor
		#enddef
	#endclass
	
	class HotkeyManager(ShkAdapterMixin, HotkeyManagerBase): pass
else:
	class HotkeyManager(HotkeyManagerBase): pass
#endif


default = HotkeyManager()
