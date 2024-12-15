# core/layout.py
import networkx as nx
import numpy as np
import pygame

def kamada_kawai_layout(graph):
    """
    Рассчитывает расположение узлов по методу Камада-Кавай.

    :param graph: NetworkX-граф.
    :return: Словарь с координатами узлов.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")
    
    if not graph.edges:
        raise ValueError("Граф не содержит рёбер.")

    # Получаем расположение узлов
    layout = nx.kamada_kawai_layout(graph)
    
    if not layout:
        raise ValueError("Алгоритм Камада-Кавай не вернул расположение для узлов.")
    
    return layout

def force_directed_layout(graph, iterations=50, k=1.0, gravity=0.1):
    """
    Рассчитывает расположение узлов по силовому методу.

    :param graph: NetworkX-граф.
    :param iterations: Количество итераций для расчёта.
    :param k: Константа силы от соседей.
    :param gravity: Сила притяжения к центру.
    :return: Словарь с координатами узлов.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")
    
    if not graph.edges:
        raise ValueError("Граф не содержит рёбер.")

    # Начальная инициализация координат
    pos = {node: np.random.rand(2) for node in graph.nodes}
    
    for _ in range(iterations):
        # Сила притяжения
        for node in graph.nodes:
            force = np.zeros(2)
            for neighbor in graph.neighbors(node):
                diff = pos[neighbor] - pos[node]
                distance = np.linalg.norm(diff)
                force += diff / (distance ** 2 + 1e-4)  # Добавляем стабилизирующий коэффициент

            # Гравитация
            force -= pos[node] * gravity

            # Применение силы
            pos[node] += force * k

    return pos


def random_layout(graph):
    """
    Случайное расположение узлов графа.

    :param graph: NetworkX-граф.
    :return: Словарь с координатами узлов.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Ожидался объект NetworkX Graph.")
    
    if not graph.nodes:
        raise ValueError("Граф не содержит узлов.")

    return nx.random_layout(graph)

def spring_layout(graph, canvas):
    """
    Реализует пружинный алгоритм для расположения узлов графа.
    
    :param graph: NetworkX граф.
    :param canvas: Канвас для обновления позиции узлов.
    """
    # Инициализация параметров
    screen_size = canvas.scene.width(), canvas.scene.height()
    screen_w, screen_h = screen_size
    const_charge = 100000
    const_spring = 0.001
    spring_equ_len = 10
    max_iterations = 200
    dt = 0.1  # Шаг времени для обновления
    bodies = []

    # Инициализация объектов
    for node_id in graph.nodes():
        pos = np.random.random(2) * np.array([screen_w, screen_h])
        bodies.append({'id': node_id, 'pos': pos, 'vel': np.zeros(2)})

    def edge_exists(body_a, body_b):
        a = body_a['id']
        b = body_b['id']
        return graph.has_edge(a, b)

    def unit(v):
        return v / np.linalg.norm(v)

    def update_body_physics(bods, dt):
        for body_a in bods:
            f_net = np.zeros(2)
            for body_b in bods:
                if body_a['id'] == body_b['id']:
                    continue
                ab = body_b['pos'] - body_a['pos']
                _ab = np.linalg.norm(ab)
                # Сила пружины
                f_s = np.zeros(2)
                if edge_exists(body_a, body_b):
                    f_s = const_spring * unit(ab) * (_ab - spring_equ_len)
                # Электрическая сила
                f_c = const_charge * unit(ab) / _ab**2
                f_net += f_s - f_c
            body_a['vel'] += (f_net) * dt
            body_a['vel'] *= 0.99  # Снижение скорости
            body_a['pos'] += body_a['vel'] * dt

    # Итерации обновления
    for _ in range(max_iterations):
        update_body_physics(bodies, dt)

    # Обновляем позиции на канвасе
    p_avg = np.mean([body['pos'] for body in bodies], axis=0)
    for body in bodies:
        node_item = canvas.nodes[body['id']][0]  # Получаем QGraphicsEllipseItem
        pos = body['pos'] + np.array(screen_size) / 2 - p_avg
        pos[1] = screen_h - pos[1]  # Переводим координаты на экран
        node_item.setPos(pos[0], pos[1])