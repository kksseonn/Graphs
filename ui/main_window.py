# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow
from ui.menu_bar import MenuBarCreator
from ui.tool_bar import ToolBarCreator
from ui.dialog_handler import DialogHandler
from ui.canvas import Canvas

class MainWindow(QMainWindow):
    """
    Главное окно приложения для работы с графами.
    """

    def __init__(self):
        super().__init__()

        # Установка заголовка и размеров окна
        self.setWindowTitle("Редактор графов")
        self.setGeometry(100, 100, 900, 700)

        # Инициализация холста для графа
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        # Создание вспомогательных компонентов
        self.dialog_handler = DialogHandler(self.canvas, self)

        # Создание меню и панели инструментов
        self.menu_bar = MenuBarCreator(self, self.dialog_handler)
        self.setMenuBar(self.menu_bar.create_menu_bar())

        self.tool_bar = ToolBarCreator(self, self.dialog_handler)
        self.addToolBar(self.tool_bar.create_tool_bar())
