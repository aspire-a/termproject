from sqlalchemy.orm import relationship
from models import db, User


class WalletHasCurrency(db.Model):
    __tablename__ = "wallet_has_currency"

    wallet_id   = db.Column(db.Integer,
                            db.ForeignKey("wallet.wallet_id"),
                            primary_key=True)
    currency_id = db.Column(db.Integer,
                            db.ForeignKey("currency.currency_id"),
                            primary_key=True)
    quantity    = db.Column(db.Float)

    wallet   = relationship("Wallet",   back_populates="currencies")
    currency = relationship("Currency")


class Wallet(db.Model):
    __tablename__ = "wallet"

    wallet_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status        = db.Column(db.String(30))
    total_balance = db.Column(db.Float)
    user_id       = db.Column(db.Integer,
                              db.ForeignKey("user.user_id"),
                              nullable=False)

    user       = relationship(User, backref="wallet", uselist=False)
    currencies = relationship(
        WalletHasCurrency,
        back_populates="wallet",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Wallet {self.wallet_id} ({self.status})>"
