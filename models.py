import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


# def book():
class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length = 60))
    stocks = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer,sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, back_populates="stocks")

    __table_args__ = (
        sq.UniqueConstraint('id_book', 'id_shop'),
    )


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.String(length=30))
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


