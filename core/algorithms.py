# core/algorithms.py
import networkx as nx

def dijkstra(graph, start):
    """Поиск кратчайших путей с помощью NetworkX."""
    try:
        lengths, paths = nx.single_source_dijkstra(graph.graph, source=start)
        return lengths, paths
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Дейкстры: {e}")

def prim_mst(graph):
    """Поиск минимального остовного дерева через NetworkX."""
    try:
        mst = nx.minimum_spanning_tree(graph.graph)
        return list(mst.edges(data=True))  # Возвращаем рёбра и веса
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Прима: {e}")

def kamada_kawai_layout(graph):
    """Расположение узлов графа с использованием алгоритма Камада-Кавай."""
    try:
        positions = nx.kamada_kawai_layout(graph.graph)
        print(f"Рассчитанные позиции: {positions}")  # Отладочный вывод
        return positions
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Камада-Кавай: {e}")