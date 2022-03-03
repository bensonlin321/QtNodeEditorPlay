from node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self, secne, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):
        self.scene = secne
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.setConnectedEdge(self)
        if self.end_socket is not None:
            self.end_socket.setConnectedEdge(self)

        self.grEdge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()
        print("Edge: ", self.grEdge.posSource, "to", self.grEdge.posDestination)

        self.scene.grScene.addItem(self.grEdge)

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x() # offest: add node (widget) position
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x() # offest: add node (widget) position
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)

        print("Start Socket: ",self.start_socket)
        print("End Socket: ", self.end_socket)

        self.grEdge.update()

    def remove_from_socket(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_socket()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)
