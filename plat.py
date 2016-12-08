''' Utility for dealing with platform-dependent features '''
import logging
log = logging.getLogger(__name__)

import sys, importlib

LINUX = MAC = WINDOWS = False
plat = sys.platform.lower()
if plat.startswith('win'): WINDOWS = True
elif plat.startswith('darwin'): MAC = True
else: LINUX = True

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
	Hotkeys = True
	WindowCapture = False
#endclass

if LINUX:
	xlib = importOrWarn('xcffib') #importOrWarn('Xlib')
	xpybutil = importOrWarn('xpybutil')
	if not xlib or not xpybutil:
		log.warn('Hotkeys are disabled.')
		Supports.Hotkeys = False
	#endif
elif WINDOWS:
	pywin32 = importOrWarn('pywin32')
	if not pywin32:
		log.warn('Hotkeys are disabled')
		Supports.Hotkeys = False
	#endif
else:
	log.warn('Hotkeys are not supported on your system')
	Supports.Hotkeys = False
#endif
