# # ui/main_window.py

# from PyQt5.QtWidgets import QMainWindow, QMenuBar, QToolBar, QAction, QVBoxLayout, QWidget
# from ui.canvas import Canvas

# from PyQt5.QtWidgets import QMessageBox
# from ui.input_dialogs import NodeDialog, EdgeDialog

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Графовое приложение")
#         self.setGeometry(100, 100, 800, 600)

#         # Создаём основной виджет и макет
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout()
#         self.central_widget.setLayout(self.layout)

#         # Инициализируем Canvas для отображения графа
#         self.canvas = Canvas()
#         self.layout.addWidget(self.canvas)

#         # Создаём меню и панель инструментов
#         self.create_menu()
#         self.create_toolbar()

#     def create_menu(self):
#         # Создаем меню и добавляем действия
#         menubar = self.menuBar()

#         # Меню "Файл"
#         file_menu = menubar.addMenu("Файл")
#         save_action = QAction("Сохранить", self)
#         load_action = QAction("Загрузить", self)
#         file_menu.addAction(save_action)
#         file_menu.addAction(load_action)

#         # Меню "Правка"
#         edit_menu = menubar.addMenu("Правка")
#         add_node_action = QAction("Добавить узел", self)
#         remove_node_action = QAction("Удалить узел", self)
#         add_edge_action = QAction("Добавить ребро", self)
#         remove_edge_action = QAction("Удалить ребро", self)
#         edit_menu.addAction(add_node_action)
#         edit_menu.addAction(remove_node_action)
#         edit_menu.addAction(add_edge_action)
#         edit_menu.addAction(remove_edge_action)

#         # Подключаем действия к методам
#         add_node_action.triggered.connect(self.canvas.add_node)
#         remove_node_action.triggered.connect(self.canvas.remove_node)
#         add_edge_action.triggered.connect(self.canvas.add_edge)
#         remove_edge_action.triggered.connect(self.canvas.remove_edge)

#     def create_toolbar(self):
#         # Создаём панель инструментов
#         toolbar = QToolBar("Панель инструментов")
#         self.addToolBar(toolbar)

#         # Добавляем кнопки на панель инструментов
#         add_node_action = QAction("Добавить узел", self)
#         remove_node_action = QAction("Удалить узел", self)
#         add_edge_action = QAction("Добавить ребро", self)
#         remove_edge_action = QAction("Удалить ребро", self)

#         toolbar.addAction(add_node_action)
#         toolbar.addAction(remove_node_action)
#         toolbar.addAction(add_edge_action)
#         toolbar.addAction(remove_edge_action)

#         # Подключаем действия к методам
#         add_node_action.triggered.connect(self.canvas.add_node)
#         remove_node_action.triggered.connect(self.canvas.remove_node)
#         add_edge_action.triggered.connect(self.canvas.add_edge)
#         remove_edge_action.triggered.connect(self.canvas.remove_edge)

#     def add_node(self):
#         # Открытие диалога для добавления узла
#         dialog = NodeDialog(self)
#         if dialog.exec_() == QDialog.Accepted:
#             node_data = dialog.get_data()
#             try:
#                 # Передача данных в Canvas
#                 self.canvas.create_node(node_data["id"], node_data["label"], node_data["color"])
#             except ValueError as e:
#                 # Отображение ошибки, если ID узла уже существует
#                 QMessageBox.warning(self, "Ошибка", str(e))

#     def add_edge(self):
#         # Открытие диалога для добавления ребра
#         node_ids = list(self.canvas.nodes.keys())
#         if not node_ids:
#             QMessageBox.warning(self, "Ошибка", "Сначала добавьте хотя бы два узла.")
#             return

#         dialog = EdgeDialog(node_ids, self)
#         if dialog.exec_() == QDialog.Accepted:
#             edge_data = dialog.get_data()
#             try:
#                 # Передача данных в Canvas
#                 self.canvas.create_edge(edge_data["start"], edge_data["end"], edge_data["weight"])
#             except ValueError as e:
#                 # Отображение ошибки, если что-то пошло не так
#                 QMessageBox.warning(self, "Ошибка", str(e))

# ui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QMenuBar, QToolBar, QAction, QGraphicsView, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.canvas import Canvas
from ui.input_dialogs import NodeDialog, EdgeDialog
from core.algorithms import dijkstra, prim_mst
from core.data_storage import serialize_graph, deserialize_graph
from utils.file_operations import save_to_file, load_from_file
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

        # Меню "Алгоритмы"
        algorithms_menu = menu_bar.addMenu("Алгоритмы")
        # Добавление опции для алгоритма Дейкстры
        dijkstra_action = QAction("Поиск кратчайшего пути", self)
        dijkstra_action.triggered.connect(self.run_dijkstra)
        algorithms_menu.addAction(dijkstra_action)

        # Добавление опции для алгоритма Прима
        prim_action = QAction("Минимальное остовное дерево", self)
        prim_action.triggered.connect(self.run_prim)
        algorithms_menu.addAction(prim_action)
         # Добавление опции "Сохранить"
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)

        # Добавление опции "Загрузить"
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_graph)
        file_menu.addAction(load_action)
        # Меню "Правка" с добавлением узлов и рёбер
        edit_menu = menu_bar.addMenu("Правка")
        add_node_action = QAction("Добавить узел", self)
        add_node_action.triggered.connect(self.add_node)
        edit_menu.addAction(add_node_action)

        add_edge_action = QAction("Добавить ребро", self)
        add_edge_action.triggered.connect(self.add_edge)
        edit_menu.addAction(add_edge_action)

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

        # Кнопка "Добавить ребро"
        add_edge_action = QAction(QIcon(), "Добавить ребро", self)
        add_edge_action.triggered.connect(self.add_edge)
        tool_bar.addAction(add_edge_action)

    def add_node(self):
        # Открытие диалога для добавления узла
        dialog = NodeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            node_data = dialog.get_data()
            try:
                # Передача данных в Canvas
                self.canvas.create_node(node_data["id"], node_data["label"], node_data["color"])
            except ValueError as e:
                # Отображение ошибки, если ID узла уже существует
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
                # Передача данных в Canvas
                self.canvas.create_edge(edge_data["start"], edge_data["end"], edge_data["weight"])
            except ValueError as e:
                # Отображение ошибки, если что-то пошло не так
                QMessageBox.warning(self, "Ошибка", str(e))
    def run_dijkstra(self):
        start_node, ok = QInputDialog.getText(self, "Алгоритм Дейкстры", "Введите начальный узел:")
        if ok and start_node in self.canvas.nodes:
            distances, _ = dijkstra(self.canvas, start_node)
            self.canvas.highlight_shortest_paths(distances)

    def run_prim(self):
        mst_edges = prim_mst(self.canvas)
        self.canvas.highlight_mst(mst_edges)

    def save_graph(self):
        """Сохраняет текущий граф в файл."""
        graph_data = serialize_graph(self.canvas)
        save_to_file(self, graph_data)

    def load_graph(self):
        """Загружает граф из файла и обновляет визуализацию."""
        graph_data = load_from_file(self)
        if graph_data:
            try:
                deserialize_graph(self.canvas, graph_data)
                self.canvas.update()  # Обновление отображения после загрузки
                QMessageBox.information(self, "Загрузка", "Граф успешно загружен.")
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Ошибка", "Файл повреждён или содержит неверные данные.")