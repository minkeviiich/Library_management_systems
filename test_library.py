import unittest
from io import StringIO
import sys
from book import Book
from library import Library
from statuses import Status


class TestBook(unittest.TestCase):
    """
    Тесты для класса Book.
    """

    def test_book_initialization(self):
        """Тестирование инициализации объекта Book."""

        book = Book(1, "Harry Potter", "J. K. Rowling", 1997)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Harry Potter")
        self.assertEqual(book.author, "J. K. Rowling")
        self.assertEqual(book.year, 1997)
        self.assertEqual(book.status, Status.AVAILABLE.value)

    def test_book_to_dict(self):
        """Тестирование метода to_dict() класса Book."""

        book = Book(1, "Harry Potter", "J. K. Rowling", 1997)
        book_dict = book.to_dict()
        expected_dict = {
            "id": 1,
            "title": "Harry Potter",
            "author": "J. K. Rowling",
            "year": 1997,
            "status": Status.AVAILABLE.value,
        }
        self.assertEqual(book_dict, expected_dict)

    def test_book_from_dict(self):
        """Тестирование метода from_dict() класса Book."""

        book_dict = {
            "id": 1,
            "title": "Harry Potter",
            "author": "J. K. Rowling",
            "year": 1997,
            "status": Status.AVAILABLE.value,
        }
        book = Book.from_dict(book_dict)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Harry Potter")
        self.assertEqual(book.author, "J. K. Rowling")
        self.assertEqual(book.year, 1997)
        self.assertEqual(book.status, Status.AVAILABLE.value)


class TestLibrary(unittest.TestCase):
    """Тесты для класса Library."""

    def setUp(self):
        """Настройка окружения для тестов."""

        self.library = Library(filename="test_books.json")
        self.library.save_books([])

    def test_add_book(self):
        """Тестирование метода add_book() класса Library."""

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        books = self.library.load_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Harry Potter")
        self.assertEqual(books[0].author, "J. K. Rowling")
        self.assertEqual(books[0].year, 1997)

    def test_remove_book(self):
        """Тестирование метода remove_book() класса Library."""

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        books = self.library.load_books()
        book_id = books[0].id
        self.library.remove_book(book_id)
        books = self.library.load_books()
        self.assertEqual(len(books), 0)

    def test_search_books_by_title(self):
        """
        Тестирование метода search_books() класса Library
        при поиске по названию.
        """

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.library.search_books(1, "Harry Potter")
            output = out.getvalue().strip()
            self.assertIn("ID: 1", output)
            self.assertIn("Название: Harry Potter", output)
            self.assertIn("Автор: J. K. Rowling", output)
            self.assertIn("Год издания: 1997", output)
            self.assertIn("Статус: в наличии", output)
        finally:
            sys.stdout = saved_stdout

    def test_search_books_by_author(self):
        """
        Тестирование метода search_books() класса Library
        при поиске по автору.
        """

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.library.search_books(2, "J. K. Rowling")
            output = out.getvalue().strip()
            self.assertIn("ID: 1", output)
            self.assertIn("Название: Harry Potter", output)
            self.assertIn("Автор: J. K. Rowling", output)
            self.assertIn("Год издания: 1997", output)
            self.assertIn("Статус: в наличии", output)
        finally:
            sys.stdout = saved_stdout

    def test_search_books_by_year(self):
        """
        Тестирование метода search_books() класса Library
        при поиске по году издания.
        """

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.library.search_books(3, "1997")
            output = out.getvalue().strip()
            self.assertIn("ID: 1", output)
            self.assertIn("Название: Harry Potter", output)
            self.assertIn("Автор: J. K. Rowling", output)
            self.assertIn("Год издания: 1997", output)
            self.assertIn("Статус: в наличии", output)
        finally:
            sys.stdout = saved_stdout

    def test_display_books(self):
        """
        Тестирование метода display_books() класса Library.
        """

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.library.display_books()
            output = out.getvalue().strip()
            self.assertIn("ID: 1", output)
            self.assertIn("Название: Harry Potter", output)
            self.assertIn("Автор: J. K. Rowling", output)
            self.assertIn("Год издания: 1997", output)
            self.assertIn("Статус: в наличии", output)
        finally:
            sys.stdout = saved_stdout

    def test_change_status(self):
        """
        Тестирование метода change_status() класса Library.
        """

        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        books = self.library.load_books()
        book_id = books[0].id
        self.library.change_status(book_id, 2)
        books = self.library.load_books()
        self.assertEqual(books[0].status, Status.BORROWED.value)
        self.library.change_status(book_id, 1)
        books = self.library.load_books()
        self.assertEqual(books[0].status, Status.AVAILABLE.value)

    def test_get_next_id(self):
        """
        Тестирование метода get_next_id() класса Library.
        """

        books = self.library.load_books()
        next_id = self.library.get_next_id(books)
        self.assertEqual(next_id, 1)
        self.library.add_book("Harry Potter", "J. K. Rowling", 1997)
        books = self.library.load_books()
        next_id = self.library.get_next_id(books)
        self.assertEqual(next_id, 2)

    def tearDown(self):
        """
        Удаление тестового файла после завершения тестов.
        """

        import os

        os.remove("test_books.json")


if __name__ == "__main__":
    unittest.main()
