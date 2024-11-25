import json
import os

from utils.Book import Book
from utils.BookSerializer import BookSerializer

class Books():
    def __init__(self, json_path:str = None, books:list[Book] = None) -> None:
        """Инициализация класса книг

        Args:
            json_path (str, optional): Путь к json файлу с книгами. По умолчанию None.
            books (list[Book], optional): Готовый лист book. По умолчанию None.
        """
        if json_path:
            self.json_path = json_path
            if not os.path.exists(os.path.abspath(self.json_path)):
                with open(self.json_path, "wt", encoding="utf-8") as f:
                    f.write("[]")
            self.books:list[Book] = [Book(i) for i in self.json]
        elif books:
            self.books:list[Book] = books
        else:
            raise ValueError("Ошибка инициализации, нет исходных данных")

        
    @property
    def json(self) -> dict:
        """Возвращает все книги в формате словаря 

        Returns:
            dict: массив со словарями книг
        """
        return json.load(open(os.path.abspath(self.json_path), "r", encoding="utf-8"))
    
    def last_id(self):
        return max([i.id for i in self.books]) or 1
    
    def save(self, save_path:str = None):
        """Сохраняет текущие книги в переданный путь

        Args:
            save_path (str): путь к файлу
        """
        json.dump(
                self.books,
                open(os.path.abspath(self.json_path), "wt", encoding="utf-8") if not save_path else save_path,
                ensure_ascii=False,
                cls=BookSerializer,
                indent=4
            )
    
    def insert(self, **kwargs) -> Book | Exception:
        """Добавляет книгу в базу

        Returns:
            Book: Объект книги или исключение
        """
        try:
            self.books.append(Book({"id":self.__last_id() + 1, **kwargs}))
        except Exception as e:
            return e
        return self.books[-1]
    
    def delete_by_id(self, id:int) -> Book | Exception:
        """Удаляет книгу из базы

        Args:
            id (int): id целевой книги
        Returns:
            Book: Объект книги или исключение
        """
        for i, b in enumerate(self.books):
            if b.id == id:
                return self.books.pop(i)
        return Exception("Не найден id")
                
    def search_by(self, prop_name:str, target_value:str) -> list[Book]:
        """Ищет по книги по целевому значению

        Args:
            prop_name (str): имя поля для поиска
            target_value (str): целевое значение

        Returns:
            list[Book]: Результаты поиска, массив книг
        """
        return [book for book in self.books if str(getattr(book, prop_name)) and (str(getattr(book, prop_name)) in str(target_value) or str(target_value) in str(getattr(book, prop_name)))]
    
    def update(self, id:int, prop_name:str, prop_value:str|int) -> Book | Exception:
        """Изменяет поля книги

        Args:
            id (int): id целевой книги
            prop_name (str): имя поля, которое нужно обновить
            prop_value (str | int): новое значение поля
        Returns:
            Book: Объект книги или исключение
        """
        cast = int if isinstance(getattr(self.books[0], prop_name), int) else str
        for b in self.books:
            if b.id == id:
                setattr(b, prop_name, cast(prop_value))
                return b
        return Exception("Не найден id")
    
    def get_or_none(self, id:int) -> Book | None:
        """Возвращает книгу по id, если она существует, иначе None

        Args:
            id (int): id книги

        Returns:
            Book | None: Книга или None
        """
        for b in self.books:
            if b.id == id:
                return b
        return None


    
    def __str__(self) -> str:
        headers = ["Статус", "ID", "Название", "Автор", "Год выпуска"]

        # Данные
        data = [j.__dict__.values() for j in self.books]

        column_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]

        def __format_row(row, widths):
            return " | ".join(str(item).ljust(width) for item, width in zip(row, widths))

        header_row = __format_row(headers, column_widths)

        separator = "-+-".join("-" * width for width in column_widths)

        data_rows = [__format_row(row, column_widths) for row in data]

        return f"{header_row}\n{separator}\n" + "\n".join(data_rows)



    


    