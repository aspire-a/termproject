from sqlalchemy.orm import relationship
from user.model import db, User


class WalletHasCurrency(db.Model):
    __tablename__ = "Wallet_has_Currency"

    wallet_id   = db.Column("Wallet ID", db.Integer,
                             db.ForeignKey('Wallet."Wallet ID"'),
                             primary_key=True)
    currency_id = db.Column("Currency ID", db.Integer,
                             db.ForeignKey('Currency."Currency ID"'),
                             primary_key=True)
    quantity    = db.Column("Quantity", db.Float)

    wallet   = relationship("Wallet", back_populates="currencies")
    currency = relationship("Currency")


class Wallet(db.Model):
    __tablename__ = "Wallet"

    wallet_id     = db.Column("Wallet ID", db.Integer,
                               primary_key=True, autoincrement=True)
    status        = db.Column("Status", db.String(30))
    total_balance = db.Column("Total Balance", db.Float)
    user_id       = db.Column("User ID", db.Integer,
                               db.ForeignKey('User."User ID"'),
                               nullable=False)

    user       = relationship(User, backref="wallet", uselist=False)
    currencies = relationship(
        WalletHasCurrency,
        back_populates="wallet",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Wallet {self.wallet_id} ({self.status})>"
