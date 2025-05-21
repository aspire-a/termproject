from sqlalchemy.orm import relationship
from user.model import db


class CurrencySymbol(db.Model):
    __tablename__ = "Currency_Symbol"

    symbol = db.Column("Symbol", db.String(10), primary_key=True)
    name   = db.Column("Name", db.String(40), nullable=False)

    currencies = relationship("Currency", back_populates="symbol_ref")


class Currency(db.Model):
    __tablename__ = "Currency"

    currency_id = db.Column("Currency ID", db.Integer,
                             primary_key=True, autoincrement=True)
    name   = db.Column("Name", db.String(40), nullable=False)
    symbol = db.Column("Symbol", db.String(10),
                        db.ForeignKey('Currency_Symbol."Symbol"'),
                        nullable=False)
    status = db.Column("Status", db.String(20))

    symbol_ref  = relationship(CurrencySymbol, back_populates="currencies")
    crypto_meta = relationship("CryptoCurrency", uselist=False,
                               back_populates="currency")
    fiat_meta   = relationship("FiatCurrency", uselist=False,
                               back_populates="currency")
    markets     = relationship("CurrencyHasMarket", back_populates="currency")


class CryptoCurrency(db.Model):
    __tablename__ = "Crypto_Currency"

    currency_id = db.Column("Currency ID", db.Integer,
                             db.ForeignKey('Currency."Currency ID"'),
                             primary_key=True)
    rank         = db.Column("Rank", db.Integer)
    market_cap   = db.Column("Market Cap", db.BigInteger)
    trading_vol  = db.Column("Trading Volume", db.BigInteger)
    circulation  = db.Column("Circulation Supply", db.BigInteger)
    total_supply = db.Column("Total Supply", db.BigInteger)
    max_supply   = db.Column("Max Suppply", db.BigInteger)
    ath          = db.Column("ATH", db.Float)
    atl          = db.Column("ATL", db.Float)

    currency = relationship(Currency, back_populates="crypto_meta")


class FiatCurrency(db.Model):
    __tablename__ = "Fiat_Currency"

    currency_id = db.Column("Currency ID", db.Integer,
                             db.ForeignKey('Currency."Currency ID"'),
                             primary_key=True)
    origin      = db.Column("Origin", db.String(60))

    currency = relationship(Currency, back_populates="fiat_meta")
