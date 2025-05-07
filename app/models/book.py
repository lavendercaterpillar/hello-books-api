# Database Backed Book Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    # author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    # author: Mapped[Optional["Author"]] = relationship(back_populates="book")


    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description

        return book_as_dict


    @classmethod
    def from_dict(cls, book_data):
        new_book_ins = Book(title=book_data["title"], description=book_data["description"])
        return new_book_ins
    

    def update_from_dict(self, book_data):
        if "title" in book_data:
            self.title = book_data["title"]
        if "description" in book_data:
            self.description = book_data["description"]
        
