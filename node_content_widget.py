from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMNodeContentWidget(QWidget):
    def __init__(self, node, parnet=None):
        super().__init__(parnet)
        self._padding = 50
        self.node = node

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_title_label = QLabel("Widget Title")
        self.layout.addWidget(self.wdg_title_label)
        self.layout.addWidget(QDMTextEdit("foo"))

    def setEditingFlag(self, value):
        self.node.scene.grScene.view.editingFlag = value

class QDMTextEdit(QTextEdit):
    def focusInEvent(self, event):
        print("focusInEvent")
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        print("focusOutEvent")
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)

