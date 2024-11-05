from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF
from math import atan2, cos, sin

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

    def create_node(self, node_id, label, color="blue"):
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

        # Создание текстовой метки внутри узла, позиционированной по центру
        text = QGraphicsTextItem(label)
        text.setParentItem(ellipse)  # Установка метки в качестве дочернего элемента эллипса
        text.setDefaultTextColor(Qt.black)  # Цвет текста для контраста
        text.setPos(
        ellipse.rect().center().x() - text.boundingRect().width() / 2,
        ellipse.rect().center().y() - text.boundingRect().height() / 2
        )

        self.scene.addItem(ellipse)
        self.nodes[node_id] = (ellipse, text)

    def create_edge(self, start, end, weight=1):
        start_node = self.nodes.get(start)
        end_node = self.nodes.get(end)

        if not start_node or not end_node:
            raise ValueError("Both nodes must exist to create an edge.")

        if start == end:
            line = QGraphicsEllipseItem(start_node[0].rect().adjusted(15, 15, -15, -15))
            line.setPen(QPen(Qt.black, weight))
        else:
            line = QGraphicsLineItem()
            self.update_edge_position(line, start_node, end_node)

        line.setData(0, start)
        line.setData(1, end)
        line.setPen(QPen(self.edge_color, weight))
        line.setFlag(QGraphicsLineItem.ItemIsSelectable)

        self.scene.addItem(line)
        self.edges.append(line)

    def delete_node(self, node_id):
        if node_id not in self.nodes:
            return
        node, label = self.nodes.pop(node_id)
        self.scene.removeItem(node)
        for edge in self.edges[:]:
            if edge.data(0) == node_id or edge.data(1) == node_id:
                self.edges.remove(edge)
                self.scene.removeItem(edge)

    def delete_edge(self, start, end):
        for edge in self.edges[:]:
            if {edge.data(0), edge.data(1)} == {start, end}:
                self.edges.remove(edge)
                self.scene.removeItem(edge)
                break

    def update_edge_position(self, edge, start_node, end_node):
        if isinstance(edge, QGraphicsLineItem):
            edge.setLine(
                start_node[0].rect().center().x() + start_node[0].scenePos().x(),
                start_node[0].rect().center().y() + start_node[0].scenePos().y(),
                end_node[0].rect().center().x() + end_node[0].scenePos().x(),
                end_node[0].rect().center().y() + end_node[0].scenePos().y()
            )

    def update_edges(self):
        for edge in self.edges:
            start_id = edge.data(0)
            end_id = edge.data(1)
            start_node = self.nodes.get(start_id)
            end_node = self.nodes.get(end_id)
            if start_node and end_node:
                self.update_edge_position(edge, start_node, end_node)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsEllipseItem):
            self.selected_node = item
            self.offset = self.mapToScene(event.pos()) - item.scenePos()
            self.select_node(item)
        else:
            self.clear_selection()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_node:
            new_pos = self.mapToScene(event.pos()) - self.offset
            self.selected_node.setPos(new_pos)
            self.update_edges()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.selected_node = None
        super().mouseReleaseEvent(event)

    def select_node(self, node_item):
        for node, (ellipse, _) in self.nodes.items():
            if ellipse == node_item:
                ellipse.setPen(QPen(Qt.red, 2))
            else:
                ellipse.setPen(QPen(Qt.black, 1))

    def clear_selection(self):
        for node, (ellipse, _) in self.nodes.items():
            ellipse.setPen(QPen(Qt.black, 1))
        for edge in self.edges:
            edge.setPen(QPen(Qt.black, edge.pen().width()))

    
    def clear_graph(self):
        """Удаляет все узлы и рёбра с холста."""
        for node_id in list(self.nodes.keys()):
            self.delete_node(node_id)
        self.edges.clear()  # Очищает список рёбер
        self.update()  # Обновляет отображение холста