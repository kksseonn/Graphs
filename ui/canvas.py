# ui/canvas.py
from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem
)
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QTimer
from math import atan2, cos, sin
import networkx as nx


class Canvas(QGraphicsView):
    """Класс Canvas для визуализации и взаимодействия с графом."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.node_color = Qt.gray
        self.edge_color = Qt.black
        self.edge_thickness = 2
        self.scale_factor = 1.1
        self.mst_edge_color = Qt.blue
        self.shortest_path_color = QColor(0, 255, 0)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_graph)
        self.update_timer.start(20)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.graph = nx.Graph()

        self.nodes = {}
        self.edges = {}
        self.edge_labels = {}
        self.selected_node = None
        self.offset = QPointF()

    def create_node(self, node_id: str, label: str, color: str = "blue", position: tuple[float, float] = None):
        """Создаёт новый узел на холсте."""
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")

        if position is None:
            position = (50 * len(self.nodes), 50)

        self.graph.add_node(node_id, label=label, color=color, position=position)

        radius = 20
        x, y = position
        ellipse = QGraphicsEllipseItem(x, y, radius * 2, radius * 2)
        ellipse.setBrush(QBrush(QColor(color)))
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        ellipse.setData(0, node_id)
        ellipse.setAcceptHoverEvents(True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        text = QGraphicsTextItem(label)
        text.setParentItem(ellipse)
        text.setDefaultTextColor(Qt.black)
        text.setPos(
            ellipse.rect().center().x() - text.boundingRect().width() / 2,
            ellipse.rect().center().y() - text.boundingRect().height() / 2
        )

        self.scene.addItem(ellipse)
        self.nodes[node_id] = (ellipse, text)

        print(f"Node {node_id} created at position {position}")

    def delete_node(self, node_id: str):
        """Удаляет узел и все связанные с ним рёбра."""
        if node_id not in self.nodes:
            return

        edges_to_delete = [edge_key for edge_key in self.edges if node_id in edge_key]
        for edge_key in edges_to_delete:
            self.delete_edge(*edge_key)

        self.graph.remove_node(node_id)

        node, label = self.nodes.pop(node_id)
        self.scene.removeItem(node)

    def update_node_position(self, node_id: str):
        """Обновляет позицию узла в графе после его перемещения."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist.")

        node = self.nodes[node_id][0]
        position = node.pos()
        self.graph.nodes[node_id]['position'] = (position.x(), position.y())
        print(f"Позиция узла {node_id} обновлена на ({position.x()}, {position.y()})")

    def create_edge(self, start: str, end: str, weight: int = 1):
        """Создаёт новое ребро между двумя узлами."""
        if not (start in self.nodes and end in self.nodes):
            raise ValueError("Both nodes must exist to create an edge.")

        if self.graph.has_edge(start, end) or self.graph.has_edge(end, start):
            raise ValueError(f"Edge between {start} and {end} already exists.")

        self.graph.add_edge(start, end, weight=weight)

        start_node = self.nodes[start][0]
        end_node = self.nodes[end][0]

        if start == end:
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

        label = QGraphicsTextItem(str(weight))
        label.setDefaultTextColor(Qt.red)
        label.setFont(QFont("Arial", 12))
        self.scene.addItem(label)
        self.edge_labels[(start, end)] = label
        self.update_edge_label_position(edge, label, start_node, end_node)

        print(f"Ребро между {start} и {end} с весом {weight} добавлено.")

    def delete_edge(self, start: str, end: str):
        """Удаляет ребро между двумя узлами."""
        if not self.graph.has_edge(start, end):
            return

        self.graph.remove_edge(start, end)

        edge = self.edges.pop((start, end), None)
        if edge:
            self.scene.removeItem(edge)

        label = self.edge_labels.pop((start, end), None)
        if label:
            self.scene.removeItem(label)

    def update_edge_position(self, edge: QGraphicsLineItem, start_node: QGraphicsEllipseItem, end_node: QGraphicsEllipseItem):
        """Обновляет позицию ребра."""
        if isinstance(edge, QGraphicsLineItem):
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

    def update_edge_label_position(self, edge: QGraphicsLineItem, label: QGraphicsTextItem, start_node: QGraphicsEllipseItem, end_node: QGraphicsEllipseItem):
        """Обновляет позицию метки ребра."""
        if isinstance(edge, QGraphicsLineItem):
            line = edge.line()
            midpoint = QPointF(
                (line.x1() + line.x2()) / 2,
                (line.y1() + line.y2()) / 2
            )
            label.setPos(midpoint - QPointF(label.boundingRect().width() / 2, label.boundingRect().height() / 2))

    def update_edges(self):
        """Обновляет позиции всех рёбер."""
        for (start, end), edge in self.edges.items():
            start_node = self.nodes[start][0]
            end_node = self.nodes[end][0]
            self.update_edge_position(edge, start_node, end_node)
            self.update_edge_label_position(edge, self.edge_labels[(start, end)], start_node, end_node)

    def update_graph(self):
        """Метод, вызываемый таймером для обновления графа."""
        self.update_edges()
        self.scene.update()

    def mouseMoveEvent(self, event):
        """
        Обрабатывает перемещение мыши.
        Перемещает захваченный узел и обновляет связанные рёбра.
        """
        if self.selected_node:
            new_pos = self.mapToScene(event.pos()) - self.offset
            self.selected_node.setPos(new_pos)

            node_id = self.selected_node.data(0)

            for (start, end), edge in self.edges.items():
                if start == node_id or end == node_id:
                    start_node = self.nodes[start][0]
                    end_node = self.nodes[end][0]
                    self.update_edge_position(edge, start_node, end_node)
                    self.update_edge_label_position(edge, self.edge_labels[(start, end)], start_node, end_node)

            self.scene.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Обрабатывает отпускание ЛКМ.
        Завершает перемещение узла.
        """
        self.selected_node = None
        super().mouseReleaseEvent(event)

    def sync_all_node_positions(self):
        """Синхронизирует позиции всех узлов в графе."""
        for node_id, (node_item, _) in self.nodes.items():
            self.update_node_position(node_id)

    def highlight_mst(self, mst_edges):
        """
        Метод для выделения рёбер минимального остовного дерева (MST).
        :param mst_edges: Список рёбер минимального остовного дерева.
        """
        self.clear_highlighted_paths()
        for edge in mst_edges:
            if isinstance(edge, tuple) and len(edge) == 3:
                start, end, _ = edge
                if (start, end) in self.edges:
                    edge_item = self.edges[(start, end)]
                    edge_item.setPen(QPen(self.mst_edge_color, self.edge_thickness))
                elif (end, start) in self.edges:
                    edge_item = self.edges[(end, start)]
                    edge_item.setPen(QPen(self.mst_edge_color, self.edge_thickness))
            else:
                print(f"Некорректный элемент в mst_edges: {edge}")

        self.scene.update()

    def highlight_shortest_paths(self, distances, paths):
        """Выделяет кратчайшие пути на графе."""
        self.clear_highlighted_paths()

        for path in paths:
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]

                edge = self.edges.get((start, end)) or self.edges.get((end, start))

                if edge:
                    edge.setPen(QPen(self.shortest_path_color, self.edge_thickness * 2))

                start_node, _ = self.nodes.get(start, (None, None))
                end_node, _ = self.nodes.get(end, (None, None))

                if start_node:
                    start_node.setBrush(QBrush(Qt.yellow))
                if end_node:
                    end_node.setBrush(QBrush(Qt.yellow))

        self.repaint()

    def clear_highlighted_paths(self):
        """Сбрасывает выделение рёбер и узлов."""
        for edge in self.edges.values():
            edge.setPen(QPen(self.edge_color, self.edge_thickness))

        for node_id, (ellipse, _) in self.nodes.items():
            ellipse.setBrush(QBrush(self.node_color))

        self.repaint()

    def clear_graph(self):
        """Очищает весь граф и связанные элементы с холста."""
        for edge in list(self.edges.values()):
            self.scene.removeItem(edge)

        for label in self.edge_labels.values():
            self.scene.removeItem(label)

        for node, (ellipse, _) in self.nodes.items():
            self.scene.removeItem(ellipse)

        self.graph.clear()
        self.nodes.clear()
        self.edges.clear()
        self.edge_labels.clear()

        self.scene.update()
