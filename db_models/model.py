from sqlalchemy import Integer, String, Column, ForeignKey, Text, CheckConstraint, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship, DeclarativeMeta


Base: DeclarativeMeta = declarative_base()


class AllUsers(Base):
    __tablename__ = 'all_users'
    global_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(40), nullable=False)
    password = Column(String(40), nullable=False)
    role = Column(String(1), nullable=False)


class Goods(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True, autoincrement=True)
    goods_name = Column(String(40), nullable=False)
    goods_description = Column(String)
    goods_price = Column(Integer)
    seller_id = Column(Integer, ForeignKey('sellers.seller_id'), nullable=False)
    is_visible = Column(Boolean)


class Reviews(Base):
    __tablename__ = 'reviews'

    goods_id = Column(Integer, ForeignKey('goods.goods_id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    review = Column(Text)
    stars = Column(Integer)

    __table_args__ = (
        CheckConstraint('stars >= 0'),
        CheckConstraint('stars <= 5')
    )


class Customers(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, ForeignKey('all_users.global_id'), primary_key=True)
    phone_number = Column(String(11), unique=True)
    email = Column(String(40), unique=True)
    customer_name = Column(String(40), nullable=False)
    birthday = Column(DateTime)
    city = Column(String(40))
    basket = Column(JSONB, default={})


class Sellers(Base):
    __tablename__ = 'sellers'

    seller_id = Column(Integer, ForeignKey('all_users.global_id'), primary_key=True)
    seller_name = Column(String(40))

