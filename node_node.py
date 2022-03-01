from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget

class Node():
    def __init__(self, scene, title="Node"):
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        # change title
        #self.grNode.title = 'test title'

        self.inputs = []
        self.outputs = []


