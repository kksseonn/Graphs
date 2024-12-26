#ui/dialog_handler.py
import time
from PyQt5.QtWidgets import (
    QInputDialog, QMessageBox, QAction, QDialog
)
import networkx as nx
from core import (
    dijkstra, prim_mst, kamada_kawai_layout,
    serialize_graph, deserialize_graph,
    force_directed_layout, spring_layout
)
from utils.file_operations import save_to_file, load_from_file
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
        """Добавляет новый узел в граф."""
        dialog = NodeDialog(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            node_data = dialog.get_data()
            try:
                self.canvas.create_node(node_data["id"], node_data["label"], node_data["color"])
            except ValueError as e:
                QMessageBox.warning(self.parent, "Ошибка", str(e))

    def remove_node(self):
        """Удаляет узел из графа."""
        node_id, ok = QInputDialog.getText(self.parent, "Удаление узла", "Введите ID узла для удаления:")
        if ok:
            try:
                self.canvas.delete_node(node_id)
            except ValueError as e:
                QMessageBox.warning(self.parent, "Ошибка", str(e))

    def add_edge(self):
        """Добавляет новое ребро между узлами."""
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
        """Удаляет ребро из графа."""
        start, ok1 = QInputDialog.getText(self.parent, "Удаление ребра", "Введите ID начального узла:")
        if ok1:
            end, ok2 = QInputDialog.getText(self.parent, "Удаление ребра", "Введите ID конечного узла:")
            if ok2:
                try:
                    self.canvas.delete_edge(start, end)
                except ValueError as e:
                    QMessageBox.warning(self.parent, "Ошибка", str(e))

    def reset_color(self):
        """Сбрасывает выделение и цвет узлов и рёбер."""
        self.canvas.clear_highlighted_paths()
        self.canvas.update()

    def add_graph_from_matrix(self):
        """Создаёт граф из матрицы смежности."""
        try:
            node_count, ok = QInputDialog.getInt(self.parent, "Количество узлов", "Введите количество узлов:")
            if not ok or node_count <= 0:
                return

            dialog = MatrixDialog(node_count, self.parent)
            if dialog.exec() == QDialog.Accepted:
                matrix = dialog.matrix

                self.canvas.clear_graph()
                for i in range(node_count):
                    self.canvas.create_node(str(i + 1), f"{i + 1}", "#ADD8E6")

                for i in range(node_count):
                    for j in range(i + 1, node_count):
                        if matrix[i][j] != 0:
                            if self.canvas.graph.has_edge(str(i + 1), str(j + 1)):
                                QMessageBox.warning(self.parent, "Ошибка", f"Ребро между {i + 1} и {j + 1} уже существует.")
                            else:
                                try:
                                    weight = int(matrix[i][j])
                                    self.canvas.create_edge(str(i + 1), str(j + 1), weight)
                                except ValueError as e:
                                    QMessageBox.warning(self.parent, "Ошибка", f"Некорректное значение ребра ({i + 1}, {j + 1}): {e}")

                QMessageBox.information(self.parent, "Матрица весов", "Граф успешно создан.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка создания графа: {e}")

    def sync_all_node_positions(self):
        """Синхронизирует позиции всех узлов в графе."""
        for node_id, (node_item, _) in self.canvas.nodes.items():
            self.canvas.update_node_position(node_id)

    def save_graph(self):
        """Сохраняет граф в файл."""
        self.sync_all_node_positions()
        graph_data = serialize_graph(self.canvas)
        save_to_file(self.parent, graph_data)

    def load_graph(self):
        """Загружает граф из файла."""
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
        """Очищает граф на холсте."""
        self.canvas.clear_graph()
        self.canvas.update()

    def run_dijkstra(self):
        """Запускает алгоритм Дейкстры."""
        start_node, ok = QInputDialog.getText(self.parent, "Алгоритм Дейкстры", "Введите начальный узел:")
        if ok and start_node in self.canvas.nodes:
            end_node, ok = QInputDialog.getText(self.parent, "Алгоритм Дейкстры", "Введите конечный узел:")

            if ok and end_node in self.canvas.nodes:
                distance, path = dijkstra(self.canvas, start_node, end_node)
                print(f"Distance: {distance}")
                print(f"Path: {path}")
                self.canvas.highlight_shortest_paths(distance, path)
            else:
                QMessageBox.warning(self.parent, "Ошибка", "Конечный узел не существует или не был введён.")

    def run_prim(self):
        """Запускает алгоритм Прима для нахождения минимального остовного дерева."""
        mst_edges = prim_mst(self.canvas)
        self.canvas.highlight_mst(mst_edges)

    def run_kamada_kawai(self):
        """Запускает алгоритм Камада-Кавай для расположения узлов."""
        try:
            if not self.canvas.graph or not nx.is_connected(self.canvas.graph):
                QMessageBox.warning(self.parent, "Ошибка", "Граф должен быть связным для выполнения алгоритма Камада-Кавай.")
                return

            self.canvas.graph.clear()
            for node_id in self.canvas.nodes:
                self.canvas.graph.add_node(node_id)
            for (start, end), edge in self.canvas.edges.items():
                self.canvas.graph.add_edge(start, end)

            start_time = time.time()
            layout = kamada_kawai_layout(self.canvas.graph)
            if not layout:
                QMessageBox.warning(self.parent, "Ошибка", "Алгоритм Камада-Кавай не вернул расположение для узлов.")
                return

            end_time = time.time()
            elapsed_time = end_time - start_time
            max_x = max(x for x, _ in layout.values())
            max_y = max(y for _, y in layout.values())

            for node_id, (x, y) in layout.items():
                scaled_x = (x / max_x) * 100
                scaled_y = (y / max_y) * 100
                self.canvas.update_node_position(node_id)

                node_item = self.canvas.nodes[node_id][0]
                node_item.setPos(scaled_x, scaled_y)

            self.canvas.scene.update()
            QMessageBox.information(self.parent, "Камада-Кавай", f"Расположение узлов выполнено за {elapsed_time:.4f} секунд.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка алгоритма Камада-Кавай: {e}")

    def run_force_directed(self):
        """Запускает силовой метод для расположения узлов."""
        try:
            if not self.canvas.graph or not nx.is_connected(self.canvas.graph):
                QMessageBox.warning(self.parent, "Ошибка", "Граф должен быть связным для выполнения силового метода.")
                return

            self.canvas.graph.clear()
            for node_id in self.canvas.nodes:
                self.canvas.graph.add_node(node_id)
            for (start, end), edge in self.canvas.edges.items():
                self.canvas.graph.add_edge(start, end)

            start_time = time.time()
            layout = force_directed_layout(self.canvas.graph)
            if not layout:
                QMessageBox.warning(self.parent, "Ошибка", "Силовой метод не вернул расположение для узлов.")
                return

            end_time = time.time()
            elapsed_time = end_time - start_time
            max_x = max(x for x, _ in layout.values())
            max_y = max(y for _, y in layout.values())

            for node_id, (x, y) in layout.items():
                scaled_x = (x / max_x) * 100
                scaled_y = (y / max_y) * 100
                self.canvas.update_node_position(node_id)

                node_item = self.canvas.nodes[node_id][0]
                node_item.setPos(scaled_x, scaled_y)

            self.canvas.scene.update()
            QMessageBox.information(self.parent, "Силовой метод", f"Расположение узлов выполнено за {elapsed_time:.4f} секунд.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка силового метода: {e}")

    def run_spring_layout(self):
        """Запускает пружинный алгоритм для расположения узлов."""
        try:
            if not self.canvas.graph or not nx.is_connected(self.canvas.graph):
                QMessageBox.warning(self.parent, "Ошибка", "Граф должен быть связным для выполнения пружинного алгоритма.")
                return

            self.canvas.graph.clear()
            for node_id in self.canvas.nodes:
                self.canvas.graph.add_node(node_id)
            for (start, end), edge in self.canvas.edges.items():
                self.canvas.graph.add_edge(start, end)

            start_time = time.time()
            spring_layout(self.canvas.graph, self.canvas)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.canvas.scene.update()
            QMessageBox.information(self.parent, "Пружинный алгоритм", f"Расположение узлов выполнено за {elapsed_time:.4f} секунд.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Ошибка", f"Ошибка пружинного алгоритма: {e}")
