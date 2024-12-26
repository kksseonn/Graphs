# ui/dialogs/edge_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox
)


class EdgeDialog(QDialog):
    """
    Диалоговое окно для добавления или редактирования ребра графа.

    Атрибуты:
        start_node (QComboBox): Поле выбора начального узла.
        end_node (QComboBox): Поле выбора конечного узла.
        weight_input (QSpinBox): Поле ввода веса ребра.
        ok_button (QPushButton): Кнопка подтверждения.
        cancel_button (QPushButton): Кнопка отмены.
    """

    def __init__(self, nodes: list, parent=None):
        """
        Инициализация диалогового окна.

        :param nodes: Список узлов графа для выбора.
        :param parent: Родительский виджет.
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

        :return: Словарь с данными:
            - start: Начальный узел.
            - end: Конечный узел.
            - weight: Вес ребра.
        """
        return {
            "start": self.start_node.currentText().strip(),
            "end": self.end_node.currentText().strip(),
            "weight": self.weight_input.value(),
        }
