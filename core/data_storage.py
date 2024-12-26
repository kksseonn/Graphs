# core/data_storage.py
import json


def serialize_graph(graph):
    """
    Сериализует граф в JSON-формат.

    :param graph: Граф, который необходимо сериализовать.
    :return: Строка в формате JSON, представляющая сериализованный граф.
    """
    nodes = []
    for node_id, data in graph.graph.nodes(data=True):
        position = data.get('position', (0, 0))
        nodes.append({
            "id": node_id,
            "label": data['label'],
            "color": data['color'],
            "position": position
        })

    edges = []
    for start, end, data in graph.graph.edges(data=True):
        edges.append({
            "start": start,
            "end": end,
            "weight": data['weight']
        })
    return json.dumps({"nodes": nodes, "edges": edges}, indent=4)


def deserialize_graph(graph, json_data: str) -> None:
    """
    Восстанавливает граф из JSON-данных.

    :param graph: Граф, который необходимо восстановить.
    :param json_data: Строка в формате JSON, содержащая данные графа.
    :return: None
    """
    data = json.loads(json_data)
    graph.clear_graph()

    for node in data["nodes"]:
        graph.create_node(
            node_id=node["id"],
            label=node["label"],
            color=node["color"],
            position=tuple(node["position"])
        )

    for edge in data["edges"]:
        graph.create_edge(
            start=edge["start"],
            end=edge["end"],
            weight=edge["weight"]
        )
