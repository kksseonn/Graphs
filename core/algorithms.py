# core/algorithms.py
import networkx as nx

def dijkstra(graph, start, end=None):
    """
    Поиск кратчайших путей с помощью NetworkX.
    
    Parameters:
        graph (nx.Graph): Граф в формате NetworkX.
        start (hashable): Начальный узел для алгоритма Дейкстры.
        end (hashable, optional): Конечный узел для поиска пути. Если None, возвращает пути для всех узлов.
    
    Returns:
        tuple: Список рёбер и длина пути.
    
    Raises:
        ValueError: Если возникнет ошибка при выполнении алгоритма.
    """
    try:
        # Вызываем метод single_source_dijkstra для получения длин и путей
        lengths, paths = nx.single_source_dijkstra(graph.graph, source=start)
        
        if end is not None:
            # Если задан конечный узел, возвращаем рёбра пути до него
            if end in paths:
                path = paths[end]
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                return lengths[end], edges
            else:
                raise ValueError(f"Нет пути до узла {end}.")
        else:
            # Если конечный узел не задан, возвращаем рёбра для всех путей
            edges_dict = {}
            for target, path in paths.items():
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                edges_dict[target] = edges
            return lengths, edges_dict
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

