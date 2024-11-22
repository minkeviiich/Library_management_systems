from statuses import Status


class Book:
    """Класс для представления книги в библиотеке."""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        status: str = Status.AVAILABLE.value,
    ):
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> dict:
        """Преобразование объекта книги в словарь."""

        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Создание объекта книги из словаря."""

        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data.get("status", Status.AVAILABLE.value),
        )
