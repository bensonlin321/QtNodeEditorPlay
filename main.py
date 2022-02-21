import sys
from PyQt5.QtWidgets import *
from node_editor_wnd import NodeEditorWnd

def Tutorial_0():
    label = QLabel("Hello, PyQt5!")
    label.show()

def Tutorial_1(app):
    wnd = NodeEditorWnd()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Tutorial_1(app)
