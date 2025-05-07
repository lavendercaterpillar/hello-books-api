from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    # books: Mapped[list["Book"]] = relationship(back_populates="author")


    def to_dict(self):
        author_as_dict = {}
        author_as_dict["id"] = self.id
        author_as_dict["name"] = self.name
        # author_as_dict["book_id"] = 

        return author_as_dict

    @classmethod
    def from_dict(cls, author_data):
        new_author = Author(name=author_data["name"]) # , book_id.get())
        return new_author
    
    def update_from_dict(self, author_data):
        if "name" in author_data:
            self.name = author_data["name"]
