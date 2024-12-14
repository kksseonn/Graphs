# utils/file_operations.py

from PyQt5.QtWidgets import QFileDialog, QMessageBox
import json
from typing import Optional, Any

# def save_to_file(parent, graph_data: str) -> None:
#     """Сохраняет данные графа в файл."""
#     file_path, _ = QFileDialog.getSaveFileName(parent, "Сохранить граф", "", "JSON Files (*.json)")
#     if not file_path:
#         return

#     try:
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(graph_data)
#         QMessageBox.information(parent, "Сохранение", "Граф успешно сохранён.")
#     except (IOError, OSError) as e:
#         QMessageBox.critical(parent, "Ошибка", f"Не удалось сохранить файл: {e}")

# def load_from_file(parent) -> Optional[Any]:
#     """Загружает данные графа из файла."""
#     file_path, _ = QFileDialog.getOpenFileName(parent, "Загрузить граф", "", "JSON Files (*.json)")
#     if not file_path:
#         return None

#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             return json.load(file)  # Сразу парсим JSON
#     except (IOError, OSError, json.JSONDecodeError) as e:
#         QMessageBox.critical(parent, "Ошибка", f"Не удалось загрузить файл: {e}")
#         return None
from PyQt5.QtWidgets import QFileDialog, QMessageBox
def save_to_file(parent, graph_data):
    """Сохраняет данные графа в файл."""
    file_path, _ = QFileDialog.getSaveFileName(parent, "Сохранить граф", "", "JSON Files (*.json)")
    if not file_path:
        return
    try:
        with open(file_path, "w") as file:
            file.write(graph_data)
        QMessageBox.information(parent, "Сохранение", "Граф успешно сохранён.")
    except Exception as e:
        QMessageBox.critical(parent, "Ошибка", f"Не удалось сохранить файл: {e}")
def load_from_file(parent):
    """Загружает данные графа из файла."""
    file_path, _ = QFileDialog.getOpenFileName(parent, "Загрузить граф", "", "JSON Files (*.json)")
    if not file_path:
        return None
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        QMessageBox.critical(parent, "Ошибка", f"Не удалось загрузить файл: {e}")
        return None
