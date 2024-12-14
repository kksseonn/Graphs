# core/data_storage.py

import json
import networkx as nx

def serialize_graph(graph):
    """Сериализует граф в JSON-формат."""
    data = nx.node_link_data(graph.graph)
    return json.dumps(data, indent=4)

def deserialize_graph(graph, json_data):
    """Восстанавливает граф из JSON-данных."""
    data = json.loads(json_data)
    graph.graph = nx.node_link_graph(data)
