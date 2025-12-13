from model.book import Book
from pydantic import BaseModel
from typing import List


class BookCollection(BaseModel):

    books: List[Book]