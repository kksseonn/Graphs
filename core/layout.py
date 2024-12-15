# core/layout.py
import networkx as nx
import numpy as np

def kamada_kawai_layout(graph):
    """
    Рассчитывает расположение узлов по методу Камада-Кавай.

    :param graph: NetworkX-граф.
    :return: Словарь с координатами узлов.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")
    
    if not graph.edges:
        raise ValueError("Граф не содержит рёбер.")

    # Получаем расположение узлов
    layout = nx.kamada_kawai_layout(graph)
    
    if not layout:
        raise ValueError("Алгоритм Камада-Кавай не вернул расположение для узлов.")
    
    return layout

def force_directed_layout(graph, iterations=50, k=1.0, gravity=0.1):
    """
    Рассчитывает расположение узлов по силовому методу.

    :param graph: NetworkX-граф.
    :param iterations: Количество итераций для расчёта.
    :param k: Константа силы от соседей.
    :param gravity: Сила притяжения к центру.
    :return: Словарь с координатами узлов.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")
    
    if not graph.edges:
        raise ValueError("Граф не содержит рёбер.")

    # Начальная инициализация координат
    pos = {node: np.random.rand(2) for node in graph.nodes}
    
    for _ in range(iterations):
        # Сила притяжения
        for node in graph.nodes:
            force = np.zeros(2)
            for neighbor in graph.neighbors(node):
                diff = pos[neighbor] - pos[node]
                distance = np.linalg.norm(diff)
                force += diff / (distance ** 2 + 1e-4)  # Добавляем стабилизирующий коэффициент

            # Гравитация
            force -= pos[node] * gravity

            # Применение силы
            pos[node] += force * k

    return pos


def random_layout(graph):
    """
    Случайное расположение узлов графа.

    :param graph: NetworkX-граф.
    :return: Словарь с координатами узлов.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")

    return nx.random_layout(graph)

