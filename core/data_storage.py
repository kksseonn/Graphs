# core/data_storage.py

import json
from PyQt5.QtGui import QPen

def serialize_graph(graph):
    """Сериализует граф в JSON-формат."""
    # Сериализация узлов
    nodes = [
        {
            "id": node_id,
            "label": data['label'],  # Прямо берем из атрибутов узла
            "color": data['color'],
            "position": (data.get('position', (0, 0)))  # Получаем позицию, если она есть
        }
        for node_id, data in graph.graph.nodes(data=True)
    ]
    
    # Сериализация рёбер
    edges = [
        {
            "start": start,
            "end": end,
            "weight": data['weight']  # Берем вес из атрибутов ребра
        }
        for start, end, data in graph.graph.edges(data=True)
    ]
    
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
            color=node["color"]
        )
        # Устанавливаем позицию узла
        graph.nodes[node["id"]][0].setPos(node["position"][0], node["position"][1])
    
    # Восстановление рёбер
    for edge in data["edges"]:
        graph.create_edge(
            start=edge["start"],
            end=edge["end"],
            weight=edge["weight"]
        )