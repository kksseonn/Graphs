from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF

class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.node_color = Qt.gray
        self.edge_color = Qt.black
        self.scale_factor = 1.1
        self.mst_edge_color = Qt.blue
        self.shortest_path_color = Qt.green
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.nodes = {}
        self.edges = []

        self.selected_node = None
        self.offset = QPointF()

    def wheelEvent(self, event):
        """Handles zooming with the mouse wheel."""
        scale_factor = self.scale_factor if event.angleDelta().y() > 0 else 1 / self.scale_factor
        self.scale(scale_factor, scale_factor)

    def mousePressEvent(self, event):
        """Handles node selection and dragging with the mouse."""
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsEllipseItem):
            self.selected_node = item
            self.offset = self.mapToScene(event.pos()) - item.scenePos()
            self.select_node(item)
        else:
            self.clear_selection()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handles node dragging."""
        if self.selected_node:
            new_pos = self.mapToScene(event.pos()) - self.offset
            self.selected_node.setPos(new_pos)
            self.update_edges()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Resets selection after dragging."""
        self.selected_node = None
        super().mouseReleaseEvent(event)

    def create_node(self, node_id, label, color="blue"):
        """Creates a node with the given ID, label, and color."""
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")
        
        radius = 20
        x, y = 50 * len(self.nodes), 50

        ellipse = QGraphicsEllipseItem(x, y, radius * 2, radius * 2)
        ellipse.setBrush(QBrush(QColor(color)))
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        ellipse.setData(0, node_id)
        ellipse.setAcceptHoverEvents(True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        text = QGraphicsTextItem(label)
        text.setPos(x + radius / 2, y + radius / 2)

        self.scene.addItem(ellipse)
        self.scene.addItem(text)
        self.nodes[node_id] = (ellipse, text)

    def create_edge(self, start, end, weight=1):
        """Creates an edge between the specified start and end nodes with the given weight."""
        start_node = self.nodes.get(start)
        end_node = self.nodes.get(end)
        if not start_node or not end_node:
            raise ValueError("Both start and end nodes must exist to create an edge.")

        line = QGraphicsLineItem(
            start_node[0].rect().center().x() + start_node[0].scenePos().x(),
            start_node[0].rect().center().y() + start_node[0].scenePos().y(),
            end_node[0].rect().center().x() + end_node[0].scenePos().x(),
            end_node[0].rect().center().y() + end_node[0].scenePos().y()
        )
        line.setData(0, start)
        line.setData(1, end)
        line.setPen(QPen(self.edge_color, weight))
        line.setFlag(QGraphicsLineItem.ItemIsSelectable)

        self.scene.addItem(line)
        self.edges.append(line)

    def select_node(self, node_item):
        """Highlights the selected node."""
        for node, (ellipse, _) in self.nodes.items():
            ellipse.setPen(QPen(Qt.red, 2) if ellipse == node_item else QPen(Qt.black, 1))

    def clear_selection(self):
        """Removes selection from all nodes and edges."""
        for node, (ellipse, _) in self.nodes.items():
            ellipse.setPen(QPen(Qt.black, 1))
        for edge in self.edges:
            edge.setPen(QPen(self.edge_color, edge.pen().width()))

    def update_edges(self):
        """Updates the positions of edges connected to nodes."""
        for edge in self.edges:
            start_id, end_id = edge.data(0), edge.data(1)
            start_node, end_node = self.nodes.get(start_id), self.nodes.get(end_id)
            if start_node and end_node:
                edge.setLine(
                    start_node[0].rect().center().x() + start_node[0].scenePos().x(),
                    start_node[0].rect().center().y() + start_node[0].scenePos().y(),
                    end_node[0].rect().center().x() + end_node[0].scenePos().x(),
                    end_node[0].rect().center().y() + end_node[0].scenePos().y()
                )

    def set_node_color(self, color):
        """Sets the color of all nodes on the canvas."""
        self.node_color = color
        for node_id, (ellipse, _) in self.nodes.items():
            ellipse.setBrush(QBrush(self.node_color))

    def set_edge_color(self, color):
        """Sets the color of all edges on the canvas."""
        self.edge_color = color
        for edge in self.edges:
            edge.setPen(QPen(self.edge_color, edge.pen().width()))
