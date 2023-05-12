import sqlalchemy as sq
import json
from sqlalchemy.orm import declarative_base, sessionmaker

database = "  "
login = "  "
password = "  "
DSN = f"postgresql://{login}:{password}@localhost:5432/{database}"
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Publisher(Base):
    __tablename__="publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30))


class Book(Base):
    __tablename__='book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)


class Shop(Base):
    __tablename__='shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30))  
  

class Stock(Base):
    __tablename__='stock'
    id = sq.Column(sq.Integer,primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable = False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable = False)
    count = sq.Column(sq.Integer)


class Sale(Base):
    __tablename__="sale"
    id = sq.Column(sq.Integer,primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer,sq.ForeignKey("stock.id"),nullable = False)
    count = sq.Column(sq.Integer)


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def upload_data():
    with open('tests_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            model = {'publisher': Publisher,'shop': Shop,'book': Book,'stock': Stock,'sale': Sale}[item.get('model')]
            session.add(model(id=item.get('pk'), **item.get('fields')))
            session.commit()

        
def find_data():
    find_name = input('Enter name to find data: ')
    try:
        publisher_id = session.query(Publisher).filter(Publisher.name == find_name).first()
        for i in session.query(Book).filter(Book.id_publisher == publisher_id.id).all():
            for c in session.query(Stock).filter(Stock.id_book == i.id).all():
                for x in session.query(Sale).filter(Sale.id_stock == c.id).all():
                    print(i.title,end =" | ")
                    print(session.query(Shop).filter(Shop.id == c.id_shop).first().name, end =" | ")
                    print(x.price, end =" | ")
                    print(x.date_sale)
    except AttributeError:
        return print('data does not exists')

if __name__ == '__main__':
    # create_tables(engine)
    # upload_data()
    find_data()
    
    session.close()