from PyQt5 import QtGui, QtCore, QtWidgets


# Renderer for collision data
class RenderCollision:
    def __init__(self, col, view):
        x1 = col[0] * 2.6
        y1 = col[1] * 2.6
        x2 = col[2] * 2.6
        y2 = col[3] * 2.6

        line = QtWidgets.QGraphicsLineItem(x1, -y1, x2, -y2)
        view.AddItem(line)


# Renderer for object data
class RenderObjects:
    def __init__(self, objectItem, view):

        view.AddItem(objectItem)


# Renderer for Area data
class RenderAreas:
    def __init__(self, area, view):
        x = area[1] * 2.6
        y = area[2] * 2.6
        width = area[3] * 2.6
        height = area[4] * 2.6

        rect = QtWidgets.QGraphicsRectItem(x, -y, width, height)
        rect.setBrush(QtGui.QBrush(QtGui.QColor(85, 80, 185, 50), QtCore.Qt.SolidPattern))
        view.AddItem(rect)


# Renderer for Path data
class RenderPaths:
    def __init__(self, path, view):
        for i in range(0, len(path[1]) - 1):
            x1 = path[1][i][0] * 2.6
            y1 = path[1][i][1] * 2.6
            x2 = path[1][i + 1][0] * 2.6
            y2 = path[1][i + 1][1] * 2.6

            line = QtWidgets.QGraphicsLineItem(x1, -y1, x2, -y2)
            pen = QtGui.QPen(QtGui.QColor(0, 255, 20))
            pen.setWidth(2)
            line.setPen(pen)
            view.AddItem(line)
