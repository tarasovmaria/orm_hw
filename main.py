import json


import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publishers, Books, Shops, Stocks, Sales

DSN = f'postgresql://postgres:password@localhost:5432/bookshop'
    
engine = sqlalchemy.create_engine(DSN)

if __name__ == '__main__':
    create_tables(engine)
    # drop_tables(engine)

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

publisher_name = str(input('Введите название издательства: '))
publisher_id = int(input('Введите id издательства: '))

def get_sales_info_by_publisher(publisher_name=None, publisher_id=None):
    if publisher_id is not None and publisher_name is None:
        for c in session.query(Books.title).join(Stocks.book).join(Stocks.shop).join(Shops.name).join(Sales.stock).join(Sales.price).join(Sales.date_sale).filter(Publishers.id == publisher_id):
            print(c)
    elif publisher_name is not None and publisher_id is None:
        for c in session.query(Books.title).join(Stocks.book).join(Stocks.shop).join(Shops.name).join(Sales.stock).join(Sales.price).join(Sales.date_sale).filter(Publishers.name == publisher_name):
            print(c)
    elif publisher_name is not None and publisher_id is not None:
        for c in session.query(Books.title).join(Stocks.book).join(Stocks.shop).join(Shops.name).join(Sales.stock).join(Sales.price).join(Sales.date_sale).filter(Publishers.name == publisher_name, Publishers.id == publisher_id):
            print(c)
    elif publisher_name is None and publisher_id is None:
        print('Введите необходимые сведения об издательстве!')

if __name__ == '__main__':
    # get_sales_info_by_publisher(publisher_name, publisher_id)
    # get_sales_info_by_publisher(None, publisher_id)
    get_sales_info_by_publisher(publisher_name, None)

session.close()