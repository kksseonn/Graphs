#ui/dialog_handler.py

from PyQt5.QtWidgets import QInputDialog, QMessageBox, QColorDialog, QAction, QDialog
from core import dijkstra, prim_mst, kamada_kawai_layout, serialize_graph, deserialize_graph
from utils.file_operations import save_to_file, load_from_file

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QDialog
import networkx as nx
from .dialogs import NodeDialog, EdgeDialog, MatrixDialog

class DialogHandler:
    """
    Класс для обработки диалогов и взаимодействия с пользователем.
    """

    def __init__(self, canvas, parent):
        self.canvas = canvas
        self.parent = parent

    def create_action(self, name, callback):
        """
        Создаёт объект QAction.
        """
        action = QAction(name, self.parent)
        action.triggered.connect(callback)
        return action

    def add_node(self):
        dialog = NodeDialog(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            node_data = dialog.get_data()
            try:
                self.canvas.create_node(node_data["id"], node_data["label"], node_data["color"])
            except ValueError as e:
                QMessageBox.warning(self.parent, "Ошибка", str(e))

    def remove_node(self):
        node_id, ok = QInputDialog.getText(self.parent, "Удаление узла", "Введите ID узла для удаления:")
        if ok:
            try:
                self.canvas.delete_node(node_id)
            except ValueError as e:
                QMessageBox.warning(self.parent, "Ошибка", str(e))

    def add_edge(self):
        node_ids = list(self.canvas.nodes.keys())
        if not node_ids:
            QMessageBox.warning(self.parent, "Ошибка", "Сначала добавьте хотя бы два узла.")
            return

        dialog = EdgeDialog(node_ids, self.parent)
        if dialog.exec_() == QDialog.Accepted:
            edge_data = dialog.get_data()
            try:
                self.canvas.create_edge(edge_data["start"], edge_data["end"], edge_data["weight"])
            except ValueError as e:
                QMessageBox.warning(self.parent, "Ошибка", str(e))

    def remove_edge(self):
        start, ok1 = QInputDialog.getText(self.parent, "Удаление ребра", "Введите ID начального узла:")
        if ok1:
            end, ok2 = QInputDialog.getText(self.parent, "Удаление ребра", "Введите ID конечного узла:")
            if ok2:
                try:
                    self.canvas.delete_edge(start, end)
                except ValueError as e:
                    QMessageBox.warning(self.parent, "Ошибка", str(e))

    def add_graph_from_matrix(self):
        try:
            # Шаг 1: Запрос количества узлов
            node_count, ok = QInputDialog.getInt(self.parent, "Количество узлов", "Введите количество узлов:")
            if not ok or node_count <= 0:
                return

            # Шаг 2: Диалог ввода матрицы
            dialog = MatrixDialog(node_count, self.parent)
            if dialog.exec() == QDialog.Accepted:
                matrix = dialog.matrix

                # Проверка матрицы (можно добавить настройку обработки самопетель)
                if any(len(row) != node_count for row in matrix):
                    QMessageBox.critical(self.parent, "Ошибка", "Матрица должна быть квадратной.")
                    return

                # Шаг 3: Создание графа
                self.canvas.clear_graph()
                for i in range(node_count):
                    self.canvas.create_node(str(i), f"Узел {i}", "#ADD8E6")

                for i in range(node_count):
                    for j in range(node_count):
                        if matrix[i][j] != 0:  # Самопетли добавляются, если `i == j`
                            try:
                                self.canvas.create_edge(str(i), str(j), float(matrix[i][j]))
                            except ValueError as e:
                                QMessageBox.warning(self.parent, "Ошибка", f"Некорректное значение ребра ({i}, {j}): {e}")

                QMessageBox.information(self.parent, "Матрица весов", "Граф успешно создан.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка создания графа: {e}")


    def save_graph(self):
        graph_data = serialize_graph(self.canvas)
        save_to_file(self.parent, graph_data)

    def load_graph(self):
        self.delete_graph()
        graph_data = load_from_file(self.parent)
        if not graph_data:
            return

        try:
            deserialize_graph(self.canvas, graph_data)
            self.canvas.update()
            QMessageBox.information(self.parent, "Загрузка", "Граф успешно загружен.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка загрузки графа: {e}")
    
    def delete_graph(self):
        """Очищаем граф на холсте."""
        self.canvas.clear_graph()  # Очистка данных и визуальных элементов
        self.canvas.update()  # Обновляем холст для применения изменений
        
    def change_node_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_node_color(color)

    def change_edge_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_edge_color(color)

    def run_dijkstra(self):
        # Запрашиваем начальный узел
        start_node, ok = QInputDialog.getText(self.parent, "Алгоритм Дейкстры", "Введите начальный узел:")
        if ok and start_node in self.canvas.nodes:
            # Запрашиваем конечный узел
            end_node, ok = QInputDialog.getText(self.parent, "Алгоритм Дейкстры", "Введите конечный узел:")

            if ok and end_node in self.canvas.nodes:
                # Выполнение алгоритма Дейкстры для поиска кратчайшего пути от start_node до end_node
                distance, path = dijkstra(self.canvas, start_node, end_node)
                print(f"Distance: {distance}")
                print(f"Path: {path}")
                self.canvas.highlight_shortest_paths(distance, path)  # Выделение кратчайшего пути
            else:
                # Если конечный узел не найден или не был введён
                QMessageBox.warning(self.parent, "Ошибка", "Конечный узел не существует или не был введён.")


    def run_prim(self):
        mst_edges = prim_mst(self.canvas)
        self.canvas.highlight_mst(mst_edges)

    def run_kamada_kawai(self):
        try:
            # Проверка связности графа
            if not self.canvas.graph or not nx.is_connected(self.canvas.graph):
                QMessageBox.warning(self.parent, "Ошибка", "Граф должен быть связным для выполнения алгоритма Камада-Кавай.")
                return

            # Обновление NetworkX-графа
            self.canvas.graph.clear()
            for node_id in self.canvas.nodes:
                self.canvas.graph.add_node(node_id)
            for (start, end), edge in self.canvas.edges.items():
                self.canvas.graph.add_edge(start, end)

            # Применение алгоритма Камада-Кавай
            layout = kamada_kawai_layout(self.canvas)
            max_x = max(x for x, _ in layout.values())
            max_y = max(y for _, y in layout.values())
            for node_id, (x, y) in layout.items():
                scaled_x = (x / max_x) * 100  # Нормализация
                scaled_y = (y / max_y) * 100
                self.canvas.move_node(node_id, scaled_x, scaled_y)

            self.canvas.scene.update()
            QMessageBox.information(self.parent, "Камада-Кавай", "Расположение узлов выполнено.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка алгоритма Камада-Кавай: {e}")

