# core/layout.py
import networkx as nx
import numpy as np


def kamada_kawai_layout(graph: nx.Graph) -> dict:
    """
    Рассчитывает расположение узлов по методу Камада-Кавай.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")

    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")

    if not graph.edges:
        raise ValueError("Граф не содержит рёбер.")

    layout = nx.kamada_kawai_layout(graph)

    if not layout:
        raise ValueError("Алгоритм Камада-Кавай не вернул расположение для узлов.")

    return layout


def force_directed_layout(graph: nx.Graph, iterations: int = 50, k: float = 1.0, gravity: float = 0.1) -> dict:
    """
    Рассчитывает расположение узлов по силовому методу.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")
    if not graph.edges:
        raise ValueError("Граф не содержит рёбер.")

    pos = {node: np.random.rand(2) for node in graph.nodes}

    for _ in range(iterations):
        new_pos = {node: pos[node].copy() for node in graph.nodes}

        for node in graph.nodes:
            force = np.zeros(2)

            for neighbor in graph.neighbors(node):
                diff = pos[neighbor] - pos[node]
                distance = max(np.linalg.norm(diff), 1e-9)
                force += diff / distance

            for other_node in graph.nodes:
                if other_node == node:
                    continue
                diff = pos[node] - pos[other_node]
                distance = max(np.linalg.norm(diff), 1e-9)
                force += diff / (distance ** 2)

            force -= pos[node] * gravity

            max_force = 10.0
            if np.linalg.norm(force) > max_force:
                force = force / np.linalg.norm(force) * max_force

            new_pos[node] += force * k

        center = np.mean(list(new_pos.values()), axis=0)
        for node in new_pos:
            new_pos[node] -= center

        pos = new_pos

    return pos


def random_layout(graph: nx.Graph) -> dict:
    """
    Случайное расположение узлов графа.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")

    return nx.random_layout(graph)


def spring_layout(graph: nx.Graph, canvas) -> None:
    """
    Реализует пружинный алгоритм для расположения узлов графа.
    """
    screen_size = canvas.scene.width(), canvas.scene.height()
    screen_w, screen_h = screen_size
    const_charge = 100000
    const_spring = 0.001
    spring_equ_len = 10
    max_iterations = 200
    dt = 0.1
    bodies = []

    for node_id in graph.nodes():
        pos = np.random.random(2) * 0.8 * np.array([screen_w, screen_h]) + 0.1 * np.array([screen_w, screen_h])
        bodies.append({'id': node_id, 'pos': pos, 'vel': np.zeros(2)})

    def edge_exists(body_a, body_b) -> bool:
        return graph.has_edge(body_a['id'], body_b['id'])

    def unit(v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        return v / norm if norm > 1e-9 else np.zeros_like(v)

    def update_body_physics(bods, dt: float) -> None:
        for body_a in bods:
            f_net = np.zeros(2)
            for body_b in bods:
                if body_a['id'] == body_b['id']:
                    continue
                ab = body_b['pos'] - body_a['pos']
                _ab = max(np.linalg.norm(ab), 1e-9)
                f_s = const_spring * unit(ab) * (_ab - spring_equ_len) if edge_exists(body_a, body_b) else 0
                f_c = const_charge * unit(ab) / _ab**2
                f_net += f_s - f_c
            body_a['vel'] += f_net * dt
            body_a['vel'] *= 0.99
            body_a['pos'] += body_a['vel'] * dt
            body_a['pos'] = np.clip(body_a['pos'], 0, [screen_w, screen_h])

    for _ in range(max_iterations):
        update_body_physics(bodies, dt)

    p_avg = np.mean([body['pos'] for body in bodies], axis=0)
    max_pos = np.max([body['pos'] for body in bodies], axis=0)
    min_pos = np.min([body['pos'] for body in bodies], axis=0)
    scale = min(screen_w / (max_pos[0] - min_pos[0] + 1e-9), screen_h / (max_pos[1] - min_pos[1] + 1e-9))
    for body in bodies:
        node_item = canvas.nodes[body['id']][0]
        pos = (body['pos'] - p_avg) * scale + np.array(screen_size) / 2
        pos[1] = screen_h - pos[1]
        node_item.setPos(pos[0], pos[1])
