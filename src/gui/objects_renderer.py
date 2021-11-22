from PySide6 import QtCore, QtGui, QtWidgets


class ObjectsRenderer(QtWidgets.QWidget):
  def __init__(self, viewportDict, windowDict, isToDrawCoordinates):
    super().__init__()
    self.viewportDict, self.windowDict = viewportDict, windowDict
    self.isToDrawCoordinates = isToDrawCoordinates
    self.viewport = windowDict['viewport']
    self.setWidgetSize()
    self.setBackgroundColor()
    print('Objects rendered.')

  def setWidgetSize(self):
    width = self.viewport.get_width()
    height = self.viewport.get_height()
    self.setFixedSize(QtCore.QSize(width, height))

  def setBackgroundColor(self):
    palette = self.palette()
    palette.setColor(self.backgroundRole(), QtGui.Qt.black)
    self.setPalette(palette)
    self.setAutoFillBackground(True)

  def paintEvent(self, event):
    self.drawViewportLimits()
    self.drawIndividualPoints()
    self.drawLines()
    self.drawPolygons()

  def drawViewportLimits(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.white)
    painter.setPen(pen)

    qtPoint1 = QtCore.QPointF(self.viewport.min_point.x, self.viewport.min_point.y)
    qtPoint2 = QtCore.QPointF(self.viewport.max_point.x, self.viewport.min_point.y)
    qtPoint3 = QtCore.QPointF(self.viewport.max_point.x, self.viewport.max_point.y)
    qtPoint4 = QtCore.QPointF(self.viewport.min_point.x, self.viewport.max_point.y)

    qtLine1 = QtCore.QLineF(qtPoint1, qtPoint2)
    qtLine2 = QtCore.QLineF(qtPoint2, qtPoint3)
    qtLine3 = QtCore.QLineF(qtPoint3, qtPoint4)
    qtLine4 = QtCore.QLineF(qtPoint4, qtPoint1)
    
    painter.drawLine(qtLine1)
    painter.drawLine(qtLine2)
    painter.drawLine(qtLine3)
    painter.drawLine(qtLine4)

    qtTextPoint = QtCore.QPointF(self.viewport.min_point.x + 5, self.viewport.min_point.y + 12)
    self.drawText(painter, qtTextPoint, 'VIEWPORT LIMITS')

  def drawText(self, painter, qtPoint, text):
    painter.setFont(QtGui.QFont('Arial', 7))
    painter.drawText(qtPoint, text)

  def drawIndividualPoints(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.green)
    painter.setPen(pen)

    for point in self.viewportDict['individual_points']:
      qtPoint = QtCore.QPointF(point.x, point.y)
      painter.drawPoint(qtPoint)
      self.drawCoordinatesText(painter, qtPoint)

  def drawLines(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.cyan)
    painter.setPen(pen)

    for line in self.viewportDict['lines']:
      if line.completely_clipped:
        continue
      qtPoint1 = QtCore.QPointF(line.point_1.x_clipped, line.point_1.y_clipped)
      qtPoint2 = QtCore.QPointF(line.point_2.x_clipped, line.point_2.y_clipped)
      qtLine = QtCore.QLineF(qtPoint1, qtPoint2)
      painter.drawLine(qtLine)
      self.drawCoordinatesText(painter, qtPoint1)
      self.drawCoordinatesText(painter, qtPoint2)

  def drawPolygons(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.magenta)
    painter.setPen(pen)

    for polygon in self.viewportDict['polygons']:
      qtPolygon = QtGui.QPolygonF()
      for point in polygon.get_points():
        qtPoint = QtCore.QPointF(point.x, point.y)
        qtPolygon.append(qtPoint)
        self.drawCoordinatesText(painter, qtPoint)
      painter.drawPolygon(qtPolygon)
  
  def drawCoordinatesText(self, painter, qtPoint):
    if not self.isToDrawCoordinates: return

    x, y = qtPoint.x(), qtPoint.y()
    tooltipPoint = QtCore.QPointF(x + 5, y + 10)
    self.drawText(painter, tooltipPoint, f'({x:.1f}, {y:.1f})')
