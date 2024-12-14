# core/data_storage.py

import json
import networkx as nx
from typing import Any

def serialize_graph(graph):
    """Сериализует граф в JSON-формат."""
    nodes = [
        {
            "id": node_id,
            "label": text.toPlainText(),
            "color": ellipse.brush().color().name(),
            "position": (ellipse.scenePos().x(), ellipse.scenePos().y())
        }
        for node_id, (ellipse, text) in graph.nodes.items()
    ]
    edges = [
        {
            "start": edge.data(0),
            "end": edge.data(1),
            "weight": edge.pen().width()
        }
        for edge in graph.edges
    ]
    return json.dumps({"nodes": nodes, "edges": edges}, indent=4)
def deserialize_graph(graph, json_data):
    """Восстанавливает граф из JSON-данных."""
    data = json.loads(json_data)
    graph.clear_graph()  # Очищаем текущий граф перед загрузкой
    for node in data["nodes"]:
        graph.create_node(
            node_id=node["id"],
            label=node["label"],
            color=node["color"]
        )
        graph.nodes[node["id"]][0].setPos(node["position"][0], node["position"][1])
    for edge in data["edges"]:
        graph.create_edge(
            start=edge["start"],
            end=edge["end"],
            weight=edge["weight"]
        )