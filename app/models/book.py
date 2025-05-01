# Database Backed Book Model
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    # indented under the Book class definition
    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description

        return book_as_dict

    # indented under the Book class definition
    @classmethod
    def from_dict(cls, book_data):
        new_book_ins = Book(title=book_data["title"], description=book_data["description"])
        return new_book_ins