from utils.Books import Books
from utils.defs import *


def main():
    books = Books("books.json")
    print("Добро пожаловать в консольное приложение для системы управления библиотекой!")
    while True:
        print("Что бы вы хотели сделать?")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Посмотреть все книги")
        print("5. Изменение данных книги")
        choise = input()
        try:
            choise = int(choise)
        except:
            pass
        choise, err = validate_input(choise, 5)
        if err:
            print("Не корректный ввод, повторите попытку, вы можете ввести только цифру от 1 до 5.")
            continue
        match choise:
            case 1:
                create_book(books)
            case 2:
                delete_book(books)
            case 3:
                search_books(books)
            case 4:
                print(books)
            case 5:
                update_book(books)
            case _:
                continue


if __name__ == "__main__":
    main()