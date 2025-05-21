from sqlalchemy.orm import relationship
from user.model import db


class Market(db.Model):
    __tablename__ = "market"

    market_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name          = db.Column(db.String(40), nullable=False)
    status        = db.Column(db.String(20))
    creation_time = db.Column(db.DateTime, nullable=False)

    order_book    = relationship("OrderBook",     uselist=False,
                                 back_populates="market",
                                 cascade="all, delete-orphan")
    price_history = relationship("PriceHistory",  back_populates="market",
                                 cascade="all, delete-orphan")
    trades        = relationship("Trade",         back_populates="market")
    orders        = relationship("Order",         back_populates="market")
    currencies    = relationship("CurrencyHasMarket",
                                 back_populates="market")


class OrderBook(db.Model):
    __tablename__ = "order_book"

    market_id   = db.Column(db.Integer,
                            db.ForeignKey("market.market_id"),
                            primary_key=True)
    update_time = db.Column(db.DateTime)

    market = relationship(Market, back_populates="order_book")


class PriceHistory(db.Model):
    __tablename__ = "price_history"

    price_id    = db.Column(db.Integer, primary_key=True)
    market_id   = db.Column(db.Integer, primary_key=True)
    high_price  = db.Column(db.Float)
    low_price   = db.Column(db.Float)
    open_price  = db.Column(db.Float)
    close_price = db.Column(db.Float)
    open_time   = db.Column(db.DateTime)
    close_time  = db.Column(db.DateTime)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["market_id"], ["market.market_id"], ondelete="CASCADE"
        ),
    )

    market = relationship(Market, back_populates="price_history")


class CurrencyHasMarket(db.Model):
    __tablename__ = "currency_has_market"

    currency_id = db.Column(db.Integer,
                            db.ForeignKey("currency.currency_id"),
                            primary_key=True)
    market_id   = db.Column(db.Integer,
                            db.ForeignKey("market.market_id"),
                            primary_key=True)

    currency = relationship("Currency", back_populates="markets")
    market   = relationship(Market, back_populates="currencies")
