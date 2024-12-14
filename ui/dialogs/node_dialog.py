# ui/dialogs/node_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QColorDialog
)


class NodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать узел")
        self.setFixedSize(300, 200)

        # Инициализация виджетов
        layout = QVBoxLayout()

        # Поля для ID, метки и выбора цвета узла
        self.id_input = QLineEdit()
        layout.addWidget(QLabel("ID узла"))
        layout.addWidget(self.id_input)

        self.label_input = QLineEdit()
        layout.addWidget(QLabel("Метка узла"))
        layout.addWidget(self.label_input)

        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.clicked.connect(self.select_color)
        self.color = "blue"  # Цвет по умолчанию
        layout.addWidget(QLabel("Цвет узла"))
        layout.addWidget(self.color_button)

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

    def get_data(self):
        """Возвращает данные из полей формы."""
        return {
            "id": self.id_input.text().strip(),
            "label": self.label_input.text().strip(),
            "color": self.color,
        }