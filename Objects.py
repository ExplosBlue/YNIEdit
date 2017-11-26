from PyQt5 import QtGui, QtCore, QtWidgets

import Renderer


class InitObject:
    def __init__(self, obj, view):
        self.objectItem = CreateObjectItem(obj)
        Renderer.RenderObjects(self.objectItem, view)


# Create an item for each object, this allows for the objects to be clicked
class CreateObjectItem(QtWidgets.QGraphicsItem):

    def __init__(self, obj):
        super(CreateObjectItem, self).__init__()

        self.obj = obj

        self.name = obj[0]
        self.xPos = obj[1] * 2.6
        self.yPos = obj[2] * 2.6

        self.objRect = (self.xPos - 13, -self.yPos - 13, 26, 26)

        # Allow for the object to be selected
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

        # Setup pens that will be used when drawing the object rects
        self.pen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.pen.setColor(QtCore.Qt.black)
        self.pen.setWidth(2)
        penWidth = self.pen.widthF()
        self.focusPen = QtGui.QPen(QtCore.Qt.DotLine)

        # Setup Brushes that will be used when drawing the object rects
        self.brush = QtGui.QBrush(QtGui.QColor(0, 90, 150, 150))
        self.focusBrush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 100))

        # Setup the rects ready to be passed to the painter
        self.rect = QtCore.QRectF(self.objRect[0], self.objRect[1], self.objRect[2], self.objRect[3])
        self.focusRect = QtCore.QRectF(self.objRect[0] - penWidth / 2, self.objRect[1] - penWidth / 2,
                                       self.objRect[2] + penWidth,
                                       self.objRect[3] + penWidth)

    # Select object
    def mousePressEvent(self, event):
        self.setSelected(True)
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

        print("selected: " + self.name + " at: X:" + str(self.rect.x()) + " Y:" + str(self.rect.y()))

    def boundingRect(self):
        return self.rect

    # Draw the rect
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)
        if self.isSelected():
            self.drawFocusRect(painter)

    # Draw a selection box around the rect
    def drawFocusRect(self, painter):
        self.focusPen.setColor(QtGui.QColor(255, 255, 255, 100))
        self.focusPen.setStyle(QtCore.Qt.DotLine)
        self.focusPen.setWidthF(2)
        painter.setBrush(self.focusBrush)
        painter.setPen(self.focusPen)
        painter.drawRect(self.focusRect)
