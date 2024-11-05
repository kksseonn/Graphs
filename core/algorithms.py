# core/algorithms.py

import heapq

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
