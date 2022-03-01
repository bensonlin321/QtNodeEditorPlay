from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMNodeContentWidget(QWidget):
    def __init__(self, parnet=None):
        super().__init__(parnet)
        self._padding = 50

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_title_label = QLabel("Widget Title")
        self.layout.addWidget(self.wdg_title_label)
        self.layout.addWidget(QTextEdit("foo"))