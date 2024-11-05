class Graph:
    def __init__(self):
        """Инициализация пустого графа с узлами и рёбрами."""
        self.nodes = {}  # Словарь для хранения узлов {node_id: {"label": str, "color": str}}
        self.edges = {}  # Словарь для хранения рёбер {(start, end): {"weight": int, "color": str}}

    def add_node(self, node_id, label="", color="blue"):
        """
        Добавляет узел в граф.
        
        :param node_id: Идентификатор узла.
        :param label: Метка узла (по умолчанию пустая).
        :param color: Цвет узла (по умолчанию синий).
        """
        if node_id in self.nodes:
            raise ValueError(f"Узел с идентификатором {node_id} уже существует.")
        
        self.nodes[node_id] = {"label": label, "color": color}
        print(f"Узел {node_id} добавлен: метка={label}, цвет={color}")

    def add_edge(self, start, end, weight=1, color="black"):
        """
        Добавляет ребро между двумя узлами.
        
        :param start: Начальный узел ребра.
        :param end: Конечный узел ребра.
        :param weight: Вес ребра (по умолчанию 1).
        :param color: Цвет ребра (по умолчанию черный).
        """
        if start not in self.nodes or end not in self.nodes:
            raise ValueError("Оба узла должны существовать в графе для добавления ребра.")
        
        if (start, end) in self.edges:
            raise ValueError(f"Ребро между {start} и {end} уже существует.")
        
        self.edges[(start, end)] = {"weight": weight, "color": color}
        print(f"Ребро добавлено: {start} -> {end}, вес={weight}, цвет={color}")

    def remove_node(self, node_id):
        """
        Удаляет узел из графа вместе со всеми его рёбрами.
        
        :param node_id: Идентификатор узла для удаления.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Узел {node_id} не существует.")
        
        # Удаляем узел
        del self.nodes[node_id]
        
        # Удаляем все рёбра, связанные с узлом
        self.edges = {(start, end): edge for (start, end), edge in self.edges.items() if start != node_id and end != node_id}
        
        print(f"Узел {node_id} и все связанные с ним рёбра удалены.")

    def remove_edge(self, start, end):
        """
        Удаляет ребро между двумя узлами.
        
        :param start: Начальный узел ребра.
        :param end: Конечный узел ребра.
        """
        if (start, end) not in self.edges:
            raise ValueError(f"Ребро между {start} и {end} не существует.")
        
        del self.edges[(start, end)]
        print(f"Ребро {start} -> {end} удалено.")

if __name__ == "__main__":
    graph = Graph()
    
    # Тестирование добавления узлов
    graph.add_node(1, label="A", color="red")
    graph.add_node(2, label="B", color="green")
    
    # Тестирование добавления рёбер
    graph.add_edge(1, 2, weight=5, color="blue")
    
    # Тестирование удаления узла
    graph.remove_node(1)
    
    # Повторное добавление узлов и рёбер для тестирования удаления рёбер
    graph.add_node(1, label="A", color="red")
    graph.add_node(3, label="C", color="yellow")
    graph.add_edge(1, 3, weight=3)
    
    # Тестирование удаления рёбер
    graph.remove_edge(1, 3)