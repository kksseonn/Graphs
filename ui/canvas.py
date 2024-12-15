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
        self.shortest_path_color = QColor(0, 255, 0)
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

        # Добавление текстовой метки веса ребра
        label = QGraphicsTextItem(str(weight))
        label.setDefaultTextColor(Qt.red)
        self.scene.addItem(label)
        self.edge_labels[(start, end)] = label
        self.update_edge_label_position(edge, label, start_node, end_node)

        # Отладка
        print(f"Ребро между {start} и {end} с весом {weight} добавлено.")


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

    def highlight_mst(self, mst_edges):
        """
        Метод для выделения рёбер минимального остовного дерева (MST).
        :param mst_edges: Список рёбер минимального остовного дерева.
        """
        self.clear_highlighted_paths()
        for edge in mst_edges:
            if isinstance(edge, tuple) and len(edge) == 3:
                start, end, data = edge
                # Проверяем, есть ли такое ребро в графе
                if (start, end) in self.edges:
                    edge_item = self.edges[(start, end)]
                    # Меняем цвет ребра на синий (или другой цвет для MST)
                    edge_item.setPen(QPen(self.mst_edge_color, self.edge_thickness))
                    # Если есть метка для этого ребра, меняем её цвет
                    # label = self.edge_labels.get((start, end))
                    # if label:
                    #     label.setDefaultTextColor(self.mst_edge_color)
                elif (end, start) in self.edges:  # Проверка для ребра в другом порядке
                    edge_item = self.edges[(end, start)]
                    edge_item.setPen(QPen(self.mst_edge_color, self.edge_thickness))
                    # label = self.edge_labels.get((end, start))
                    # if label:
                    #     label.setDefaultTextColor(self.mst_edge_color)
            else:
                print(f"Некорректный элемент в mst_edges: {edge}")

        # Принудительное обновление сцены после изменений
        self.scene.update()

    def highlight_shortest_paths(self, distances, paths):
        self.clear_highlighted_paths()
        print("Paths:", paths)

        for path in paths:
            print(f"Highlighting path: {path}")
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                print(f"Highlighting edge from {start} to {end}")

                edge = self.edges.get((start, end)) or self.edges.get((end, start))
                
                if edge:
                    print(f"Edge found between {start} and {end}")
                    edge.setPen(QPen(self.shortest_path_color, self.edge_thickness * 2))  # Подсвечиваем ребро
                else:
                    print(f"Edge not found between {start} and {end}")

                start_node, _ = self.nodes.get(start, (None, None))
                end_node, _ = self.nodes.get(end, (None, None))

                if start_node:
                    print(f"Highlighting node {start}")
                    start_node.setBrush(QBrush(Qt.yellow))  # Подсвечиваем начальный узел
                if end_node:
                    print(f"Highlighting node {end}")
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
        """Очищаем граф на холсте."""
        # Удаляем все рёбра
        for edge in list(self.edges.values()):
            self.scene.removeItem(edge)  # Удаляем ребра с сцены

        # Удаляем все метки веса рёбер
        for edge, label in self.edge_labels.items():
            self.scene.removeItem(label)  # Удаляем метку с сцены

        # Удаляем все узлы
        for node_id, (ellipse, _) in list(self.nodes.items()):
            self.scene.removeItem(ellipse)  # Удаляем узлы с сцены

        # Очищаем внутренние структуры данных
        self.nodes.clear()
        self.edges.clear()
        self.edge_labels.clear()  # Очистка меток веса рёбер

        self.update()  # Обновляем холст
