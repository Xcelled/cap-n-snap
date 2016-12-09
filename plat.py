''' Utility for dealing with platform-dependent features '''
import logging
log = logging.getLogger(__name__)

import platform, importlib

log.info('{} {}'.format(platform.python_implementation(), platform.python_version()))
log.info('Running on {} {}'.format(platform.platform(), platform.uname()))

LINUX = MAC = WINDOWS = False
plat = platform.system().lower()
if plat.startswith('win'): WINDOWS = True
elif plat.startswith('darwin'): MAC = True
elif plat.startswith('linux'): LINUX = True

if True not in (LINUX, MAC, WINDOWS):
	log.warn('Unsupported platform "{}"'.format(plat))
else:
	log.info('Detected OS as {}'.format('Linux' if LINUX else ('Windows' if Windows else 'Mac')))

#endif

# check OS specific libs
def importOrWarn(libname):
	try:
		importlib.import_module(libname)
		return True
	except ImportError as e:
		log.warn('Failed to load {}.'.format(libname))
		log.warn('Detail: {}'.format(e))
	except:
		log.exception('Unexpected error importing {}.'.format(libname))
	return False
#enddef

class Supports:
	hotkeys = True
	windowCapture = False
#endclass

if LINUX:
	xlib = importOrWarn('xcffib') #importOrWarn('Xlib')
	xpybutil = importOrWarn('xpybutil')
	if not xlib or not xpybutil:
		log.warn('Hotkeys are disabled.')
		Supports.hotkeys = False
	#endif
elif WINDOWS:
	pywin32 = importOrWarn('pywin32')
	if not pywin32:
		log.warn('Hotkeys are disabled')
		Supports.hotkeys = False
	#endif
else:
	log.warn('Hotkeys are not supported on your system')
	Supports.hotkeys = False
#endif

feats = dict((attr, getattr(Supports, attr)) for attr in dir(Supports) if not callable(getattr(Supports,attr)) and not attr.startswith("__"))
log.info('Supported features: {}'.format(feats))