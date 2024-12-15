# ui/dialogs/node_dialog.py
import random
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QColorDialog
)
from PyQt5.QtGui import QColor


class NodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать узел")
        self.setFixedSize(300, 200)

        # Инициализация виджетов
        layout = QVBoxLayout()

        # Поле для метки и выбора цвета узла
        self.label_input = QLineEdit()
        layout.addWidget(QLabel("Метка узла"))
        layout.addWidget(self.label_input)

        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.clicked.connect(self.select_color)
        self.color = "blue"  # Цвет по умолчанию
        layout.addWidget(QLabel("Цвет узла"))
        layout.addWidget(self.color_button)

        # Кнопка для случайного цвета
        self.random_color_button = QPushButton("Случайный цвет")
        self.random_color_button.clicked.connect(self.set_random_color)
        layout.addWidget(self.random_color_button)

        # Кнопки OK и Отмена
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def select_color(self):
        """Открывает диалог выбора цвета и обновляет стиль кнопки цвета."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.color_button.setStyleSheet(f"background-color: {self.color}")

    def set_random_color(self):
        """Генерирует случайный цвет и обновляет стиль кнопки."""
        random_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = random_color.name()
        self.color_button.setStyleSheet(f"background-color: {self.color}")

    def get_data(self):
        """Возвращает данные из полей формы, устанавливая ID равным метке."""
        label = self.label_input.text().strip()
        return {
            "id": label,  # Устанавливаем ID равным метке
            "label": label,
            "color": self.color,
        }