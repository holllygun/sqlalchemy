
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
DSN = '...'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

pub = input('Введите id или имя автора')
if pub.isdigit():
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == int(pub))
else:
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name.like(pub))

#почему не работает "|" ?
# query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter((Publisher.id == int(pub)) | (Publisher.name == pub))

for q in query.all():
    print(f'Название книги: {q[0]} | Магазин: {q[1]} | Стоимость: {str(q[2])} | Дата: {str(q[3])}')
