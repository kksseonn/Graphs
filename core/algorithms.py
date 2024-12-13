# core/algorithms.py

import heapq
import numpy as np
import networkx as nx

def dijkstra(graph, start):
    """Поиск кратчайшего пути от узла start до всех остальных узлов графа."""
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    priority_queue = [(0, start)]  # (расстояние, узел)
    previous_nodes = {node: None for node in graph.nodes}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes  # Возвращаем дистанции и пути

def prim_mst(graph):
    """Поиск минимального остовного дерева графа с использованием алгоритма Прима."""
    start_node = next(iter(graph.nodes))  # Начинаем с любого узла
    visited = set([start_node])
    edges = [
        (weight, start_node, neighbor)
        for neighbor, weight in graph.get_neighbors(start_node)
    ]
    heapq.heapify(edges)

    mst = []
    while edges:
        weight, start, end = heapq.heappop(edges)
        if end not in visited:
            visited.add(end)
            mst.append((start, end, weight))

            for to_neighbor, to_weight in graph.get_neighbors(end):
                if to_neighbor not in visited:
                    heapq.heappush(edges, (to_weight, end, to_neighbor))

    return mst  # Возвращаем рёбра МОДа


def kamada_kawai_layout(graph):
    """
    Реализация алгоритма Камада-Кавай для расположения узлов графа.

    :param graph: Экземпляр графа, содержащий узлы и рёбра.
    :return: Словарь с координатами узлов.
    """
    # Создание NetworkX графа из текущего графа
    nx_graph = nx.Graph()
    for node_id, node_data in graph.nodes.items():
        nx_graph.add_node(node_id)
    for edge in graph.edges.values():
        nx_graph.add_edge(edge.start, edge.end, weight=edge.weight)

    # Вычисление позиций узлов с помощью алгоритма Камада-Кавай
    positions = nx.kamada_kawai_layout(nx_graph)

    # Установка новых позиций для узлов
    for node_id, pos in positions.items():
        graphic_node = graph.nodes[node_id]  # Получение графического объекта узла
        if hasattr(graphic_node, "setPos"):
            graphic_node.setPos(pos[0] * 100, pos[1] * 100)  # Масштабирование для удобства
        else:
            raise ValueError(f"Узел {node_id} не поддерживает метод setPos")

    return positions