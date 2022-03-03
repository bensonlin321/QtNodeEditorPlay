from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent=None, socket_type=1):
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 3.0

        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF52e220"),
            QColor("#FF0056a6"),
            QColor("#FFa86db1"),
            QColor("#FFb54747"),
            QColor("#FFdbe220")
        ]

        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")
        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QstyleOptionGraphicsItem, widget=None):

        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        x = -self.radius
        y = -self.radius
        w = 2*self.radius
        h = 2*self.radius
        painter.drawEllipse(x, y, w, h)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )

