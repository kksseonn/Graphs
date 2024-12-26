# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


if __name__ == "__main__":
    """Запускает приложение и отображает главное окно."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
