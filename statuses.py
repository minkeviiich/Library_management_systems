from enum import Enum


class Status(Enum):
    """
    Перечисление для статусов книг.
    """

    AVAILABLE = "в наличии"
    BORROWED = "выдана"
