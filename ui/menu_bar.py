# ui/menu_bar.py
from PyQt5.QtWidgets import QMenuBar


class MenuBarCreator:
    """Класс для создания строки меню приложения."""

    def __init__(self, main_window, dialog_handler):
        self.main_window = main_window
        self.dialog_handler = dialog_handler

    def create_menu_bar(self):
        """Создаёт строку меню с основными функциями."""
        menu_bar = QMenuBar(self.main_window)

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.dialog_handler.create_action("Сохранить", self.dialog_handler.save_graph))
        file_menu.addAction(self.dialog_handler.create_action("Загрузить", self.dialog_handler.load_graph))
        file_menu.addAction(self.dialog_handler.create_action("Очистить", self.dialog_handler.delete_graph))
        file_menu.addAction(self.dialog_handler.create_action("Выход", self.main_window.close))

        algorithms_menu = menu_bar.addMenu("Алгоритмы")
        algorithms_menu.addAction(self.dialog_handler.create_action("Поиск кратчайшего пути", self.dialog_handler.run_dijkstra))
        algorithms_menu.addAction(self.dialog_handler.create_action("Минимальное остовное дерево", self.dialog_handler.run_prim))
        algorithms_menu.addAction(self.dialog_handler.create_action("Расположение Камада-Кавай", self.dialog_handler.run_kamada_kawai))
        algorithms_menu.addAction(self.dialog_handler.create_action("Силовой метод", self.dialog_handler.run_force_directed))
        algorithms_menu.addAction(self.dialog_handler.create_action("Пружинный алгоритм", self.dialog_handler.run_spring_layout))

        edit_menu = menu_bar.addMenu("Правка")
        edit_menu.addAction(self.dialog_handler.create_action("Добавить узел", self.dialog_handler.add_node))
        edit_menu.addAction(self.dialog_handler.create_action("Удалить узел", self.dialog_handler.remove_node))
        edit_menu.addAction(self.dialog_handler.create_action("Добавить ребро", self.dialog_handler.add_edge))
        edit_menu.addAction(self.dialog_handler.create_action("Удалить ребро", self.dialog_handler.remove_edge))
        edit_menu.addAction(self.dialog_handler.create_action("Добавить граф по матрице весов", self.dialog_handler.add_graph_from_matrix))

        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0;
                font-size: 16px;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 10px;
            }
            QMenuBar::item:selected {
                background-color: #d0d0d0;
            }
            QMenu {
                background-color: #ffffff;
                font-size: 14px;
                border: 1px solid #cccccc;
            }
            QMenu::item:selected {
                background-color: #b0b0b0;
            }
        """)

        return menu_bar
