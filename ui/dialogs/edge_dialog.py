# ui/dialogs/edge_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox
)


class EdgeDialog(QDialog):
    """
    Диалоговое окно для добавления или редактирования ребра графа.
    """

    def __init__(self, nodes: list, parent=None):
        """
        Инициализация диалогового окна.
        """
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать ребро")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

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

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_data(self) -> dict:
        """
        Возвращает данные, введенные в форму.
        """
        return {
            "start": self.start_node.currentText().strip(),
            "end": self.end_node.currentText().strip(),
            "weight": self.weight_input.value(),
        }
