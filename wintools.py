import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

import plat
from PyQt5.QtCore import QRect

if plat.LINUX:
	# X11 stuff for getting windows
	from xpybutil import ewmh, window

	def getActiveWin():
		return ewmh.get_active_window().reply()
	#endif

	def getWinGeometry(wid, skip=0, **kwargs):
		''' Gets the window geometry of the window.

		Skip controls howe many extra parents we should go to to get the geometry.
		In most window managers, this should be zero (ie, decorations are the parent of wid).
		However, at least one (KWin) introduces an extra parent window, so the decorations
		are actually the grandparent of the wid. In this case, skip should be 1. '''
		for i in range(skip): wid = window.get_parent_window(wid)

		geo = window.get_geometry(wid).reply() # x, y, w, h
		return QRect(*geo)
	#enddef
elif plat.WINDOWS:
	import win32gui

	def getActiveWin():
		return win32gui.GetForegroundWindow()
	#enddef

	def getWinGeometry(wid, **kwargs):
		bounds = win32gui.GetWindowRect(wid)
		return QRect(bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1])
	#enddef
#endif