''' Module containing screenshot functions '''
import platform

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QImage, QPainter
from PyQt5.QtWidgets import QApplication

def captureScreen(screen):
	''' Captures an entire screen '''

	geo = screen.geometry()
	shot = screen.grabWindow(0, geo.x(), geo.y(), geo.width(), geo.height())

	return shot.toImage()
#end def

def captureRegion(x, y, width, height, winId = 0):
	''' Captures a region '''

	region = QRect(x, y, width, height)

	screens = [s for s in QApplication.screens() if s.geometry().intersects(region)]

	# How much to reposition each image so the whole thing is based at 0, 0
	offsetX, offsetY = -x, -y

	final = QImage(width, height, QImage.Format_ARGB32)
	final.fill(QColor(0, 0, 0, 255))

	painter = QPainter()
	painter.begin(final)
	painter.setCompositionMode(QPainter.CompositionMode_Source)

	for screen in screens:
		geo = screen.geometry()
		shot = screen.grabWindow(winId, geo.x(), geo.y(), geo.width(), geo.height())

		# determine the area to copy
		toCopy = geo.intersected(region)

		# Composite it onto the final
		painter.drawPixmap(toCopy.x() + offsetX, toCopy.y() + offsetY, shot.copy(toCopy))
	#end for

	painter.end()

	return final
#end def

def captureDesktop():
	''' Captures the whole desktop '''

	screens = QApplication.screens()

	# Calculate the bounds of the final image
	geos = [s.geometry() for s in screens]
	minX, minY = min(g.x() for g in geos), min(g.y() for g in geos)
	maxX, maxY = max(g.x() + g.width() for g in geos), max(g.y() + g.height() for g in geos)

	return captureRegion(minX, minY, maxX - minX, maxY - minY, 0)
#end def

def captureWindow(windowId, captureWinBorders):
	if platform.lower().startswith('darwin'): captureWinBorders = True

	raise NotImplementedError()
#end def