from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF

class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация сцены и основных параметров
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Настройка графов
        self.nodes = {}  # Словарь для хранения узлов
        self.edges = []  # Список для хранения рёбер

        # Переменные для перетаскивания узлов
        self.selected_node = None
        self.offset = QPointF()

    def create_node(self, node_id, label, color="blue"):
        """Создаёт узел с заданными параметрами."""
        if node_id in self.nodes:
            raise ValueError(f"Узел с идентификатором {node_id} уже существует.")

        # Создание узла в виде эллипса
        radius = 20
        x, y = 50 * len(self.nodes), 50  # Расположение узлов для начала

        ellipse = QGraphicsEllipseItem(x, y, radius * 2, radius * 2)
        ellipse.setBrush(QBrush(QColor(color)))
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsMovable)  # Разрешаем перемещение

        # Установка действия на щелчок
        ellipse.setData(0, node_id)  # Сохранение ID узла для обработки событий
        ellipse.setAcceptHoverEvents(True)
        ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable)  # Выделение узла

        # Создание текстовой метки
        text = QGraphicsTextItem(label)
        text.setPos(x + radius / 2, y + radius / 2)

        # Добавление элементов на сцену
        self.scene.addItem(ellipse)
        self.scene.addItem(text)

        # Добавление узла в словарь
        self.nodes[node_id] = (ellipse, text)

    def create_edge(self, start, end, weight=1):
        """Создаёт ребро между узлами start и end с заданным весом."""
        start_node = self.nodes.get(start)
        end_node = self.nodes.get(end)

        if not start_node or not end_node:
            raise ValueError("Указанные узлы должны существовать для добавления ребра.")

        # Создание линии между узлами
        line = QGraphicsLineItem(
            start_node[0].rect().center().x() + start_node[0].scenePos().x(),
            start_node[0].rect().center().y() + start_node[0].scenePos().y(),
            end_node[0].rect().center().x() + end_node[0].scenePos().x(),
            end_node[0].rect().center().y() + end_node[0].scenePos().y()
        )
        pen = QPen(Qt.black, weight)  # Толщина линии соответствует весу
        line.setPen(pen)
        line.setFlag(QGraphicsLineItem.ItemIsSelectable)

        # Добавление линии на сцену
        self.scene.addItem(line)
        self.edges.append(line)

    def mousePressEvent(self, event):
        """Обрабатывает событие нажатия мыши."""
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsEllipseItem):
            self.selected_node = item
            self.offset = self.mapToScene(event.pos()) - item.scenePos()
            self.select_node(item)
        else:
            self.clear_selection()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Обрабатывает событие перемещения мыши для перетаскивания узлов."""
        if self.selected_node:
            new_pos = self.mapToScene(event.pos()) - self.offset
            self.selected_node.setPos(new_pos)
            self.update_edges()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Сбрасывает выбор узла при отпускании кнопки мыши."""
        self.selected_node = None
        super().mouseReleaseEvent(event)

    def select_node(self, node_item):
        """Выделяет выбранный узел изменением цвета рамки."""
        for node, (ellipse, _) in self.nodes.items():
            if ellipse == node_item:
                ellipse.setPen(QPen(Qt.red, 2))  # Выделение красным цветом
            else:
                ellipse.setPen(QPen(Qt.black, 1))

    def clear_selection(self):
        """Снимает выделение со всех узлов и рёбер."""
        for node, (ellipse, _) in self.nodes.items():
            ellipse.setPen(QPen(Qt.black, 1))
        for edge in self.edges:
            edge.setPen(QPen(Qt.black, edge.pen().width()))

    def update_edges(self):
        """Обновляет положение рёбер при перемещении узлов."""
        for edge in self.edges:
            start_id = edge.data(0)
            end_id = edge.data(1)
            start_node = self.nodes.get(start_id)
            end_node = self.nodes.get(end_id)
            if start_node and end_node:
                edge.setLine(
                    start_node[0].rect().center().x() + start_node[0].scenePos().x(),
                    start_node[0].rect().center().y() + start_node[0].scenePos().y(),
                    end_node[0].rect().center().x() + end_node[0].scenePos().x(),
                    end_node[0].rect().center().y() + end_node[0].scenePos().y()
                )
    def highlight_shortest_paths(self, distances):
            """Подсвечивает узлы и рёбра, которые лежат на кратчайших путях."""
            for node, distance in distances.items():
                if distance < float('inf'):
                    self.nodes[node][0].setBrush(QBrush(Qt.green))  # Подсветка узлов

            # Здесь можно добавить подсветку рёбер, используя данные о предыдущих узлах

    def highlight_mst(self, mst_edges):
        """Подсвечивает рёбра, которые входят в минимальное остовное дерево."""
        for start, end, weight in mst_edges:
            for edge in self.edges:
                if {edge.data(0), edge.data(1)} == {start, end}:
                    edge.setPen(QPen(Qt.blue, 2))  # Подсветка рёбер в МОД