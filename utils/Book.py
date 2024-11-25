
class Book():
    id:int
    title:str
    author:str
    year:int
    status:str

    def __init__(self, book_dict:dict) -> None:
        """Инициализация объекта класса Book

        Args:
            book_dict (dict): Словарь книги
        """
        self.status = "в наличии"
        for k,v in book_dict.items():
            self.__setattr__(k, v)

    def __str__(self) -> str:
        return f"\t{self.id}\t|\t{self.title}\t|\t{self.author}\t|\t{self.year}\t|\t{self.status}"

