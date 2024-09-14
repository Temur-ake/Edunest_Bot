from sqlalchemy import create_engine, BIGINT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine(f'postgresql+psycopg2://postgres:1@localhost:5432/postgres_temur')
session = Session(bind=engine)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT)


class Contact(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number1: Mapped[str] = mapped_column(VARCHAR(255))
    phone_number2: Mapped[str] = mapped_column(VARCHAR(255))
    channel: Mapped[str] = mapped_column(VARCHAR(255))
    email: Mapped[str] = mapped_column(VARCHAR(255))
    latitude: Mapped[float]
    longtitude: Mapped[float]

    def __repr__(self) -> str:
        return (f'Contact (phone_number1{self.phone_number1!r},phone_number2{self.phone_number2!r},'
                f'email{self.email!r},id{self.id!r},longtitude{self.longtitude!r},latitude{self.longtitude!r}')


class News(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(VARCHAR(255))
    title: Mapped[str] = mapped_column(VARCHAR(255))
    image: Mapped[str] = mapped_column(VARCHAR(255))
    price: Mapped[str] = mapped_column(VARCHAR(255))

    def __repr__(self) -> str:
        return (f'Contact (title{self.title!r},description{self.description!r},'
                f'image{self.image!r},id{self.id!r},price{self.price!r}')


Base.metadata.create_all(engine)
