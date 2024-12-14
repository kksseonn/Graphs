# ui/dialogs/edge_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QColorDialog, QSpinBox, QComboBox
)
from PyQt5.QtCore import Qt


class EdgeDialog(QDialog):
    def __init__(self, nodes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать ребро")
        self.setFixedSize(300, 200)

        # Инициализация виджетов
        layout = QVBoxLayout()

        # Поля для начального и конечного узлов, а также веса
        layout.addWidget(QLabel("Начальный узел"))
        self.start_node = QComboBox()
        self.start_node.addItems(nodes)
        layout.addWidget(self.start_node)

        layout.addWidget(QLabel("Конечный узел"))
        self.end_node = QComboBox()
        self.end_node.addItems(nodes)
        layout.addWidget(self.end_node)

        self.weight_input = QSpinBox()
        self.weight_input.setRange(1, 100)
        layout.addWidget(QLabel("Вес ребра"))
        layout.addWidget(self.weight_input)

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

    def get_data(self):
        """Возвращает данные из полей формы."""
        return {
            "start": self.start_node.currentText().strip(),
            "end": self.end_node.currentText().strip(),
            "weight": self.weight_input.value(),
        }
