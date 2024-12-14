#ui/tool_bar.py

from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt

class ToolBarCreator:
    """
    Класс для создания панели инструментов.
    """

    def __init__(self, main_window, dialog_handler):
        self.main_window = main_window
        self.dialog_handler = dialog_handler

    def create_tool_bar(self):
        """
        Создаёт панель инструментов для быстрого доступа к функциям.
        """
        tool_bar = QToolBar("Инструменты", self.main_window)
        self.main_window.addToolBar(Qt.TopToolBarArea, tool_bar)

        tool_bar.addAction(self.dialog_handler.create_action("Добавить узел", self.dialog_handler.add_node))
        tool_bar.addAction(self.dialog_handler.create_action("Удалить узел", self.dialog_handler.remove_node))
        tool_bar.addAction(self.dialog_handler.create_action("Добавить ребро", self.dialog_handler.add_edge))
        tool_bar.addAction(self.dialog_handler.create_action("Удалить ребро", self.dialog_handler.remove_edge))

        return tool_bar
