from sqlalchemy import Integer, String, Column, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, DeclarativeMeta


Base: DeclarativeMeta = declarative_base()


class Goods(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True, autoincrement=True)
    goods_name = Column(String(40), nullable=False)
    goods_description = Column(String)
    goods_price = Column(Integer)
    seller_id = Column(Integer)

    children = relationship("Reviews", back_populates="parent")


class Reviews(Base):
    __tablename__ = 'reviews'

    goods_id = Column(Integer, ForeignKey('goods.goods_id'), primary_key=True)
    user_id = Column(Integer, primary_key=True)
    review = Column(Text)
    stars = Column(Integer)

    parent = relationship("Goods", back_populates="children")

    __table_args__ = (
        CheckConstraint('stars >= 0'),
        CheckConstraint('stars <= 5')
    )

