
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QPushButton, 
    QMessageBox
)


class MatrixDialog(QDialog):
    def __init__(self, node_count, parent=None):
        super().__init__(parent)
        self.node_count = node_count
        self.matrix = [[0] * node_count for _ in range(node_count)]
        self.setWindowTitle("Ввод матрицы весов")
        layout = QVBoxLayout(self)

        # Создание таблицы для ввода
        self.table = QTableWidget(node_count, node_count, self)
        self.table.setHorizontalHeaderLabels([f"Узел {i}" for i in range(node_count)])
        self.table.setVerticalHeaderLabels([f"Узел {i}" for i in range(node_count)])
        layout.addWidget(self.table)

        # Кнопка OK
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.process_input)
        layout.addWidget(self.ok_button)

    def process_input(self):
        try:
            for i in range(self.node_count):
                for j in range(self.node_count):
                    item = self.table.item(i, j)
                    if item is None or item.text().strip() in ["", "-"]:
                        self.matrix[i][j] = 0  # Пропуск ребра
                    else:
                        self.matrix[i][j] = int(item.text().strip())
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка ввода данных: {e}")