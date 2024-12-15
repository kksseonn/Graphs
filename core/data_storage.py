# core/data_storage.py

import json
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QPointF

def serialize_graph(graph):
    """Сериализует граф в JSON-формат."""
    nodes = []
    for node_id, data in graph.graph.nodes(data=True):
        position = data.get('position', (0, 0))  # Получаем позицию узла из атрибутов
        nodes.append({
            "id": node_id,
            "label": data['label'],
            "color": data['color'],
            "position": position  # Сохраняем позицию узла
        })
    
    edges = []
    for start, end, data in graph.graph.edges(data=True):
        edges.append({
            "start": start,
            "end": end,
            "weight": data['weight']
        })
    
    return json.dumps({"nodes": nodes, "edges": edges}, indent=4)

def deserialize_graph(graph, json_data):
    """Восстанавливает граф из JSON-данных."""
    data = json.loads(json_data)
    graph.clear_graph()  # Очищаем текущий граф перед загрузкой
    
    # Восстановление узлов
    for node in data["nodes"]:
        graph.create_node(
            node_id=node["id"],
            label=node["label"],
            color=node["color"],
            position=tuple(node["position"])  # Передаем позицию узла как кортеж
        )
    
    # Восстановление рёбер
    for edge in data["edges"]:
        graph.create_edge(
            start=edge["start"],
            end=edge["end"],
            weight=edge["weight"]
        )