# core/algorithms.py
import networkx as nx

def dijkstra(graph, start):
    """
    Поиск кратчайших путей с помощью NetworkX.
    
    Parameters:
        graph (nx.Graph): Граф в формате NetworkX.
        start (hashable): Начальный узел для алгоритма Дейкстры.
    
    Returns:
        tuple: Длина путей от начального узла и сами пути.
    
    Raises:
        ValueError: Если возникнет ошибка при выполнении алгоритма.
    """
    try:
        # Вызываем метод single_source_dijkstra для получения длин и путей
        lengths, paths = nx.single_source_dijkstra(graph.graph, source=start)
        return lengths, paths
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Дейкстры: {e}")

def prim_mst(graph):
    """
    Поиск минимального остовного дерева через NetworkX.
    
    Parameters:
        graph (nx.Graph): Граф в формате NetworkX.
    
    Returns:
        list: Список рёбер с информацией о весах.
    
    Raises:
        ValueError: Если возникнет ошибка при построении MST.
    """
    try:
        # Строим минимальное остовное дерево
        mst = nx.minimum_spanning_tree(graph.graph)
        return list(mst.edges(data=True))  # Рёбра и их веса
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Прима: {e}")

