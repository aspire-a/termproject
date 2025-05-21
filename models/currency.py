from sqlalchemy.orm import relationship
from user.model import db


class CurrencySymbol(db.Model):
    __tablename__ = "currency_symbol"

    symbol = db.Column(db.String(10), primary_key=True)
    name   = db.Column(db.String(40), nullable=False)

    currencies = relationship("Currency", back_populates="symbol_ref")


class Currency(db.Model):
    __tablename__ = "currency"

    currency_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(40), nullable=False)
    symbol      = db.Column(db.String(10),
                            db.ForeignKey("currency_symbol.symbol"),
                            nullable=False)
    status      = db.Column(db.String(20))

    symbol_ref  = relationship(CurrencySymbol, back_populates="currencies")
    crypto_meta = relationship("CryptoCurrency", uselist=False,
                               back_populates="currency")
    fiat_meta   = relationship("FiatCurrency",   uselist=False,
                               back_populates="currency")
    markets     = relationship("CurrencyHasMarket", back_populates="currency")


class CryptoCurrency(db.Model):
    __tablename__ = "crypto_currency"

    currency_id  = db.Column(db.Integer,
                             db.ForeignKey("currency.currency_id"),
                             primary_key=True)
    rank         = db.Column(db.Integer)
    market_cap   = db.Column(db.BigInteger)
    trading_vol  = db.Column(db.BigInteger)
    circulation  = db.Column(db.BigInteger)
    total_supply = db.Column(db.BigInteger)
    max_supply   = db.Column(db.BigInteger)
    ath          = db.Column(db.Float)
    atl          = db.Column(db.Float)

    currency = relationship(Currency, back_populates="crypto_meta")


class FiatCurrency(db.Model):
    __tablename__ = "fiat_currency"

    currency_id = db.Column(db.Integer,
                             db.ForeignKey("currency.currency_id"),
                             primary_key=True)
    origin      = db.Column(db.String(60))

    currency = relationship(Currency, back_populates="fiat_meta")
