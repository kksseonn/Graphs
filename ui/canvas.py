# ui/canvas.py
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF
from math import atan2, cos, sin
import networkx as nx

class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.node_color = Qt.gray
        self.edge_color = Qt.black
        self.edge_thickness = 2
        self.scale_factor = 1.1
        self.mst_edge_color = Qt.blue
        self.shortest_path_color = Qt.green
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.graph = nx.Graph()
        self.nodes = {}  # Хранение ссылок на узлы в графической сцене
        self.edges = {}  # Хранение ссылок на рёбра в графической сцене
        self.edge_labels = {}  # Хранение ссылок на текстовые метки рёбер
        self.selected_node = None
        self.offset = QPointF()

    def create_node(self, node_id, label, color="blue"):
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")

        # Добавление узла в NetworkX-граф
        self.graph.add_node(node_id, label=label, color=color)

        # Создание графического узла
        radius = 20
        x, y = 50 * len(self.nodes), 50

        ellipse = QGraphicsEllipseItem(x, y, radius * 2, radius * 2)
        ellipse.setBrush(QBrush(QColor(color)))
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        ellipse.setData(0, node_id)
        ellipse.setAcceptHoverEvents(True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        # Создание текстовой метки внутри узла
        text = QGraphicsTextItem(label)
        text.setParentItem(ellipse)
        text.setDefaultTextColor(Qt.black)
        text.setPos(
            ellipse.rect().center().x() - text.boundingRect().width() / 2,
            ellipse.rect().center().y() - text.boundingRect().height() / 2
        )

        self.scene.addItem(ellipse)
        self.nodes[node_id] = (ellipse, text)

    def create_edge(self, start, end, weight=1):
        if not (start in self.nodes and end in self.nodes):
            raise ValueError("Both nodes must exist to create an edge.")

        if self.graph.has_edge(start, end):
            raise ValueError(f"Edge between {start} and {end} already exists.")

        # Добавление ребра в NetworkX-граф
        self.graph.add_edge(start, end, weight=weight)

        # Создание графического ребра
        start_node = self.nodes[start][0]
        end_node = self.nodes[end][0]

        if start == end:
            # Петля (self-loop)
            rect = start_node.rect().adjusted(15, 15, -15, -15)
            edge = QGraphicsEllipseItem(rect)
            edge.setPen(QPen(self.edge_color, self.edge_thickness))
        else:
            edge = QGraphicsLineItem()
            self.update_edge_position(edge, start_node, end_node)
            edge.setPen(QPen(self.edge_color, self.edge_thickness))

        edge.setData(0, start)
        edge.setData(1, end)
        self.scene.addItem(edge)
        self.edges[(start, end)] = edge

        # Добавление текстовой метки веса ребра
        label = QGraphicsTextItem(str(weight))
        label.setDefaultTextColor(Qt.red)
        self.scene.addItem(label)
        self.edge_labels[(start, end)] = label
        self.update_edge_label_position(edge, label, start_node, end_node)

    def delete_node(self, node_id):
        if node_id not in self.nodes:
            return

        # Удаление узла из NetworkX-графа
        self.graph.remove_node(node_id)

        # Удаление графического узла
        node, label = self.nodes.pop(node_id)
        self.scene.removeItem(node)

        # Удаление всех связанных рёбер
        for edge_key in list(self.edges.keys()):
            if node_id in edge_key:
                self.delete_edge(*edge_key)

    def delete_edge(self, start, end):
        if not self.graph.has_edge(start, end):
            return

        # Удаление ребра из NetworkX-графа
        self.graph.remove_edge(start, end)

        # Удаление графического ребра
        edge = self.edges.pop((start, end), None)
        if edge:
            self.scene.removeItem(edge)

        # Удаление текстовой метки ребра
        label = self.edge_labels.pop((start, end), None)
        if label:
            self.scene.removeItem(label)

    def update_edge_position(self, edge, start_node, end_node):
        if isinstance(edge, QGraphicsLineItem):
            # Вычисление точек начала и конца ребра с учётом границы узлов
            start_center = start_node.scenePos() + start_node.rect().center()
            end_center = end_node.scenePos() + end_node.rect().center()

            angle = atan2(end_center.y() - start_center.y(), end_center.x() - start_center.x())
            start_offset = QPointF(cos(angle) * start_node.rect().width() / 2, sin(angle) * start_node.rect().height() / 2)
            end_offset = QPointF(cos(angle + 3.14) * end_node.rect().width() / 2, sin(angle + 3.14) * end_node.rect().height() / 2)

            edge.setLine(
                start_center.x() + start_offset.x(),
                start_center.y() + start_offset.y(),
                end_center.x() + end_offset.x(),
                end_center.y() + end_offset.y()
            )

    def update_edge_label_position(self, edge, label, start_node, end_node):
        if isinstance(edge, QGraphicsLineItem):
            line = edge.line()
            midpoint = QPointF(
                (line.x1() + line.x2()) / 2,
                (line.y1() + line.y2()) / 2
            )
            label.setPos(midpoint - QPointF(label.boundingRect().width() / 2, label.boundingRect().height() / 2))

    def update_edges(self):
        for (start, end), edge in self.edges.items():
            start_node = self.nodes[start][0]
            end_node = self.nodes[end][0]
            self.update_edge_position(edge, start_node, end_node)
            self.update_edge_label_position(edge, self.edge_labels[(start, end)], start_node, end_node)

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

            # Обновляем только те рёбра, которые связаны с перемещаемым узлом
            node_id = self.selected_node.data(0)
            for (start, end), edge in self.edges.items():
                if start == node_id or end == node_id:
                    start_node = self.nodes[start][0]
                    end_node = self.nodes[end][0]
                    self.update_edge_position(edge, start_node, end_node)
                    self.update_edge_label_position(edge, self.edge_labels[(start, end)], start_node, end_node)
            
            # Принудительное обновление сцены
            self.scene.update()

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
        for edge in self.edges.values():
            edge.setPen(QPen(self.edge_color, self.edge_thickness))

    def clear_graph(self):
        """Удаляет все узлы и рёбра с холста."""
        for node_id in list(self.nodes.keys()):
            self.delete_node(node_id)
        self.edges.clear()
        self.graph.clear()  # Очистка NetworkX-графа
        self.update()

    def move_node(self, node_id, x, y):
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist.")
        
        node, _ = self.nodes[node_id]
        print(f"Перемещение узла {node_id} в ({x}, {y})")  # Отладочное сообщение
        node.setPos(x, y)
        self.update_edges()  # Обновляем связанные рёбра

    def zoom_in(self):
        """Увеличивает масштаб холста."""
        self.scale(self.scale_factor, self.scale_factor)

    def zoom_out(self):
        """Уменьшает масштаб холста."""
        self.scale(1 / self.scale_factor, 1 / self.scale_factor)

    def reset_view(self):
        """Сбрасывает масштаб и центрирует вид."""
        self.resetTransform()
        self.centerOn(0, 0)
