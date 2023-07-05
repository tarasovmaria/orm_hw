import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, drop_tables, Publishers, Books, Shops, Stocks, Sales

DSN = f'postgresql://postgres:password.@localhost:5432/bookshop'
# Я пыталась разобраться с os и получением параметров из окружения через .getenv и config, но не могу до конца понять логику написания кода для этого. Буду признательна, если сможете объяснить.
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

with open('C:\\Users\\Admin\\Desktop\\orm\\test_data.json', 'r') as f:
    data = json.load(f)

for r in data:
    model = {
        'publisher': Publishers,
        'shop': Shops,
        'book': Books,
        'stock': Stocks,
        'sale': Sales,
    }[r.get('model')]
    session.add(model(id=r.get('pk'), **r.get('fields')))
session.commit()

def get_sales_info_by_publisher(publisher_info=None):
    request = session.query(Books.title, Shops.name, Sales.price, Sales.date_sale).select_from(Shops).join(Stocks, Stocks.id_shop == Shops.id).join(Books, Books.id == Stocks.id_book).join(Publishers, Publishers.id == Books.id_publisher).join(Sales, Sales.id_stock == Stocks.id)
    if publisher_info.isdigit():
        request = request.filter(Publishers.id == publisher_info).all()
        for book_title, shop, price, date in request:
            print(f"{book_title: <40} | {shop: <10} | {price: <8} | {date.strftime('%d-%m-%Y')}")
    else:
        request = request.filter(Publishers.name == publisher_info).all()
        for book_title, shop, price, date in request:
            print(f"{book_title: <40} | {shop: <10} | {price: <8} | {date.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    drop_tables(engine)
    create_tables(engine)
    publisher_info = input('Введите название издательства или id: ')
    get_sales_info_by_publisher(publisher_info)
session.close()
