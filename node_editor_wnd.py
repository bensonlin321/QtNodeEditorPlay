from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_scene import QDMGraphicsScene
from node_graphics_view import QDMGraphicsView
from node_scene import Scene

class NodeEditorWnd(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # create graphics scene
        #self.grScene = QDMGraphicsScene()
        self.scene = Scene()
        self.grScene = self.scene.grScene

        # create graphics view
        #self.view = QGraphicsView(self)
        #self.view.setScene(self.grScene)

        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")

        self.addDebugContent()

        self.show()



    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        outlinePen2 = QPen(Qt.blue)
        outlinePen2.setWidth(5)

        rect = self.grScene.addRect(-200, -200, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)
        
        text = self.grScene.addText("This is a good text", QFont("Garamond"))
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 0.7, 1.0))
        text.setPos(0, -30)

        widget1 = QPushButton("Hello", self)
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        #self.layout.addWidget(widget1)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 80)

        line = self.grScene.addLine(-50, -50, -20, -20, outlinePen2)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)


