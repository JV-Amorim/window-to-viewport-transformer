from PySide6 import QtCore, QtGui, QtWidgets
from models.classes.line import Line
from models.classes.point_2d import Point2D
from models.classes.polygon import Polygon
from utils.font import get_custom_font


ITEMS_PER_FORM_ROW = 6
DIALOG_INSERT_TITLE = 'Insert Object'
DIALOG_UPDATE_TITLE = 'Update Object'


class ObjectInsertionDialog(QtWidgets.QDialog):
  onPointInserted = QtCore.Signal(Point2D)
  onLineInserted = QtCore.Signal(Line)
  onPolygonInserted = QtCore.Signal(Polygon)

  def __init__(self, objectPoints = None):
    super().__init__()
    self.isInUpdateMode = objectPoints is not None
    self.pointsOfTheObjectToUpdate = objectPoints
    self.setWindowProperties()
    self.initUI()

  def setWindowProperties(self):
    if self.isInUpdateMode:
      self.setWindowTitle(DIALOG_UPDATE_TITLE)
    else:
      self.setWindowTitle(DIALOG_INSERT_TITLE)
    self.setModal(True)
    self.setFixedSize(300, 270)

  def initUI(self):
    self.initFormContainer()
    self.initRowButtons()
    self.initForm()
    self.initInsertButton()
    
  def initFormContainer(self):
    self.formContainer = QtWidgets.QVBoxLayout()

    title = QtWidgets.QLabel()

    if self.isInUpdateMode:
      title.setText(DIALOG_UPDATE_TITLE)
    else:
      title.setText(DIALOG_INSERT_TITLE)

    title.setFont(get_custom_font('bold', 14))
    self.formContainer.addWidget(title)

    self.setLayout(self.formContainer)
    
  def initRowButtons(self):
    rowButtons = QtWidgets.QHBoxLayout()

    addPointButton = QtWidgets.QPushButton('Add Point')
    addPointButton.clicked.connect(self.insertFormRow)
    rowButtons.addWidget(addPointButton)

    resetButton = QtWidgets.QPushButton('Reset')
    resetButton.clicked.connect(self.resetForm)
    rowButtons.addWidget(resetButton)

    self.formContainer.addLayout(rowButtons)

  def initForm(self):
    self.formLayout = QtWidgets.QGridLayout()
    formLayoutWrapper = QtWidgets.QWidget()
    formLayoutWrapper.setLayout(self.formLayout)

    formScrollArea = QtWidgets.QScrollArea()
    formScrollArea.setWidget(formLayoutWrapper)
    formScrollArea.setFixedHeight(150)
    formScrollArea.setWidgetResizable(True)

    self.formContainer.addWidget(formScrollArea)

    if self.isInUpdateMode:
      for point in self.pointsOfTheObjectToUpdate:
        self.insertFormRow(point.x, point.y)
    else:
      self.insertFormRow()

  def initInsertButton(self):
    insertButton = QtWidgets.QPushButton()

    if self.isInUpdateMode:
      insertButton.setText('Update ✔')
    else:
      insertButton.setText('Insert ➕')

    insertButton.clicked.connect(self.insertObject)
    self.formContainer.addWidget(insertButton)

  def insertFormRow(self, xValue = 0, yValue = 0):
    newRowNumber = int(self.formLayout.count() / ITEMS_PER_FORM_ROW + 1)

    rowName = QtWidgets.QLabel(f'P{newRowNumber}')
    rowName.setFont(get_custom_font('bold'))
    self.formLayout.addWidget(rowName, newRowNumber, 0)

    xLabel = QtWidgets.QLabel('X')
    xLabel.setAlignment(QtGui.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    self.formLayout.addWidget(xLabel, newRowNumber, 1)

    xInput = QtWidgets.QDoubleSpinBox()
    xInput.setMinimum(-10000)
    xInput.setMaximum(10000)
    xInput.setValue(xValue)
    self.formLayout.addWidget(xInput, newRowNumber, 2)

    yLabel = QtWidgets.QLabel('Y')
    yLabel.setAlignment(QtGui.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    self.formLayout.addWidget(yLabel, newRowNumber, 3)

    yInput = QtWidgets.QDoubleSpinBox()
    yInput.setMinimum(-10000)
    yInput.setMaximum(10000)
    yInput.setValue(yValue)
    self.formLayout.addWidget(yInput, newRowNumber, 4)

    deleteButton = QtWidgets.QPushButton('❌')
    deleteButton.setFixedWidth(20)
    deleteButton.clicked.connect(lambda : self.deleteFormRow(newRowNumber))
    self.formLayout.addWidget(deleteButton, newRowNumber, 5)

  def deleteFormRow(self, rowToDelete):
    rangeStart = (rowToDelete - 1) * ITEMS_PER_FORM_ROW
    rangeEnd = (rowToDelete) * ITEMS_PER_FORM_ROW
    indexOfItemsToDelete = range(rangeStart, rangeEnd)

    for index in reversed(indexOfItemsToDelete):
      widgetToRemove = self.formLayout.takeAt(index).widget()
      widgetToRemove.setParent(None)

    remainingXValues = []
    remainingYValues = []

    for index in range(2, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      xInput = self.formLayout.itemAt(index).widget()
      remainingXValues.append(xInput.value())

    for index in range(4, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      yInput = self.formLayout.itemAt(index).widget()
      remainingYValues.append(yInput.value())

    self.clearForm()
    for index in range(len(remainingXValues)):
      self.insertFormRow(remainingXValues[index], remainingYValues[index])

  def clearForm(self):
    for index in reversed(range(self.formLayout.count())):
      widgetToRemove = self.formLayout.takeAt(index).widget()
      widgetToRemove.setParent(None)

  @QtCore.Slot()
  def resetForm(self):
    self.clearForm()
    self.insertFormRow()

  @QtCore.Slot()
  def insertObject(self):
    xValues = []
    yValues = []

    for index in range(2, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      xInput = self.formLayout.itemAt(index).widget()
      xValues.append(xInput.value())

    for index in range(4, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      yInput = self.formLayout.itemAt(index).widget()
      yValues.append(yInput.value())

    self.emitInsertion(xValues, yValues)
    self.resetForm()

  def emitInsertion(self, xValues, yValues):
    pointsCount = len(xValues)

    if pointsCount == 0:
      return

    elif pointsCount == 1:
      self.onPointInserted.emit(Point2D(xValues[0], yValues[0]))

    elif pointsCount == 2:
      p1 = Point2D(xValues[0], yValues[0])
      p2 = Point2D(xValues[1], yValues[1])
      self.onLineInserted.emit(Line(p1, p2))

    else:
      points = []
      for index in range(pointsCount):
        points.append(Point2D(xValues[index], yValues[index]))
      self.onPolygonInserted.emit(Polygon(points))
