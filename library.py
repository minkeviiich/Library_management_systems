import json
from typing import List
from book import Book
from statuses import Status
from messages import Messages


class Library:
    """Класс для управления библиотекой книг."""

    def __init__(self, filename: str = "books.json"):
        """
        Инициализация библиотеки с указанием имени файла для хранения данных.
        """
        self.filename: str = filename

    def load_books(self) -> List[Book]:
        """Загрузка книг из JSON файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                return [Book.from_dict(book) for book in books_data]
        except FileNotFoundError:
            return []

    def save_books(self, books: List[Book]) -> None:
        """Сохранение списка книг в JSON файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in books],
                file, indent=2, ensure_ascii=False
            )

    def get_next_id(self, books: List[Book]) -> int:
        """Получение следующего уникального идентификатора для новой книги."""
        if not books:
            return 1
        return max(book.id for book in books) + 1

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавление новой книги в библиотеку.
        """
        books = self.load_books()
        # Приведение всех строк к нижнему регистру для проверки
        normalized_title = title.lower().strip()
        normalized_author = author.lower().strip()

        if any(
            book.title.lower() == normalized_title
            and book.author.lower() == normalized_author
            and book.year == year
            for book in books
        ):
            print(Messages.INVALID_ADDED)
            return

        new_id = self.get_next_id(books)
        new_book = Book(new_id, title, author, year)
        books.append(new_book)
        self.save_books(books)
        print(Messages.BOOK_ADDED)

    def remove_book(self, book_id: int) -> None:
        """
        Удаление книги из библиотеки по идентификатору.
        """
        books = self.load_books()
        updated_books = [book for book in books if book.id != book_id]
        if len(updated_books) == len(books):
            print(Messages.BOOK_NOT_FOUND)
        else:
            self.save_books(updated_books)
            print(Messages.BOOK_REMOVED)

    def search_books(self, search_type: int, value: str) -> None:
        """
        Поиск книг в библиотеке по заданным критериям.
        """
        books = self.load_books()
        results = []
        if search_type == 1:
            results = [
                book for book in books
                if book.title.lower() == value.lower()
            ]
        elif search_type == 2:
            results = [
                book for book in books
                if book.author.lower() == value.lower()
            ]
        elif search_type == 3:
            results = [
                book for book in books
                if str(book.year) == value
            ]

        if results:
            for book in results:
                self.print_book(book)
        else:
            print(Messages.BOOK_NOT_FOUND)

    def display_books(self) -> None:
        """
        Отображение всех книг в библиотеке.
        """
        books = self.load_books()
        if books:
            for book in books:
                self.print_book(book)
        else:
            print(Messages.NO_BOOKS)

    def change_status(self, book_id: int, new_status: int) -> None:
        """
        Изменение статуса книги по идентификатору.
        """
        books = self.load_books()
        for book in books:
            if book.id == book_id:
                desired_status = (
                    Status.AVAILABLE.value
                    if new_status == 1 else Status.BORROWED.value
                )
                if book.status == desired_status:
                    print("Такой статус уже установлен.")
                    return
                book.status = desired_status
                self.save_books(books)
                print("Статус книги изменен.")
                return
        print(Messages.BOOK_NOT_FOUND)

    @staticmethod
    def print_book(book: Book) -> None:
        """
        Печать информации о книге.
        """
        print(f"\n{'='*40}")
        print(f"ID: {book.id}")
        print(f"Название: {book.title}")
        print(f"Автор: {book.author}")
        print(f"Год издания: {book.year}")
        print(f"Статус: {book.status}")
        print(f"{'='*40}")
