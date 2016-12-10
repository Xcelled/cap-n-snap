#-*- coding:utf-8 -*-

import os, json, plat, logging, hotkeys
from PyQt5.QtCore import QSettings
log = logging.getLogger(__name__)

class Config:
	def __init__(self, filename=None):
		# Get the config file location if one is specified.
		self.filename = filename or os.getenv('CAPNSNAP_CONFIG', None)
		self.qsettings = QSettings("Cap-n_Snap", "Cap-n_Snap")

		self.hooks = {
			'beforeLoad': [],
			'afterLoad': [],
			'beforeSave': [],
			'afterSave': [],
		}
		self.load()
	#enddef

	def execHooks(self, name):
		for (hook, userdata) in self.hooks[name]:
			hook(userdata)
		#endfor
	#enddef

	def hook(self, hn, hook, userdata=None):
		self.hooks[hn].append((hook, userdata))
	#enddef

	def unhook(self, hn, hook):
		found = False
		for i, (fun, userdata) in enumerate(self.hooks[hn]):
			if fun == hook:
				found = True
				break
			#endif
		#endfor

		if found:
			self.hooks[hn].pop(i)
		#endif
	#enddef

	def beforeLoad(self, hook, userdata=None): self.hook('beforeLoad', hook, userdata)
	def afterLoad(self, hook, userdata=None): self.hook('afterLoad', hook, userdata)
	def beforeSave(self, hook, userdata=None): self.hook('beforeSave', hook, userdata)
	def afterSave(self, hook, userdata=None): self.hook('afterSave', hook, userdata)

	def load(self):
		self.execHooks('beforeLoad')
		if self.filename:
			log.debug('Loading config from %s', self.filename)
			self.config = json.load(self.filename)
		else:
			log.debug('Loading config from %s', self.qsettings.fileName())
			self.qsettings.sync()
			self.config = json.loads(self.qsettings.value('settings', '{}'))
		#endif
		self.execHooks('afterLoad')
	#enddef

	def save(self):
		self.execHooks('beforeSave')
		if self.filename:
			log.debug('Saving config to %s', self.filename)
			json.dump(self.filename, self.config)
		else:
			log.debug('Saving config to %s', self.qsettings.fileName())
			self.qsettings.setValue('settings', json.dumps(self.config))
			self.qsettings.sync()
		#endif
		self.execHooks('afterSave')
	#enddef

	def get(self, key, default=None):
		return self.config.get(key, default)
	#enddef

	def set(self, key, value):
		self.config[key] = value
		self.save()
	#enddef
#endclass

default = Config()
