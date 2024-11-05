# ui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QMenuBar, QToolBar, QAction, QGraphicsView, QMessageBox, QDialog, QInputDialog, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.canvas import Canvas
from ui.input_dialogs import NodeDialog, EdgeDialog
from core.algorithms import dijkstra, prim_mst
from core.data_storage import serialize_graph, deserialize_graph
from utils.file_operations import save_to_file, load_from_file
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Установка заголовка и размеров окна
        self.setWindowTitle("Редактор графов")
        self.setGeometry(100, 100, 800, 600)

        # Инициализация холста для графа
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        # Создание меню и панели инструментов
        self.create_menu_bar()
        self.create_tool_bar()

    def create_menu_bar(self):
        # Создание строки меню
        menu_bar = QMenuBar(self)

        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Добавление опции "Сохранить"
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)

        # Добавление опции "Загрузить"
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_graph)
        file_menu.addAction(load_action)

        # Меню "Алгоритмы"
        algorithms_menu = menu_bar.addMenu("Алгоритмы")
        
        # Алгоритм Дейкстры
        dijkstra_action = QAction("Поиск кратчайшего пути", self)
        dijkstra_action.triggered.connect(self.run_dijkstra)
        algorithms_menu.addAction(dijkstra_action)

        # Алгоритм Прима
        prim_action = QAction("Минимальное остовное дерево", self)
        prim_action.triggered.connect(self.run_prim)
        algorithms_menu.addAction(prim_action)

        # Меню "Правка" с добавлением узлов и рёбер
        edit_menu = menu_bar.addMenu("Правка")

        add_node_action = QAction("Добавить узел", self)
        add_node_action.triggered.connect(self.add_node)
        edit_menu.addAction(add_node_action)

        remove_node_action = QAction("Удалить узел", self)
        remove_node_action.triggered.connect(self.remove_node)
        edit_menu.addAction(remove_node_action)

        add_edge_action = QAction("Добавить ребро", self)
        add_edge_action.triggered.connect(self.add_edge)
        edit_menu.addAction(add_edge_action)

        remove_edge_action = QAction("Удалить ребро", self)
        remove_edge_action.triggered.connect(self.remove_edge)
        edit_menu.addAction(remove_edge_action)

        # Меню "Настройки"
        settings_menu = menu_bar.addMenu("Настройки")

        # Настройка цвета узлов
        node_color_action = QAction("Цвет узлов", self)
        node_color_action.triggered.connect(self.change_node_color)
        settings_menu.addAction(node_color_action)

        # Настройка цвета рёбер
        edge_color_action = QAction("Цвет рёбер", self)
        edge_color_action.triggered.connect(self.change_edge_color)
        settings_menu.addAction(edge_color_action)

        # Установка строки меню
        self.setMenuBar(menu_bar)

    def create_tool_bar(self):
        # Создание панели инструментов
        tool_bar = QToolBar("Инструменты", self)
        self.addToolBar(Qt.TopToolBarArea, tool_bar)

        # Кнопка "Добавить узел"
        add_node_action = QAction(QIcon(), "Добавить узел", self)
        add_node_action.triggered.connect(self.add_node)
        tool_bar.addAction(add_node_action)

        # Кнопка "Удалить узел"
        remove_node_action = QAction("Удалить узел", self)
        remove_node_action.triggered.connect(self.remove_node)
        tool_bar.addAction(remove_node_action)

        # Кнопка "Добавить ребро"
        add_edge_action = QAction(QIcon(), "Добавить ребро", self)
        add_edge_action.triggered.connect(self.add_edge)
        tool_bar.addAction(add_edge_action)

        # Кнопка "Удалить ребро"
        remove_edge_action = QAction("Удалить ребро", self)
        remove_edge_action.triggered.connect(self.remove_edge)
        tool_bar.addAction(remove_edge_action)

    def add_node(self):
        # Открытие диалога для добавления узла
        dialog = NodeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            node_data = dialog.get_data()
            try:
                # Добавление узла на холст
                self.canvas.create_node(node_data["id"], node_data["label"], node_data["color"])
            except ValueError as e:
                # Отображение ошибки, если ID узла уже существует
                QMessageBox.warning(self, "Ошибка", str(e))

    def remove_node(self):
        # Открытие диалога для удаления узла
        node_id, ok = QInputDialog.getText(self, "Удаление узла", "Введите ID узла для удаления:")
        if ok:
            try:
                # Удаление узла с холста
                self.canvas.delete_node(node_id)
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def add_edge(self):
        # Открытие диалога для добавления ребра
        node_ids = list(self.canvas.nodes.keys())
        if not node_ids:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте хотя бы два узла.")
            return

        dialog = EdgeDialog(node_ids, self)
        if dialog.exec_() == QDialog.Accepted:
            edge_data = dialog.get_data()
            try:
                # Добавление ребра на холст
                self.canvas.create_edge(edge_data["start"], edge_data["end"], edge_data["weight"])
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def remove_edge(self):
        # Открытие диалога для удаления ребра
        start, ok1 = QInputDialog.getText(self, "Удаление ребра", "Введите ID начального узла:")
        if ok1:
            end, ok2 = QInputDialog.getText(self, "Удаление ребра", "Введите ID конечного узла:")
            if ok2:
                try:
                    # Удаление ребра с холста
                    self.canvas.delete_edge(start, end)
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))

    def run_dijkstra(self):
        # Диалог для запуска алгоритма Дейкстры
        start_node, ok = QInputDialog.getText(self, "Алгоритм Дейкстры", "Введите начальный узел:")
        if ok and start_node in self.canvas.nodes:
            distances, _ = dijkstra(self.canvas, start_node)
            self.canvas.highlight_shortest_paths(distances)

    def run_prim(self):
        # Запуск алгоритма Прима
        mst_edges = prim_mst(self.canvas)
        self.canvas.highlight_mst(mst_edges)

    def save_graph(self):
        # Сохранение графа в файл
        graph_data = serialize_graph(self.canvas)
        save_to_file(self, graph_data)

    def load_graph(self):
        # Загрузка графа из файла
        graph_data = load_from_file(self)
        if graph_data:
            try:
                deserialize_graph(self.canvas, graph_data)
                self.canvas.update()
                QMessageBox.information(self, "Загрузка", "Граф успешно загружен.")
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Ошибка", "Файл повреждён или содержит неверные данные.")

    def change_node_color(self):
        # Диалог для изменения цвета узлов
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_node_color(color)

    def change_edge_color(self):
        # Диалог для изменения цвета рёбер
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_edge_color(color)
