from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    def to_dict(self):
        author_as_dict = {}
        author_as_dict["id"] = self.id
        author_as_dict["name"] = self.name

        return author_as_dict

    @classmethod
    def from_dict(cls, author_data):
        new_author = Author(name=author_data["name"])
        return new_author
    
    def update_from_dict(self, author_data):
        if "name" in author_data:
            self.name = author_data["name"]
