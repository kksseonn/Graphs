# core/graph.py
import networkx as nx
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

class Graph:
    def __init__(self):
        """Инициализация графа на основе NetworkX."""
        self.graph = nx.Graph()

    def add_node(self, node_id: str, label: str = "", color: str = "blue"):
        """Добавление узла с атрибутами."""
        if node_id in self.graph.nodes:
            raise ValueError(f"Узел с идентификатором {node_id} уже существует.")
        self.graph.add_node(node_id, label=label, color=color)
        logging.info(f"Узел {node_id} добавлен: метка={label}, цвет={color}")

    def add_edge(self, start: str, end: str, weight: float = 1, color: str = "black"):
        """Добавление ребра между узлами."""
        if start not in self.graph.nodes or end not in self.graph.nodes:
            raise ValueError("Оба узла должны существовать в графе.")
        if self.graph.has_edge(start, end):
            raise ValueError(f"Ребро между {start} и {end} уже существует.")
        self.graph.add_edge(start, end, weight=weight, color=color)
        logging.info(f"Ребро добавлено: {start} -> {end}, вес={weight}, цвет={color}")

    def remove_node(self, node_id: str):
        """Удаление узла и всех связанных рёбер."""
        if node_id not in self.graph.nodes:
            raise ValueError(f"Узел {node_id} не существует.")
        self.graph.remove_node(node_id)
        logging.info(f"Узел {node_id} и все связанные с ним рёбра удалены.")

    def remove_edge(self, start: str, end: str):
        """Удаление ребра между узлами."""
        if not self.graph.has_edge(start, end):
            raise ValueError(f"Ребро между {start} и {end} не существует.")
        self.graph.remove_edge(start, end)
        logging.info(f"Ребро {start} -> {end} удалено.")

    def from_weight_matrix(self, matrix: list[list[float]]):
        """
        Создание графа из матрицы весов.

        Аргументы:
            matrix (list[list[float]]): Матрица весов. 0 или '-' означают отсутствие ребра.
        """
        if not matrix or not all(len(row) == len(matrix) for row in matrix):
            raise ValueError("Матрица должна быть квадратной.")

        self.graph.clear()

        for i in range(len(matrix)):
            self.graph.add_node(i, label=f"Узел {i}")

        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value not in [0, "-"]:
                    try:
                        weight = float(value)
                        self.graph.add_edge(i, j, weight=weight)
                    except ValueError:
                        raise ValueError(f"Некорректное значение матрицы: {value} в позиции ({i}, {j})")
