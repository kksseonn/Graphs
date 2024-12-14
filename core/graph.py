# core/graph.py

import networkx as nx
import numpy as np

class Graph:
    def __init__(self):
        """Инициализация графа на основе NetworkX."""
        self.graph = nx.Graph()  # Основной объект графа NetworkX

    def add_node(self, node_id, label="", color="blue"):
        """Добавление узла с атрибутами."""
        if node_id in self.graph.nodes:
            raise ValueError(f"Узел с идентификатором {node_id} уже существует.")
        self.graph.add_node(node_id, label=label, color=color)
        print(f"Узел {node_id} добавлен: метка={label}, цвет={color}")

    def add_edge(self, start, end, weight=1, color="black"):
        """Добавление ребра между узлами."""
        if start not in self.graph.nodes or end not in self.graph.nodes:
            raise ValueError("Оба узла должны существовать в графе.")
        if self.graph.has_edge(start, end):
            raise ValueError(f"Ребро между {start} и {end} уже существует.")
        self.graph.add_edge(start, end, weight=weight, color=color)
        print(f"Ребро добавлено: {start} -> {end}, вес={weight}, цвет={color}")

    def remove_node(self, node_id):
        """Удаление узла и всех связанных рёбер."""
        if node_id not in self.graph.nodes:
            raise ValueError(f"Узел {node_id} не существует.")
        self.graph.remove_node(node_id)
        print(f"Узел {node_id} и все связанные с ним рёбра удалены.")

    def remove_edge(self, start, end):
        """Удаление ребра между узлами."""
        if not self.graph.has_edge(start, end):
            raise ValueError(f"Ребро между {start} и {end} не существует.")
        self.graph.remove_edge(start, end)
        print(f"Ребро {start} -> {end} удалено.")

    def from_weight_matrix(self, matrix):
        """
        Создание графа из матрицы весов.

        Аргументы:
            matrix (list[list[float]]): Матрица весов. 0 или '-' означают отсутствие ребра.
        """
        if not matrix or not all(len(row) == len(matrix[0]) for row in matrix):
            raise ValueError("Матрица весов должна быть прямоугольной.")
        
        self.graph.clear()  # Очистка графа

        rows, cols = len(matrix), len(matrix[0])

        # Добавление узлов
        for i in range(rows):
            self.graph.add_node(i, label=f"Узел {i}")  # Узлы имеют метки "Узел i"

        # Добавление рёбер
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] not in [0, "-"]:  # Пропуск отсутствующих рёбер
                    try:
                        weight = float(matrix[i][j])
                        self.graph.add_edge(i, j, weight=weight)
                    except ValueError:
                        raise ValueError(f"Некорректное значение матрицы: {matrix[i][j]} в позиции ({i}, {j})")
