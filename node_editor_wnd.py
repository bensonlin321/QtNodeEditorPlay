from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_scene import QDMGraphicsScene
from node_graphics_view import QDMGraphicsView
from node_scene import Scene
from node_node import Node
from node_socket import Socket
from node_edge import *

class NodeEditorWnd(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # create graphics scene
        self.scene = Scene()
        #self.grScene = QDMGraphicsScene(self.scene)
        
        self.addNodes()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.scene.setView(self.view)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")

        # test
        #self.addDebugContent(self.scene.grScene)

        self.show()

    def addNodes(self):
        node1 = Node(self.scene, "Adam", inputs=[0,2,3], outputs=[1])
        node1.setPos(-350, -250)
        node2 = Node(self.scene, "Benson", inputs=[0,4,5], outputs=[1])
        node2.setPos(150, -250)
        node3 = Node(self.scene, "New Node 3", inputs=[0,0,1], outputs=[1])
        node3.setPos(0, 0)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

    def addDebugContent(self, grScene):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        outlinePen2 = QPen(Qt.blue)
        outlinePen2.setWidth(5)

        rect = grScene.addRect(-200, -200, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)
        
        text = grScene.addText("This is a good text", QFont("Garamond"))
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 0.7, 1.0))
        text.setPos(0, -30)

        widget1 = QPushButton("Hello", self)
        proxy1 = grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        #self.layout.addWidget(widget1)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 80)

        line = grScene.addLine(-50, -50, -20, -20, outlinePen2)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
        print("Style loading: ", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

