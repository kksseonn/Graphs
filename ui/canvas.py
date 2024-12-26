# ui/canvas.py
from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem
)
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from math import atan2, cos, sin
import networkx as nx


class Canvas(QGraphicsView):
    """Класс Canvas для визуализации и взаимодействия с графом."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Параметры отображения
        self.node_color = Qt.gray
        self.edge_color = Qt.black
        self.edge_thickness = 2
        self.scale_factor = 1.1
        self.mst_edge_color = Qt.blue
        self.shortest_path_color = QColor(0, 255, 0)
        
        # Таймер обновления
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_graph)
        self.update_timer.start(20)  # Обновление каждые 20 мс

        # Сцена и граф
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.graph = nx.Graph()

        # Внутренние структуры
        self.nodes = {}  # {node_id: (ellipse_item, text_item)}
        self.edges = {}  # {(start, end): edge_item}
        self.edge_labels = {}  # {(start, end): text_item}
        self.selected_node = None
        self.offset = QPointF()

    # --- Методы для узлов ---
    def create_node(self, node_id: str, label: str, color: str = "blue", position: tuple[float, float] = None):
        """Создаёт новый узел на холсте."""
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")

        # Если позиция не передана, установим по умолчанию
        if position is None:
            position = (50 * len(self.nodes), 50)

        # Добавление узла в NetworkX-граф с атрибутом позиции
        self.graph.add_node(node_id, label=label, color=color, position=position)

        # Создание графического узла
        radius = 20
        x, y = position
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

        # Логирование для отладки
        print(f"Node {node_id} created at position {position}")
    
    def delete_node(self, node_id: str):
        """Удаляет узел и все связанные с ним рёбра."""
        if node_id not in self.nodes:
            return

        # Удаление всех связанных рёбер
        edges_to_delete = [edge_key for edge_key in self.edges if node_id in edge_key]
        for edge_key in edges_to_delete:
            self.delete_edge(*edge_key)

        # Удаление узла из NetworkX-графа
        self.graph.remove_node(node_id)

        # Удаление графического узла
        node, label = self.nodes.pop(node_id)
        self.scene.removeItem(node)


    def update_node_position(self, node_id: str):
        """Обновляет позицию узла в графе после его перемещения."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist.")

        node = self.nodes[node_id][0]  # Получаем графический элемент узла
        position = node.pos()  # Получаем текущую позицию графического узла
        # Обновляем позицию в NetworkX графе
        self.graph.nodes[node_id]['position'] = (position.x(), position.y())
        print(f"Позиция узла {node_id} обновлена на ({position.x()}, {position.y()})")

# --- Методы для рёбер ---
    def create_edge(self, start: str, end: str, weight: int = 1):
        if not (start in self.nodes and end in self.nodes):
            raise ValueError("Both nodes must exist to create an edge.")

        # Для неориентированного графа проверяем оба направления
        if self.graph.has_edge(start, end) or self.graph.has_edge(end, start):
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

        # Добавление текстовой метки веса ребра с увеличенным шрифтом
        label = QGraphicsTextItem(str(weight))
        label.setDefaultTextColor(Qt.red)
        label.setFont(QFont("Arial", 12))  # Устанавливаем шрифт и размер
        self.scene.addItem(label)
        self.edge_labels[(start, end)] = label
        self.update_edge_label_position(edge, label, start_node, end_node)

        # Отладка
        print(f"Ребро между {start} и {end} с весом {weight} добавлено.")

    def delete_edge(self, start: str, end: str):
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

    def update_edge_position(self, edge: QGraphicsLineItem, start_node: QGraphicsEllipseItem, end_node: QGraphicsEllipseItem):
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

    def update_edge_label_position(self, edge: QGraphicsLineItem, label: QGraphicsTextItem, start_node: QGraphicsEllipseItem, end_node: QGraphicsEllipseItem):
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

    def update_graph(self):
        """Метод, вызываемый таймером для обновления графа."""
        self.update_edges()
        self.scene.update()

    # --- Методы управления сценой ---
    def mouseMoveEvent(self, event):
        """
        Обрабатывает перемещение мыши.
        Перемещает захваченный узел и обновляет связанные рёбра.
        """
        if self.selected_node:
            # Вычисляем новую позицию узла
            new_pos = self.mapToScene(event.pos()) - self.offset
            self.selected_node.setPos(new_pos)

            # Получаем ID перемещаемого узла
            node_id = self.selected_node.data(0)

            # Обновляем только связанные рёбра
            for (start, end), edge in self.edges.items():
                if start == node_id or end == node_id:
                    start_node = self.nodes[start][0]
                    end_node = self.nodes[end][0]
                    self.update_edge_position(edge, start_node, end_node)  # Обновляем рёбра
                    self.update_edge_label_position(edge, self.edge_labels[(start, end)], start_node, end_node)  # Обновляем метки

            # Принудительное обновление сцены для отображения изменений
            self.scene.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Обрабатывает отпускание ЛКМ.
        Завершает перемещение узла.
        """
        self.selected_node = None  # Сбрасываем выбранный узел
        super().mouseReleaseEvent(event)

    def sync_all_node_positions(self):
        """Синхронизирует позиции всех узлов в графе."""
        for node_id, (node_item, _) in self.nodes.items():
            self.update_node_position(node_id)

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
            raise ValueError(f"Узел с ID {node_id} не найден.")
        node, _ = self.nodes[node_id]
        node.setPos(x, y)
        self.update_node_position(node_id)
        self.update_edges()  # Обновляем связанные рёбра

    def highlight_mst(self, mst_edges):
        """
        Метод для выделения рёбер минимального остовного дерева (MST).
        :param mst_edges: Список рёбер минимального остовного дерева.
        """
        self.clear_highlighted_paths()
        for edge in mst_edges:
            if isinstance(edge, tuple) and len(edge) == 3:
                start, end, _ = edge
                # Проверяем, есть ли такое ребро в графе
                if (start, end) in self.edges:
                    edge_item = self.edges[(start, end)]
                    edge_item.setPen(QPen(self.mst_edge_color, self.edge_thickness))
                elif (end, start) in self.edges:  # Проверка для ребра в другом порядке
                    edge_item = self.edges[(end, start)]
                    edge_item.setPen(QPen(self.mst_edge_color, self.edge_thickness))
            else:
                print(f"Некорректный элемент в mst_edges: {edge}")

        # Принудительное обновление сцены после изменений
        self.scene.update()

    def highlight_shortest_paths(self, distances, paths):
        self.clear_highlighted_paths()

        for path in paths:
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]

                edge = self.edges.get((start, end)) or self.edges.get((end, start))

                if edge:
                    edge.setPen(QPen(self.shortest_path_color, self.edge_thickness * 2))  # Подсвечиваем ребро

                start_node, _ = self.nodes.get(start, (None, None))
                end_node, _ = self.nodes.get(end, (None, None))

                if start_node:
                    start_node.setBrush(QBrush(Qt.yellow))  # Подсвечиваем начальный узел
                if end_node:
                    end_node.setBrush(QBrush(Qt.yellow))  # Подсвечиваем конечный узел

        self.repaint()  # Используем repaint для обновления сцены

    def clear_highlighted_paths(self):
        # Сбрасываем подсветку рёбер
        for edge in self.edges.values():
            edge.setPen(QPen(self.edge_color, self.edge_thickness))  # Возвращаем стандартный цвет и толщину

        # Сбрасываем подсветку узлов
        for node_id, (ellipse, _) in self.nodes.items():
            ellipse.setBrush(QBrush(self.node_color))  # Возвращаем стандартный цвет узлов

        self.repaint()  # Перерисовываем сцену

    def clear_graph(self):
        """Очищает весь граф и связанные элементы с холста."""
        # Удаляем все рёбра
        for edge in list(self.edges.values()):
            self.scene.removeItem(edge)  # Удаляем рёбра с холста

        # Удаляем все метки веса рёбер
        for label in self.edge_labels.values():
            self.scene.removeItem(label)  # Удаляем метки с холста

        # Удаляем все узлы
        for node, (ellipse, _) in self.nodes.items():
            self.scene.removeItem(ellipse)  # Удаляем узлы с холста

        # Очищаем NetworkX-граф
        self.graph.clear()

        # Очищаем внутренние структуры данных
        self.nodes.clear()
        self.edges.clear()
        self.edge_labels.clear()

        # Принудительное обновление холста
        self.scene.update()

