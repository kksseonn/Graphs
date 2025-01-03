# core/algorithms.py
import networkx as nx


def dijkstra(graph: nx.Graph, start: str, end: str = None) -> tuple:
    """
    Реализует алгоритм Дейкстры для нахождения кратчайших путей.
    """
    try:
        lengths, paths = nx.single_source_dijkstra(graph.graph, source=start)
        if end is not None:
            if end in paths:
                path = paths[end]
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                return lengths[end], edges
            else:
                raise ValueError(f"Нет пути до узла {end}.")
        else:
            edges_dict = {}
            for target, path in paths.items():
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                edges_dict[target] = edges
            return lengths, edges_dict
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Дейкстры: {e}")


def prim_mst(graph: nx.Graph) -> list:
    """
    Реализует алгоритм Прима для нахождения минимального остовного дерева.
    """
    try:
        mst = nx.minimum_spanning_tree(graph.graph)
        return list(mst.edges(data=True))
    except nx.NetworkXError as e:
        raise ValueError(f"Ошибка алгоритма Прима: {e}")
