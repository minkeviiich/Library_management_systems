from library import Library
from messages import Messages


def display_menu() -> None:
    """
    Отображение главного меню.
    """
    print("\n" + "=" * 40)
    print("{:^40}".format("СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ"))
    print("=" * 40)
    print("{:<2} | {:<30}".format("1.", "Добавить книгу"))
    print("{:<2} | {:<30}".format("2.", "Удалить книгу"))
    print("{:<2} | {:<30}".format("3.", "Найти книгу"))
    print("{:<2} | {:<30}".format("4.", "Отобразить все книги"))
    print("{:<2} | {:<30}".format("5.", "Изменить статус книги"))
    print("{:<2} | {:<30}".format("6.", "Выход"))
    print("=" * 40)
    print("\nВыберите действие: ", end="")


def input_with_validation(prompt: str, validation_type: str) -> any:
    """
    Функция для получения ввода с валидацией.
    """
    while True:
        user_input = input(prompt).strip()
        if validation_type == "int":
            if user_input.isdigit():
                return int(user_input)
            else:
                print("Некорректный ввод. Пожалуйста, введите число.")
        elif validation_type == "str":
            if user_input.isalpha():
                return user_input
            else:
                print("Некорректный ввод. Пожалуйста, введите текст.")


def add_book(library: Library) -> None:
    """Функция для добавления книги в библиотеку."""

    title = input("Введите название книги: ").strip()
    author = input_with_validation("Введите автора книги: ", "str")
    year = input_with_validation("Введите год издания книги: ", "int")
    library.add_book(title, author, year)


def remove_book(library: Library) -> None:
    """Функция для удаления книги из библиотеки."""

    book_id = input_with_validation("Введите id книги: ", "int")
    library.remove_book(book_id)


def search_books(library: Library) -> None:
    """Функция для поиска книг в библиотеке."""

    search_type = input_with_validation(
        "Поиск по: 1 - Названию, 2 - Автору, 3 - Году издания: ", "int"
    )
    value = input("Введите значение для поиска: ").strip()
    library.search_books(search_type, value)


def change_status(library: Library) -> None:
    """Функция для изменения статуса книги."""

    book_id = input_with_validation("Введите id книги: ", "int")
    books = library.load_books()
    if not any(book.id == book_id for book in books):
        print(Messages.BOOK_NOT_FOUND)
    else:
        new_status = input_with_validation(
            "Изменить статус на: 1 - В наличии, 2 - Выдана: ", "int"
        )
        library.change_status(book_id, new_status)


def perform_action(choice: int, library: Library) -> bool:
    """
    Выполнение действия, выбранного пользователем из меню.
    """
    if choice == 1:
        add_book(library)
    elif choice == 2:
        remove_book(library)
    elif choice == 3:
        search_books(library)
    elif choice == 4:
        library.display_books()
    elif choice == 5:
        change_status(library)
    elif choice == 6:
        print(Messages.EXIT)
        return False
    else:
        print(Messages.INVALID_INPUT)
    return True


def main() -> None:
    """Функция для запуска программы."""
    library = Library()

    while True:
        display_menu()
        choice = input_with_validation("", "int")
        if perform_action(choice, library):
            while True:
                print("\nХотите выполнить это действие еще раз или вернуться в меню?")
                print("1. Повторить действие")
                print("2. Вернуться в меню")
                next_action = input_with_validation("", "int")
                if next_action == 1:
                    perform_action(choice, library)
                elif next_action == 2:
                    break
                else:
                    print(Messages.INVALID_INPUT)
        else:
            break


if __name__ == "__main__":
    main()
