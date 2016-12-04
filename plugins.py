''' Plugin manager '''

import logging, importlib, sys, os, os.path
log = logging.getLogger(__name__)

class PluginManager:
	def __init__(self, host):
		self.plugins = []
		self.host = host
	#enddef

	def _getPlugins(pluginFolder):
		''' Loads plugin packages from the folder and returns a tuple
		of (package name, `import packagename`)'''
		importlib.invalidate_caches()

		plugs = []
		for (dirpath, dirnames, filenames) in os.walk(pluginFolder):
			plugs.extend([d for d in dirnames if d[0] != '.'])
			for fn in (f for f in filenames if f[0] != '.'):
				abs = os.path.realpath(os.path.join(dirpath, fn))
				if abs not in sys.path: sys.path.append(abs)
				plugs.append(os.path.splitext(fn)[0])
			#endfor
			break
		#endfor

		for pkgname in plugs:
			log.debug('Loading package {}'.format(pkgname))
			try:
				module = importlib.reload(importlib.import_module(pkgname))
				yield pkgname, module
			except:
				log.exception('Cannot load package {}'.format(pkgname))
			#endtry
		#endfor
	#enddef

	def load(self, pluginFolder):
		pluginFolder = os.path.realpath(pluginFolder)
		log.info('Loading plugins from {}'.format(pluginFolder))
		if pluginFolder not in sys.path: sys.path.append(pluginFolder)

		self.plugins = [] # todo: unload these?

		for pkgname, pkg in PluginManager._getPlugins(pluginFolder):
			try:
				info = pkg.info
				init = pkg.init
				log.info('Loaded {} from {}'.format(info['name'], pkgname))
			except:
				log.exception('Failed to load package {}'.format(pkgname))
				continue
			#endtry
			try:
				init(self.host)
				self.plugins.append((pkgname, pkg))
			except:
				log.exception('Failed to initialize {}'.format(pkg.info['name']))
			#endtry
		#endfor
	#enddef
#endclass