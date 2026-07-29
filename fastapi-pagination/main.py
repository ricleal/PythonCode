from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

app = FastAPI()
add_pagination(app)

engine = create_engine("sqlite:///:memory:")


# -- Database Models --
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()


# -- Pydantic Models --
class UserOut(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    name: str
    age: int


# -- Application Startup --


@app.on_event("startup")
def on_startup():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)
    with Session(engine) as session:
        session.add_all(
            [
                User(id=idx + 1001, name=f"User {idx}", age=idx % 30)
                for idx in range(200)
            ]
        )
        session.commit()


# -- API Endpoints --


@app.get("/users")
def get_users() -> CursorPage[UserOut]:
    with Session(engine) as session:
        return paginate(session, select(User).order_by(User.id))


@app.get("/users/{user_id}")
def get_user(user_id: int) -> UserOut:
    with Session(engine) as session:
        return session.get(User, user_id)


@app.post("/users", status_code=201)
def create_user(user: UserIn) -> UserOut:
    with Session(engine) as session:
        db_user = User(name=user.name, age=user.age)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
