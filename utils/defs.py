from utils.Books import Books

def create_book(books:Books):
    """Принимает и валидирует параметры для добавления книги, добавляет книгу

    Args:
        books (Books): Объект Books
    """
    print("Введите название книги")
    title = input()
    print("Введите автора книги")
    author = input()
    print("Введите год выпуска книги")
    year, err = validate_input(input(), float("inf"))
    year_flag = False
    while err:
        print("Не правильный ввод года, он должен быть целым числом, повторите попытку ввода. Введите -1, если хотите отменить создание книги.")
        year, err = validate_input(input(), float("inf"))
        if year == -1:
            year_flag = True
            break
        if not err:
            break
    if year_flag:
        return
    new_book = books.insert(title = title, author = author, year = year)
    books.save()
    print("Новая книга добавлена!")
    print(new_book)

def delete_book(books:Books):
    """Принимает и валидирует параметры для удаления книги, удаляет книгу

    Args:
        books (Books): Объект Books
    """
    while True:
        print(books)
        print("Введите id книги, которую вы хотите удалить.")
        last_id = books.last_id()
        b_id, err = validate_input(input(), last_id)
        b_id_flag = False
        if b_id == -1:
            return
        while err:
            print(f"Не правильный ввод id, он должен быть целым числом, и быть меньше {last_id}. Введите -1, если хотите отменить удаление книги.")
            b_id, err = validate_input(input(), last_id)
            if b_id == -1:
                b_id_flag = True
                break
            if not err:
                break
        if b_id_flag:
            return
        new_book = books.get_or_none(b_id)
        if not new_book:
            print("Книга не найдена, введите другой id. Для отмены введите -1")
            continue
        else:
            break
    new_book = books.delete_by_id(b_id)
    books.save()
    print("Книга удалена!")
    print(new_book)
    print("Если вы хотите восстановить книгу введите 1, иначе нажмите на enter")
    remove, err = validate_input(input(), 1)
    if not err and remove == 1:
        books.books.append(new_book)
        books.save()
        print("Удаление отменено!")

def search_books(books:Books):
    """Принимает и валидирует параметры для поиска книги, выводит книгу в консоль

    Args:
        books (Books): Объект Books
    """
    while True:
        print("Выберите поле, по которому хотите осуществить поиск.")
        print("1. Название")
        print("2. Автор")
        print("3. Год выпуска")
        print("-1. Выйти")
        choise, err = validate_input(input(), 3)
        if choise == -1:
            return
        choise_flag = False
        while err:
            print(f"Не правильный ввод. Введите целое число от 1 до 3, если хотите отменить поиск книги введите -1.")
            choise, err = validate_input(input(), 3)
            if choise == -1:
                choise_flag = True
                break
            if not err:
                break
        if choise_flag:
            return
        match choise:
            case 1:
                print("Введите название или часть названия книги.")
                user_title = input()
                found_books = books.search_by("title", user_title)
            case 2:
                print("Введите имя автора или часть имени автора книги.")
                user_author = input()
                found_books = books.search_by("author", user_author)
            case 3:
                print("Введите год выпуска или несколько известных цифр года выпуска книги.")
                user_year = input()
                found_books = books.search_by("year", user_year)
        if found_books:
            print("Вот, что мне удалось найти:")
            print(Books(books=found_books))
            return
        print("Ничего не удалось найти, попробуйте другой критерий.")

def update_book(books:Books):
    """Принимает и валидирует параметры для изменения книги, обновляет книгу

    Args:
        books (Books): Объект Books
    """
    while True:
        print(books)
        print("Введите id книги, которую вы хотите обновить.")
        last_id = books.last_id()
        b_id, err = validate_input(input(), last_id)
        b_id_flag = False
        if b_id == -1:
            return
        while err:
            print(f"Не правильный ввод id, он должен быть целым числом, и быть меньше {last_id}. Введите -1, если хотите отменить удаление книги.")
            b_id, err = validate_input(input(), last_id)
            if b_id == -1:
                b_id_flag = True
                break
            if not err:
                break
        if b_id_flag:
            return
        new_book = books.get_or_none(b_id)
        if not new_book:
            print("Книга не найдена, введите другой id. Для отмены введите -1")
            continue
        else:
            break
    books.update(b_id, "status", "в наличии" if new_book.status == "выдана" else "выдана")
    books.save()
    print("Книга обновлена!")
    print(new_book)

def validate_input(input_str:str, num:int) -> list[int|str, bool]:
    """Функция для валидации ввода

    Returns:
        list[int|str, bool]: Обработанный или не обработанный в случае ошибки, была ли ошибка
    """
    try:
        input_str = int(input_str)
    except:
        pass
    if not isinstance(input_str, int):
        return input_str, True
    if input_str < 1 or input_str > num:
        return input_str, True
    return input_str, False