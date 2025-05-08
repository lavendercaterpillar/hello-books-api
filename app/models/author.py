from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author") # This line defines relationship (and not an attr)

    # without this line pylance gives a warning on line 7 "Book"
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .book import Book


    def to_dict(self):
        author_as_dict = {}
        author_as_dict["id"] = self.id
        author_as_dict["name"] = self.name

        return author_as_dict


    @classmethod
    def from_dict(cls, author_data):
        new_author = cls(name=author_data["name"]) # , book_id.get())
        return new_author


    def update_from_dict(self, author_data):
        if "name" in author_data:
            self.name = author_data["name"]
