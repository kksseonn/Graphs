#ui/tool_bar.py
from PyQt5.QtWidgets import QToolBar, QToolButton
from PyQt5.QtCore import QSize  # Импортируем QSize
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

        # Создание действий
        add_node_action = self.dialog_handler.create_action("Добавить узел", self.dialog_handler.add_node)
        remove_node_action = self.dialog_handler.create_action("Удалить узел", self.dialog_handler.remove_node)
        add_edge_action = self.dialog_handler.create_action("Добавить ребро", self.dialog_handler.add_edge)
        remove_edge_action = self.dialog_handler.create_action("Удалить ребро", self.dialog_handler.remove_edge)
        reset_color_action = self.dialog_handler.create_action("Сбросить Цвета", self.dialog_handler.reset_color)

        # Используем QToolButton для управления размером иконки
        add_node_button = QToolButton()
        add_node_button.setDefaultAction(add_node_action)
        add_node_button.setIconSize(QSize(32, 32))  # Установка размера иконки
        add_node_button.setText("Добавить узел")

        remove_node_button = QToolButton()
        remove_node_button.setDefaultAction(remove_node_action)
        remove_node_button.setIconSize(QSize(32, 32))  # Установка размера иконки
        remove_node_button.setText("Удалить узел")

        add_edge_button = QToolButton()
        add_edge_button.setDefaultAction(add_edge_action)
        add_edge_button.setIconSize(QSize(32, 32))  # Установка размера иконки
        add_edge_button.setText("Добавить ребро")

        remove_edge_button = QToolButton()
        remove_edge_button.setDefaultAction(remove_edge_action)
        remove_edge_button.setIconSize(QSize(32, 32))  # Установка размера иконки
        remove_edge_button.setText("Удалить ребро")
        
        reset_color_button = QToolButton()
        reset_color_button.setDefaultAction(reset_color_action)
        reset_color_button.setIconSize(QSize(32, 32))  # Установка размера иконки
        reset_color_button.setText("Сбросить Цвета")

        # Добавление кнопок на панель инструментов
        tool_bar.addWidget(add_node_button)
        tool_bar.addWidget(remove_node_button)
        tool_bar.addWidget(add_edge_button)
        tool_bar.addWidget(remove_edge_button)
        tool_bar.addWidget(reset_color_button)

        # Настройка стиля кнопок для улучшения внешнего вида
        tool_bar.setStyleSheet("""
            QToolButton {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
                min-width: 100px;
            }
            QToolButton:hover {
                background-color: #d0d0d0;
            }
            QToolBar {
                background-color: #e0e0e0;
                padding: 5px;
            }
        """)

        return tool_bar

