from PyQt5.QtCore import QCoreApplication, QRect, QRectF, QPointF, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def _(*args, **kwargs): return QCoreApplication.translate('Selector', *args, **kwargs)

class Selector(QDialog):
	def __init__(self, x, y, width, height, pixmap):
		super().__init__()
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
		self.view.setSceneRect(0, 0, width, height)

		self.bounds = QRect(x, y, width, height)
		self.rubber = OccultingRubberband(self, QColor(100,100,100,140), QColor('red'), 15,
			'Select an area using the mouse.\nPress Enter to take a screenshot or Esc to exit.',
			 QColor(28,28,28,220), QColor(150,150,150,240))
		self.rubber.setGeometry(0, 0, width, height)
	#enddef

	def showEvent(self, e):
		self.raise_()
		self.setGeometry(self.bounds)
		self.repaint()
		self.activateWindow()
		#self.setWindowState(Qt.WindowFullScreen)
	#enddef

	def keyReleaseEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
			raise Exception()
		#endif

		super().keyReleaseEvent(event)
	#enddef
#endclass

class OccultingRubberband(QGraphicsView):
	''' Implementation of a rubber band that grays out area around the selection '''
	def __init__(self, parent, occultColor, lineColor, handleSize, helpText, textBgColor, textColor):
		super().__init__(parent)
		self.setCursor(Qt.OpenHandCursor)

		self.selectionStart, self.selectionEnd = None, None

		self.theScene = QGraphicsScene(self)
		self.setStyleSheet("QGraphicsView { border-style: none; background-color: transparent;}")
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.selectionView = QGraphicsItemGroup()
		self.theScene.addItem(self.selectionView)

		self.occulting = [QGraphicsRectItem() for i in range(4)]
		for o in self.occulting:
			o.setBrush(QBrush(occultColor))
			o.setPen(QPen(Qt.NoPen))
			o.setCursor(Qt.CrossCursor)
			self.selectionView.addToGroup(o)
		#endfor

		self.lines = [QGraphicsLineItem() for i in range(4)]
		for l, cursor in zip(self.lines, [Qt.SizeHorCursor, Qt.SizeVerCursor]*2):
			l.setPen(QPen(lineColor, 2))
			l.setCursor(cursor)
			self.selectionView.addToGroup(l)
		#endfor

		self.corners = [QGraphicsRectItem() for i in range(4)]
		for c, cursor in zip(self.corners, [Qt.SizeFDiagCursor, Qt.SizeBDiagCursor]*2):
			c.setBrush(QBrush(occultColor))
			c.setPen(QPen(lineColor, 2))
			c.setCursor(cursor)
			self.selectionView.addToGroup(c)
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
		self.moving = self.drawing = self.resizing = False
	#enddef

	def selection(self):
		if self.selectionStart is None or self.selectionEnd is None: return None
		if self.selectionStart.x() == self.selectionEnd.x(): return None
		if self.selectionStart.y() == self.selectionEnd.y(): return None

		selRect = QRectF(QPointF(self.selectionStart), QPointF(self.selectionEnd)).normalized()

		return selRect.intersected(QRectF(self.geometry())) # So we can't go outside the bounds
	#enddef

	def _updateLayout(self):
		geo = self.geometry()

		selection = self.selection()

		if selection is None:
			self.selectionView.setVisible(False)
			self.noSelectionOverlay.setVisible(True)
		else:
			leftBound = selection.x() - geo.x()
			rightBound = leftBound + selection.width()
			topBound = selection.y() - geo.y()
			bottomBound = topBound + selection.height()

			left, top, right, bottom = self.occulting
			left.setRect(geo.x(), geo.y(), leftBound, geo.height())
			top.setRect(leftBound, geo.y(), selection.width(), topBound)
			right.setRect(rightBound, geo.x(), geo.width() - rightBound, geo.height())
			bottom.setRect(leftBound, bottomBound, selection.width(), geo.height() - bottomBound)

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
		geo = QRectF(self.geometry())
		self.setSceneRect(geo)
		self.drawingOverlay.setRect(geo)
		self.noSelectionHighlight.setRect(geo)

		hr = self.helpOverlay.boundingRect()
		hr.moveCenter(geo.center())
		self.helpOverlay.setPos(hr.x(), hr.y())

		self._updateLayout()
	#enddef

	def mousePressEvent(self, e):
		pos = e.pos()
		self.moving = self.drawing = self.resizing = False

		if self.selection() is None or any(r.contains(pos) for r in self.occulting):
			self.helpOverlay.setVisible(False)
			self.drawingOverlay.setVisible(True)
			self.drawingOverlay.setZValue(10)
			self.drawing = True
			self.selectionStart = self.selectionEnd = pos
		#endif
	#enddef

	def mouseMoveEvent(self, e):
		if self.drawing:
			self.selectionEnd = e.pos()
			self._updateLayout()
		#endif

		super().mouseMoveEvent(e)
	#enddef

	def mouseReleaseEvent(self, e):
		if self.drawing:
			self.drawingOverlay.setVisible(False)

		self.moving = self.drawing = self.resizing = False

		self._updateLayout()
	#enddef
#endclass