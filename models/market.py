from sqlalchemy.orm import relationship
from user.model import db


class Market(db.Model):
    __tablename__ = "Market"

    market_id     = db.Column("Market ID", db.Integer,
                               primary_key=True, autoincrement=True)
    name          = db.Column("Name", db.String(40), nullable=False)
    status        = db.Column("Status", db.String(20))
    creation_time = db.Column("Creation Time", db.DateTime, nullable=False)

    order_book    = relationship("OrderBook", uselist=False,
                                 back_populates="market",
                                 cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="market",
                                 cascade="all, delete-orphan")
    trades        = relationship("Trade", back_populates="market")
    orders        = relationship("Order", back_populates="market")
    currencies    = relationship("CurrencyHasMarket", back_populates="market")


class OrderBook(db.Model):
    __tablename__ = "Order_Book"

    market_id   = db.Column("Market ID", db.Integer,
                             db.ForeignKey('Market."Market ID"'),
                             primary_key=True)
    update_time = db.Column("Update Time", db.DateTime)

    market = relationship(Market, back_populates="order_book")


class PriceHistory(db.Model):
    __tablename__ = "Price_History"

    price_id    = db.Column("Price ID", db.Integer, primary_key=True)
    market_id   = db.Column("Market ID", db.Integer, primary_key=True)
    high_price  = db.Column("High Price", db.Float)
    low_price   = db.Column("Low Price", db.Float)
    open_price  = db.Column("Open Price", db.Float)
    close_price = db.Column("Close Price", db.Float)
    open_time   = db.Column("Open Time", db.DateTime)
    close_time  = db.Column("Close Time", db.DateTime)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["Market ID"], ['Market."Market ID"'], ondelete="CASCADE"
        ),
    )

    market = relationship(Market, back_populates="price_history")


class CurrencyHasMarket(db.Model):
    __tablename__ = "Currency_has_Market"

    currency_id = db.Column("Currency ID", db.Integer,
                             db.ForeignKey('Currency."Currency ID"'),
                             primary_key=True)
    market_id   = db.Column("Market ID", db.Integer,
                             db.ForeignKey('Market."Market ID"'),
                             primary_key=True)

    currency = relationship("Currency", back_populates="markets")
    market   = relationship(Market, back_populates="currencies")
