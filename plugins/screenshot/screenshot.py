''' Module containing screenshot functions '''
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QImage, QPainter, QPixmap, QCursor
from PyQt5.QtWidgets import QApplication
from .selector import Selector
import plat

if plat.Supports.wintools: import wintools

def _captureRegion(x, y, width, height, winId = 0):
	''' Captures a region '''

	region = QRect(x, y, width, height)

	screens = [s for s in QApplication.screens() if s.geometry().intersects(region)]

	# How much to reposition each image so the whole thing is based at 0, 0
	offsetX, offsetY = -x, -y

	final = QPixmap(width, height)
	final.fill(QColor(0, 0, 0, 255))

	painter = QPainter()
	painter.begin(final)
	painter.setCompositionMode(QPainter.CompositionMode_Source)

	for screen in screens:
		geo = screen.geometry()
		snap = screen.grabWindow(winId, geo.x(), geo.y(), geo.width(), geo.height())

		# determine the area to copy
		toCopy = geo.intersected(region)

		# Composite it onto the final
		painter.drawPixmap(toCopy.x() + offsetX, toCopy.y() + offsetY, snap.copy(toCopy))
	#end for

	painter.end()

	return final
#end def

def _getDesktopBounds():
	screens = QApplication.screens()

	# Calculate the bounds of the final image
	geos = [s.geometry() for s in screens]
	minX, minY = min(g.x() for g in geos), min(g.y() for g in geos)
	maxX, maxY = max(g.x() + g.width() for g in geos), max(g.y() + g.height() for g in geos)

	return minX, minY, maxX - minX, maxY - minY
#enddef

def captureDesktop():
	''' Captures the whole desktop '''

	x, y, w, h = _getDesktopBounds()

	return _captureRegion(x, y, w, h, 0).toImage()
#end def

def captureScreen():
	''' Captures the screen the mouse is currently on '''
	num = QApplication.desktop().screenNumber(QCursor.pos())
	geo = QApplication.screens()[num].geometry()

	return _captureRegion(geo.x(), geo.y(), geo.width(), geo.height(), 0).toImage()
#enddef

def captureWindow(windowId, captureWinBorders):
	if not plat.Supports.wintools: raise NotImplementedError()

	if plat.MAC: captureWinBorders = True

	activeWin = wintools.getActiveWin()

	if captureWinBorders:
		# TODO: If KDE...
		geo = wintools.getWinGeomtry(activeWin)
		return _captureRegion(geo.x(), geo.y(), geo.width(), geo.height(), 0).toImage()
	#endif

	return QApplication.primaryScreen().grabWindow(activeWin).toImage()
#end def

def captureRegion():
	x, y, w, h = _getDesktopBounds()
	pixmap = _captureRegion(x, y, w, h, 0)
	
	sel = Selector(x, y, w, h, pixmap)
	sel.exec_()

	toCopy = sel.selection()

	if toCopy is None: return None

	return pixmap.copy(toCopy).toImage()
#enddef