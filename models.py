import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

Base = declarative_base()

class Publishers(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True, nullable=False)
    def __str__(self):
        return f'Издатель {self.id}: {self.name}'

class Books(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publishers, backref="book")
    def __str__(self):
        return f'Книга {self.id}: {self.title}'

class Shops(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)
    def __str__(self):
        return f'Магазин {self.id}: {self.name}'

class Stocks(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, default=0, nullable=False)
    book = relationship(Books, backref="stock")
    shop = relationship(Shops, backref="stock")
    def __str__(self):
        return f'Наличие {self.id} книги {self.book.c.title}: {self.count}'

class Sales(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer,primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, default=date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stocks, backref="sale")
    def __str__(self):
        return f'Покупка {self.id}: на сумму {self.price}, количество {self.count} {self.date_sale}'

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)