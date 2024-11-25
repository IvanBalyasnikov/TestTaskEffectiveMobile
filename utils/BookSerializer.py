import json
from utils.Book import Book

class BookSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)