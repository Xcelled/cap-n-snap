import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

from PyQt5.QtCore import QCoreApplication, QRect, QRectF, QPointF, Qt, QObject, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def _(*args, **kwargs): return QCoreApplication.translate('Selector', *args, **kwargs)


class RegionSelector:
	'''Class to handle coordinating multiple selector windows for a multimonitor setup. '''

	def __init__(self, x, y, w, h, pixmap):
		self.moving = self.drawing = self.resizing = False

		self.bounds = QRectF(x, y, w, h)
		self.selectors = []
		self.selection = None
		for screen in QApplication.screens():
			# make a new selector for this screen
			# TODO: Support limited subset of screens?
			geo = screen.geometry()
			sel = Selector(geo.x(), geo.y(), geo.width(), geo.height(), pixmap, self)
			self.selectors.append(sel)
		#endfor
	#enddef

	def exec_(self):
		cPos = QCursor.pos()
		QCursor.setPos(0, 0) # XFCE workaround. In XCFE, window position is relative to the cursor position
		for sel in self.selectors: sel.show()
		QCursor.setPos(cPos)
		self.selectors[-1].exec_()
	#enddef

	def updateSelection(self):
		for s in self.selectors: s.updateSelection()
	#enddef

	def mousePressEvent(self, e):
		pos = e.globalPos()
		self.moving = self.drawing = self.resizing = False
		
		if self.selection is None or not self.selection.contains(pos):
			self.drawing = True
			self.selection = None
			self.selectionStart = pos
		#elif in corner
		#elif on line
		else: # in
			self.moving = True
			self.selBeforeMove = self.selection
			self.moveOrigin = pos
		#endif
		self.updateSelection()
	#enddef

	def mouseMoveEvent(self, e):
		pos = e.globalPos()
		if self.drawing:
			if pos.x() != self.selectionStart.x() and pos.y() != self.selectionStart.y():
				self.selection = QRectF(QPointF(self.selectionStart), QPointF(pos)).normalized()
				self.selection = self.selection.intersected(self.bounds)
				self.updateSelection()
			#endif
		elif self.moving:
			delta = pos - self.moveOrigin
			moved = self.selBeforeMove.translated(delta)

			# TODO: this cause the bounds to be "sticky", since trying to move back after pushing it 50px off the edge
			# means we must re-traverse the other 49 "off screen" pixels before we get some visible movement
			minX, maxX = self.bounds.x(), self.bounds.x() + self.bounds.width() - moved.width()
			minY, maxY = self.bounds.y(), self.bounds.y() + self.bounds.height() - moved.height()

			moved.moveTo(min(max(minX, moved.x()), maxX), min(max(minY, moved.y()), maxY))

			self.selection = moved.intersected(self.bounds)
			self.updateSelection()
		#endif
	#enddef

	def mouseReleaseEvent(self, e):
		self.moving = self.drawing = self.resizing = False

		self.updateSelection()
	#enddef

	def keyReleaseEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.selection = None
			self.close()
		elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
			if self.selection:
				self.close()
			#endif
		#endif
	#enddef

	def close(self):
		for s in self.selectors: s.close()
	#enddef
#endclass
	

class Selector(QDialog):
	def __init__(self, x, y, width, height, pixmap, region):
		super().__init__()
		log.debug('Opening selector at {x}, {y}: {w} {h}', x=x, y=y, w=width, h=height)
		self.region = region
		# ui setup
		self.setWindowTitle(_('Select a region'))
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setFocusPolicy(Qt.StrongFocus)
		
		bgImg = QGraphicsPixmapItem(pixmap)

		self.view = QGraphicsView(self)
		self.view.setStyleSheet("QGraphicsView { border-style: none; }")
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.graphics = QGraphicsScene(self.view)
		self.graphics.addItem(bgImg)
		self.view.setScene(self.graphics)

		self.view.setGeometry(0, 0, width, height)
		self.view.setSceneRect(x, y, width, height)

		self.bounds = QRect(x, y, width, height)
		self.rubber = OccultingRubberband(self, QColor(100,100,100,140), QColor('red'), 15,
			'Select an area using the mouse.\nPress Enter to take a screenshot or Esc to exit.',
			 QColor(28,28,28,220), QColor(150,150,150,240), region)
		self.rubber.setSceneRect(QRectF(self.bounds))
		self.rubber.setGeometry(0, 0, width, height)
	#enddef

	def showEvent(self, e):
		self.raise_()
		self.setGeometry(self.bounds)
		self.repaint()
		#self.setWindowState(Qt.WindowFullScreen)
	#enddef

	def keyReleaseEvent(self, event):
		self.region.keyReleaseEvent(event)
		super().keyReleaseEvent(event)
	#enddef

	def updateSelection(self):
		self.rubber._updateLayout()
	#enddef
#endclass

class OccultingRubberband(QGraphicsView):
	''' Implementation of a rubber band that grays out area around the selection '''
	def __init__(self, parent, occultColor, lineColor, handleSize, helpText, textBgColor, textColor, region):
		super().__init__(parent)
		self.region = region
		self.setCursor(Qt.OpenHandCursor)

		self.theScene = QGraphicsScene(self)
		self.setStyleSheet("QGraphicsView { border-style: none; background-color: transparent;}")
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.selectionView = QGraphicsItemGroup()
		self.theScene.addItem(self.selectionView)

		self.occulting = [QGraphicsRectItem() for i in range(4)]
		for o in self.occulting:
			o.setBrush(occultColor)
			o.setPen(QPen(Qt.NoPen))
			o.setCursor(Qt.CrossCursor)
			self.selectionView.addToGroup(o)
		#endfor

		self.lines = [QGraphicsLineItem() for i in range(4)]
		for l, cursor in zip(self.lines, [Qt.SizeHorCursor, Qt.SizeVerCursor]*2):
			l.setPen(QPen(lineColor, 2))
			#l.setCursor(cursor)
			self.selectionView.addToGroup(l)
		#endfor

		self.corners = [QGraphicsRectItem() for i in range(4)]
		for c, cursor in zip(self.corners, [Qt.SizeFDiagCursor, Qt.SizeBDiagCursor]*2):
			c.setBrush(QBrush(occultColor))
			c.setPen(QPen(lineColor, 2))
			c.setCursor(cursor)
			#self.selectionView.addToGroup(c)
		#endfor

		# Displayed when there's no selection
		self.noSelectionHighlight = QGraphicsRectItem()
		self.noSelectionHighlight.setCursor(Qt.CrossCursor)
		self.noSelectionHighlight.setPen(QPen(Qt.NoPen))
		self.noSelectionHighlight.setBrush(QBrush(occultColor))
		self.theScene.addItem(self.noSelectionHighlight)

		helpTextItem = QGraphicsTextItem()
		helpFont = QFont()
		helpFont.setPointSize(20)
		helpTextItem.setFont(helpFont)
		helpTextItem.setDefaultTextColor(textColor)
		helpTextItem.setTextWidth(1000) # TODO: Get this from the geometry
		helpTextItem.document().setDefaultTextOption(QTextOption(Qt.AlignCenter))
		helpTextItem.setPlainText(helpText)

		helpRect = helpTextItem.boundingRect()

		helpRectPath = QPainterPath()
		helpRectPath.addRoundedRect(helpRect.x() - 10, helpRect.y() - 10, helpRect.width() + 20, helpRect.height() + 20, 10, 10)

		helpRectItem = QGraphicsPolygonItem()
		helpRectItem.setPolygon(helpRectPath.toFillPolygon(QTransform()))
		helpRectItem.setBrush(textBgColor)

		self.theScene.addItem(helpRectItem)
		self.theScene.addItem(helpTextItem)

		self.helpOverlay = self.theScene.createItemGroup([helpTextItem, helpRectItem])
		self.helpOverlay.setZValue(2)
		helpTextItem.setZValue(1)

		self.noSelectionOverlay = self.noSelectionHighlight # in case we want to add more here later
		
		# This is so we get a cross cursor while drawing
		# without this, the rubber band's resize cursors take over
		# as the user is drawing initially.
		self.drawingOverlay = QGraphicsRectItem()
		self.drawingOverlay.setCursor(Qt.CrossCursor)
		self.drawingOverlay.setPen(QPen(Qt.NoPen))
		self.theScene.addItem(self.drawingOverlay)

		self.setScene(self.theScene)
		self.handleSize = handleSize
	#enddef

	def _updateLayout(self):
		selection = self.region.selection

		geo = self.sceneRect()

		self.drawingOverlay.setVisible(self.region.drawing)
		if self.region.drawing: self.helpOverlay.setVisible(False)

		if selection is None or not selection.intersects(geo):
			self.selectionView.setVisible(False)
			self.noSelectionOverlay.setVisible(True)
		else:
			# Get the bounds of selection for this window's area
			intersected = selection.intersected(geo)

			# Calculate the bounds of the occulting rectangles
			left, top, right, bottom = self.occulting

			leftBound = selection.x() # X coord of the left edge of selection
			topBound = selection.y() # Y coord of the top edge of selection
			rightBound = leftBound + selection.width() # X coord of the right edge of selection 
			bottomBound = topBound + selection.height() # relative Y coord of the bottom edge of selection

			if leftBound > geo.x(): # Only draw occulting if selection starts to our right
				left.setRect(geo.x(), 0, leftBound - geo.x(), geo.height())
				left.setVisible(True)
			else: left.setVisible(False)

			if topBound > geo.y(): # Only draw top items if selection starts below our top
				top.setRect(leftBound, geo.y(), rightBound - leftBound, topBound - geo.y())
				top.setVisible(True)
			else: top.setVisible(False)

			if rightBound < geo.x() + geo.width(): # Only draw right if selection ends to the left of out right edge
				right.setRect(rightBound, geo.y(), geo.x() + geo.width() + rightBound, geo.height())
				right.setVisible(True)
			else: right.setVisible(False)

			if bottomBound < geo.y() + geo.height(): # Only draw bottom if selection ends above our bottom edge
				bottom.setRect(leftBound, bottomBound, rightBound - leftBound, geo.y() + geo.height() - bottomBound)
				bottom.setVisible(True)
			else: bottom.setVisible(False)

			offset = 2/2 # Half of pen width
			leftBound -= offset
			topBound -= offset
			rightBound += offset
			bottomBound += offset

			left, top, right, bottom = self.lines
			left.setLine(leftBound, topBound, leftBound, bottomBound)
			top.setLine(leftBound, topBound, rightBound, topBound)
			right.setLine(rightBound, topBound, rightBound, bottomBound)
			bottom.setLine(leftBound, bottomBound, rightBound, bottomBound)

			left,top, right, bottom = self.corners
			left.setRect(leftBound, topBound, self.handleSize, self.handleSize)
			top.setRect(rightBound - self.handleSize, topBound, self.handleSize, self.handleSize)
			right.setRect(rightBound - self.handleSize, bottomBound - self.handleSize, self.handleSize, self.handleSize)
			bottom.setRect(leftBound, bottomBound - self.handleSize, self.handleSize, self.handleSize)

			self.selectionView.setVisible(True)
			self.noSelectionOverlay.setVisible(False)
		#endif
	#enddef

	def resizeEvent(self, e):
		geo = QRectF(self.sceneRect())
		self.drawingOverlay.setRect(geo)
		self.noSelectionHighlight.setRect(geo)

		hr = self.helpOverlay.boundingRect()
		hr.moveCenter(geo.center())
		self.helpOverlay.setPos(hr.x(), hr.y())

		self._updateLayout()
	#enddef

	def mousePressEvent(self, e):
		self.region.mousePressEvent(e)
		super().mousePressEvent(e)
	#enddef

	def mouseMoveEvent(self, e):
		self.region.mouseMoveEvent(e)
		super().mouseMoveEvent(e)
	#enddef

	def mouseReleaseEvent(self, e):
		self.region.mouseReleaseEvent(e)
		super().mouseReleaseEvent(e)
	#enddef
#endclass