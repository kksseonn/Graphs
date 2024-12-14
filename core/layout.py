# core/layout.py
import networkx as nx

def kamada_kawai_layout(graph):
    """Рассчитывает расположение узлов по методу Камада-Кавай."""
    return nx.kamada_kawai_layout(graph.graph)

def random_layout(graph):
    """Случайное расположение узлов графа."""
    return nx.random_layout(graph.graph)
