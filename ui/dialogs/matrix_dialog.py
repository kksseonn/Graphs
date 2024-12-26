from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QPushButton,
    QMessageBox
)


class MatrixDialog(QDialog):
    """
    Диалоговое окно для ввода матрицы весов графа.
    """

    def __init__(self, node_count: int, parent=None):
        """
        Инициализация окна для ввода матрицы весов.
        """
        super().__init__(parent)
        self.node_count = node_count
        self.matrix = [[0] * node_count for _ in range(node_count)]
        self.setWindowTitle("Ввод матрицы весов")

        layout = QVBoxLayout(self)

        self.table = QTableWidget(node_count, node_count, self)
        self.table.setHorizontalHeaderLabels([f"Узел {i}" for i in range(node_count)])
        self.table.setVerticalHeaderLabels([f"Узел {i}" for i in range(node_count)])
        layout.addWidget(self.table)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.process_input)
        layout.addWidget(self.ok_button)

    def process_input(self):
        """
        Обрабатывает ввод данных из таблицы и сохраняет в матрице.
        """
        try:
            for i in range(self.node_count):
                for j in range(self.node_count):
                    item = self.table.item(i, j)
                    if item is None or item.text().strip() in ["", "-"]:
                        self.matrix[i][j] = 0
                    else:
                        self.matrix[i][j] = int(item.text().strip())
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка ввода данных: {e}")

    def get_matrix(self) -> list:
        """
        Возвращает матрицу весов после подтверждения.
        """
        return self.matrix
