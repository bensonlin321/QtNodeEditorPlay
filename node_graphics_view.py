from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_socket import *
from node_graphics_edge import *
from node_edge import *
from node_graphics_cutline import QDMCutLine
import inspect

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10 # pixels

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.zoomInFactor = 1.25
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10] # min, max
        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.editingFlag = False

        # cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.setDragMode(QGraphicsView.RubberBandDrag)

    # mouse event

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    # use middle button to drag view
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)

        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        check = self.checkSocketModeForLeftMPress(event)
        if not check:
            super().mousePressEvent(event)


    def leftMouseButtonRelease(self, event):
        check = self.checkSocketModeForLeftMRelease(event)
        if not check:
            super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        if isinstance(item, QDMGraphicsEdge):
            print("RMB DEBUG:", item.edge, "connecting sockets:", item.edge.start_socket, "<-->", item.edge.end_socket)

        if type(item) is QDMGraphicsSocket: 
            print("RMB DEBUG:", item.socket, "has edge: ", item.socket.edge)

        if item is None:
            print("SCENE:")
            print("  Nodes:")
            for node in self.grScene.scene.nodes:
                print("    ", node)
            print("  Edges:")
            for edge in self.grScene.scene.edges:
                print("    ", edge)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)


    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        # draw dash line
        elif self.mode == MODE_EDGE_CUT:
            # check position
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        print("grView:: Key press:", event.key())
        if event.key() == Qt.Key_Delete:
            print(self.editingFlag)
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        # going through each item
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, "node"):
                item.node.remove()

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

        event.accept()

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    """ For Dragging Edge """
    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measure if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene_pos = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        print("distance on click & release:", dist_scene_pos)

        dsp_x = dist_scene_pos.x()
        dsp_y = dist_scene_pos.y()

        # If the user just click without moving
        # if mouse_has_not_moved_enough:
        # v(x, y) = x*x + y*y < threshold*threshold
        return (dsp_x*dsp_x + dsp_y*dsp_y) > EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        print("View::", inspect.currentframe().f_code.co_name, " End dragging edge")

        # if the end point is a socket
        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket:
                print("-> Assign End Socket: ", item.socket)

                # if the end socket already has an edge, remove it
                if item.socket.hasEdge():
                    item.socket.edge.remove()

                # remove the previous edge line if you point out to a new one
                if self.previousEdge is not None: self.previousEdge.remove()

                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.updatePositions()
                return True

        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge

        return False

    def edgeDragStart(self, item):
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                print("View::", inspect.currentframe().f_code.co_name, " Start dragging edge")
                print("-> Assign Start Socket")
                self.previousEdge = item.socket.edge
                self.last_start_socket = item.socket
                self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
                print("View::", inspect.currentframe().f_code.co_name, " dragEdge:", self.dragEdge)

                return True
        return False

    def isShiftPressed(self, event, item):
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                print("LMB + Shift on", item)
                event.ignore()
                # event.modifiers(): Qt.ShiftModifier, Qt.ControlModifier, Qt.AltModifier
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return True

    def isShiftReleased(self, event, item):
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge):
            if event.modifiers() & Qt.ShiftModifier:
                print("LMB Release + Shift on", item)
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return True


    def checkSocketModeForLeftMPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if self.isShiftPressed(event, item): return True

        if self.edgeDragStart(item): return True

        if self.mode == MODE_EDGE_DRAG:
            return self.edgeDragEnd(item)

        # cut edge
        if item is None:
            if event.modifiers() == Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return True

        return False

    def checkSocketModeForLeftMRelease(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        if self.isShiftReleased(event, item): return True

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                return self.edgeDragEnd(item)

        if self.mode == MODE_EDGE_CUT:
            # check all the edges in the scene
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return True

        return False

    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            # check each edge in scene
            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()
