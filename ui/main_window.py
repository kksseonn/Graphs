# ui/main_window.py

import json
from PyQt5.QtWidgets import (
    QMainWindow, QMenuBar, QToolBar, QAction, QGraphicsView, 
    QMessageBox, QDialog, QInputDialog, QColorDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ui.canvas import Canvas
from ui.input_dialogs import NodeDialog, EdgeDialog
from core.algorithms import dijkstra, prim_mst, kamada_kawai_layout
from core.data_storage import serialize_graph, deserialize_graph
from utils.file_operations import save_to_file, load_from_file

class MainWindow(QMainWindow):
    """
    Главное окно приложения для работы с графами.
    """

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
        """
        Создаёт строку меню с основными функциями.
        """
        menu_bar = QMenuBar(self)

        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.create_action("Выход", self.close))
        file_menu.addAction(self.create_action("Сохранить", self.save_graph))
        file_menu.addAction(self.create_action("Загрузить", self.load_graph))

        # Меню "Алгоритмы"
        algorithms_menu = menu_bar.addMenu("Алгоритмы")
        algorithms_menu.addAction(self.create_action("Поиск кратчайшего пути", self.run_dijkstra))
        algorithms_menu.addAction(self.create_action("Минимальное остовное дерево", self.run_prim))
        algorithms_menu.addAction(self.create_action("Расположение Камада-Кавай", self.run_kamada_kawai))

        # Меню "Правка"
        edit_menu = menu_bar.addMenu("Правка")
        edit_menu.addAction(self.create_action("Добавить узел", self.add_node))
        edit_menu.addAction(self.create_action("Удалить узел", self.remove_node))
        edit_menu.addAction(self.create_action("Добавить ребро", self.add_edge))
        edit_menu.addAction(self.create_action("Удалить ребро", self.remove_edge))
        edit_menu.addAction(self.create_action("Добавить граф по матрице весов", self.add_graph_from_matrix))
        edit_menu.addAction(self.create_action("Добавить граф по матрице смежности", self.add_graph_from_matrix))

        # Меню "Настройки"
        settings_menu = menu_bar.addMenu("Настройки")
        settings_menu.addAction(self.create_action("Цвет узлов", self.change_node_color))
        settings_menu.addAction(self.create_action("Цвет рёбер", self.change_edge_color))

        self.setMenuBar(menu_bar)

    def create_tool_bar(self):
        """
        Создаёт панель инструментов для быстрого доступа к функциям.
        """
        tool_bar = QToolBar("Инструменты", self)
        self.addToolBar(Qt.TopToolBarArea, tool_bar)

        tool_bar.addAction(self.create_action("Добавить узел", self.add_node))
        tool_bar.addAction(self.create_action("Удалить узел", self.remove_node))
        tool_bar.addAction(self.create_action("Добавить ребро", self.add_edge))
        tool_bar.addAction(self.create_action("Удалить ребро", self.remove_edge))

    def create_action(self, name, callback):
        """
        Вспомогательный метод для создания QAction.

        Args:
            name (str): Название действия.
            callback (callable): Функция, вызываемая при активации действия.

        Returns:
            QAction: Созданное действие.
        """
        action = QAction(name, self)
        action.triggered.connect(callback)
        return action

    def add_node(self):
        """
        Открывает диалог для добавления нового узла.
        """
        dialog = NodeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            node_data = dialog.get_data()
            try:
                self.canvas.create_node(node_data["id"], node_data["label"], node_data["color"])
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def remove_node(self):
        """
        Удаляет узел с заданным ID после подтверждения.
        """
        node_id, ok = QInputDialog.getText(self, "Удаление узла", "Введите ID узла для удаления:")
        if ok:
            try:
                self.canvas.delete_node(node_id)
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def add_edge(self):
        """
        Открывает диалог для добавления нового ребра между существующими узлами.
        """
        node_ids = list(self.canvas.nodes.keys())
        if not node_ids:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте хотя бы два узла.")
            return

        dialog = EdgeDialog(node_ids, self)
        if dialog.exec_() == QDialog.Accepted:
            edge_data = dialog.get_data()
            try:
                self.canvas.create_edge(edge_data["start"], edge_data["end"], edge_data["weight"])
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def remove_edge(self):
        """
        Удаляет ребро между двумя узлами после подтверждения.
        """
        start, ok1 = QInputDialog.getText(self, "Удаление ребра", "Введите ID начального узла:")
        if ok1:
            end, ok2 = QInputDialog.getText(self, "Удаление ребра", "Введите ID конечного узла:")
            if ok2:
                try:
                    self.canvas.delete_edge(start, end)
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))

    def add_graph_from_matrix(self):
        """
        Создаёт граф на основе введённой матрицы весов.
        """
        text, ok = QInputDialog.getMultiLineText(
            self,
            "Матрица весов",
            "Введите матрицу весов (через пробелы, строки разделены переносом строки):",
        )
        if not ok or not text.strip():
            return

        try:
            matrix = [
                list(map(float, row.split()))
                for row in text.strip().split("\n")
            ]
            size = len(matrix)
            if not all(len(row) == size for row in matrix):
                raise ValueError("Матрица должна быть квадратной.")

            self.canvas.clear_graph()

            for i in range(size):
                self.canvas.create_node(str(i), f"Узел {i}", "#ADD8E6")

            for i in range(size):
                for j in range(size):
                    if matrix[i][j] != 0 and i != j:
                        self.canvas.create_edge(str(i), str(j), matrix[i][j])

            QMessageBox.information(self, "Матрица весов", "Граф успешно создан.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Некорректный ввод матрицы: {e}")

    def run_dijkstra(self):
        """
        Запускает алгоритм Дейкстры для поиска кратчайших путей.
        """
        start_node, ok = QInputDialog.getText(self, "Алгоритм Дейкстры", "Введите начальный узел:")
        if ok and start_node in self.canvas.nodes:
            distances, _ = dijkstra(self.canvas, start_node)
            self.canvas.highlight_shortest_paths(distances)

    def run_prim(self):
        """
        Запускает алгоритм Прима для построения минимального остовного дерева.
        """
        mst_edges = prim_mst(self.canvas)
        self.canvas.highlight_mst(mst_edges)

    def save_graph(self):
        # Сохранение графа в файл
        graph_data = serialize_graph(self.canvas)
        save_to_file(self, graph_data)

    def load_graph(self):
        # Загрузка графа из файла
        graph_data = load_from_file(self)
        if not graph_data:
            return  # Выход, если загрузка файла была отменена

        try:
            deserialize_graph(self.canvas, graph_data)
            self.canvas.update()  # Обновление сцены для отображения загруженных элементов
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

    def run_kamada_kawai(self):
        # Вызываем алгоритм Камада-Кавай
        try:
            layout = kamada_kawai_layout(self.canvas)
            for node_id, (x, y) in layout.items():
                self.canvas.move_node(node_id, x, y)  # Метод для перемещения узлов
            self.canvas.update()  # Обновление сцены
            QMessageBox.information(self, "Камада-Кавай", "Расположение узлов выполнено.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить алгоритм Камада-Кавай: {e}")