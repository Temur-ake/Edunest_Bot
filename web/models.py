from sqlalchemy import create_engine, BIGINT, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine(f'postgresql+psycopg2://postgres:1@localhost:5449/postgres_temur')
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
    phone_number1: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    phone_number2: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    channel_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    channel_link: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    channel_name1: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    channel_link1: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    instagram_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    instagram_link: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    you_tube_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    you_tube_link: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    latitude: Mapped[float]
    longtitude: Mapped[float]

    def __repr__(self) -> str:
        return (f'Contact (phone_number1{self.phone_number1!r},phone_number2{self.phone_number2!r},'
                f'email{self.channel_link!r},id{self.id!r},longtitude{self.longtitude!r},latitude{self.longtitude!r}')


class News(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(VARCHAR(255))
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    image: Mapped[str] = mapped_column(VARCHAR(255))
    price: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)

    def __repr__(self) -> str:
        return (f'Contact (title{self.title!r},description{self.description!r},'
                f'image{self.image!r},id{self.id!r},price{self.price!r}')


class Course(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))


class Level(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    course: Mapped["Course"] = relationship("Course", back_populates="levels")


Course.levels = relationship("Level", back_populates="course")

Base.metadata.create_all(engine)
