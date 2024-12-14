# core/validation.py
def validate_matrix(matrix):
    """Проверяет корректность матрицы."""
    if not all(len(row) == len(matrix) for row in matrix):
        raise ValueError("Матрица должна быть квадратной.")
    for row in matrix:
        for value in row:
            if value not in [0, "-", float("-inf")] and not isinstance(value, (int, float)):
                raise ValueError("Матрица должна содержать только числа, 0 или '-'.")

def validate_node_id(node_id):
    """Проверяет корректность идентификатора узла."""
    if not isinstance(node_id, str) or not node_id.strip():
        raise ValueError("ID узла должен быть непустой строкой.")