''' Plugin manager '''

import logging, pkgutil, importlib, sys, os.path
log = logging.getLogger(__name__)

class PluginManager:
	def __init__(self):
		self.plugins = []
	#enddef

	def _getPlugins(pluginFolder):
		''' Loads plugin packages from the folder and returns a tuple
		of (package name, `import packagename`)'''
		importlib.invalidate_caches()

		# todo: replace this with directories + zip

		for _, pkgname, ispkg in pkgutil.walk_packages([pluginFolder]):
			if not ispkg:
				log.debug('Skipping {}'.format(pkgname))
				continue
			#endif

			log.debug('Loading package {}'.format(pkgname))
			try:
				module = importlib.reload(importlib.import_module(pkgname))
				yield pkgname, module
			except:
				log.exception('Cannot load package{}'.format(pkgname))
			#endtry
		#endfor
	#enddef

	def load(self, pluginFolder):
		pluginFolder = os.path.realpath(pluginFolder)
		log.info('Loading plugins from {}'.format(pluginFolder))
		if pluginFolder not in sys.path: sys.path.append(pluginFolder)

		self.plugins = [] # todo: unload these?

		for pkgname, pi in PluginManager._getPlugins(pluginFolder):
			try:
				info = pi.info
				plug = pi.getPlugin()
				log.info('Loaded {} from {}'.format(info['name'], pkgname))
			except:
				log.exception('Failed to load package {}'.format(pkgname))
				continue
			#endtry
			try:
				plug.init(self)
				self.plugins.append((pkgname, pi, plug))
			except:
				log.exception('Failed to initialize {}'.format(pi.info['name']))
			#endtry
		#endfor
	#enddef
#endclass