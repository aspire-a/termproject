from sqlalchemy.orm import relationship
from user.model import db, User
from .market import Market, OrderBook


class Trade(db.Model):
    __tablename__ = "Trade"

    trade_id   = db.Column("Trade ID", db.Integer,
                            primary_key=True, autoincrement=True)
    price      = db.Column("Price", db.Float)
    quantity   = db.Column("Quantity", db.Float)
    trade_time = db.Column("Trade Time", db.DateTime)
    market_id  = db.Column("Market ID", db.Integer,
                            db.ForeignKey('Market."Market ID"'),
                            nullable=False)

    market = relationship(Market, back_populates="trades")
    orders = relationship("Order", back_populates="trade")


class Order(db.Model):
    __tablename__ = "Order"

    order_id      = db.Column("Order ID", db.Integer,
                               primary_key=True, autoincrement=True)
    type          = db.Column("Type", db.String(10))
    status        = db.Column("Status", db.String(20))
    quantity      = db.Column("Quantity", db.Float)
    price         = db.Column("Price", db.Float)
    creation_time = db.Column("Creation Time", db.DateTime)
    close_time    = db.Column("Close Time", db.DateTime)

    user_id        = db.Column("User ID", db.Integer,
                                db.ForeignKey('User."User ID"'), nullable=False)
    market_id      = db.Column("Market ID", db.Integer,
                                db.ForeignKey('Market."Market ID"'), nullable=False)
    trade_id       = db.Column("Trade ID", db.Integer,
                                db.ForeignKey('Trade."Trade ID"'), nullable=False)
    market_id_book = db.Column("Market ID (Book)", db.Integer,
                                db.ForeignKey('Order_Book."Market ID"'),
                                nullable=False)

    user   = relationship(User, backref="orders")
    market = relationship(Market, back_populates="orders")
    trade  = relationship(Trade, back_populates="orders")
    book   = relationship(OrderBook)
