from oxyde import Field, Model


class Author(Model):
    id: int | None = Field(default=None, db_pk=True)
    name: str
    bio: str | None = Field(default=None)
    books: list["Book"] = Field(db_reverse_fk="author")

    class Meta:
        is_table = True
        table_name = "authors"


class Book(Model):
    id: int | None = Field(default=None, db_pk=True)
    title: str
    year: int | None = Field(default=None)
    author: Author | None = Field(default=None, db_on_delete="CASCADE")

    class Meta:
        is_table = True
        table_name = "books"
