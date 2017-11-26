import sys
from PyQt5 import QtGui, QtCore, QtWidgets

import Reader
import Renderer
import Objects


# TODO: Allow for selection of collision ect
# TODO: Create a widget to allow for object parameters to be edited
# TODO: Allow selecting levels from a dialog
# TODO: Allow for stuff to be saved
# TODO: Allow for the paths to the param & stage folders to be user specified

# Setup the window
class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.zoomLabel = QtWidgets.QLabel("Current Zoom: 100%")
        self.view = ViewArea()
        self.zoom = ZoomWidget()

        self.initUI()

    # Setup the ui
    def initUI(self):
        self.resize(1280, 720)
        self.center()
        # Put a real title here when I think of something to name this
        self.setWindowTitle('Yoshi\'s new Island Editor')

        # Set up initial ui layout
        vLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(vLayout)

        # Placeholder for where Obj editor widget will go
        label = QtWidgets.QLabel("Placeholder")

        # Place View and Editor widgets into horizontal layout
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(label)
        hLayout.addWidget(self.view)

        # Setup Zoom widget
        # noinspection PyUnresolvedReferences
        self.zoom.valueChanged.connect(self.ZoomAdjust)

        zoomLayout = QtWidgets.QHBoxLayout()
        zoomLayout.addWidget(self.zoom)
        zoomLayout.addWidget(self.zoomLabel)

        # Place everything into the vertical layout
        vLayout.addLayout(hLayout)
        vLayout.addLayout(zoomLayout)

        # Load level data
        filename = input("input a level name: ")
        levelData = Reader.LoadLevelData(filename)

        # Render Stuff
        # Render Collision
        for col in range(0, len(levelData.Data[0])):
            Renderer.RenderCollision(levelData.Data[0][col], self.view)

        # Render Objects
        for obj in range(0, len(levelData.Data[1])):
            Objects.InitObject(levelData.Data[1][obj], self.view)

        # Render Areas
        for area in range(0, len(levelData.Data[2])):
            Renderer.RenderAreas(levelData.Data[2][area], self.view)

        # Render Paths
        for path in range(0, len(levelData.Data[3])):
            Renderer.RenderPaths(levelData.Data[3][path], self.view)

        self.setWindowTitle('Yoshi\'s new Island Editor | ' + filename)

    # Allows window to be moved to the center of the screen
    def center(self):
        windowRect = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        windowRect.moveCenter(centerPoint)
        self.move(windowRect.topLeft())

    # Allows for the zoom slider to change the scale of the view widget
    @QtCore.pyqtSlot(int)
    def ZoomAdjust(self):
        zoomLevels = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
        zoomFactor = zoomLevels[self.zoom.value()]

        self.view.resetTransform()
        self.view.scale(zoomFactor, zoomFactor)
        self.zoomLabel.setText("Current Zoom: %.0f%%" % (100 * zoomFactor))


# Create a graphics view that can be drawn too
class ViewArea(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        QtWidgets.QGraphicsView.__init__(self, parent)

        # Create graphics scene
        self.scene = QtWidgets.QGraphicsScene()
        self.setBackgroundBrush(QtGui.QColor(119, 136, 153))

        # Setup Size Policy
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        # Setup Scrollbars
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # self.scene.setSceneRect(-40000, -40000, 80000, 80000)

        self.setScene(self.scene)

    def AddItem(self, item):
        self.scene.addItem(item)
        self.update()


# Create a slider widget that can be used to adjust the zoom of the view area
class ZoomWidget(QtWidgets.QSlider):
    def __init__(self, parent=None):
        QtWidgets.QSlider.__init__(self, parent)

        self.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setMaximum(6)
        self.setValue(2)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setMaximumWidth(500)


# Run stuff
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
