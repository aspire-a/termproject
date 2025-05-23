from sqlalchemy.orm import relationship
from models import db, User
from .market import Market, OrderBook


class Trade(db.Model):
    __tablename__ = "trade"

    trade_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price      = db.Column(db.Float)
    quantity   = db.Column(db.Float)
    trade_time = db.Column(db.DateTime)
    market_id  = db.Column(db.Integer,
                            db.ForeignKey("market.market_id"),
                            nullable=False)

    market = relationship(Market, back_populates="trades")
    orders = relationship("Order", back_populates="trade")


class Order(db.Model):
    __tablename__ = "order"

    order_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type          = db.Column(db.String(10))
    status        = db.Column(db.String(20))
    quantity      = db.Column(db.Float)
    price         = db.Column(db.Float)
    creation_time = db.Column(db.DateTime)
    close_time    = db.Column(db.DateTime)

    user_id        = db.Column(db.Integer,
                               db.ForeignKey("user.user_id"), nullable=False)
    market_id      = db.Column(db.Integer,
                               db.ForeignKey("market.market_id"), nullable=False)
    trade_id       = db.Column(db.Integer,
                               db.ForeignKey("trade.trade_id"))
    order_book_id  = db.Column(db.Integer,
                               db.ForeignKey("order_book.market_id"),
                               nullable=False)

    user   = relationship(User,   backref="orders")
    market = relationship(Market, back_populates="orders")
    trade  = relationship(Trade,  back_populates="orders")
    book   = relationship(OrderBook)
