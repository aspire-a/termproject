from sqlalchemy import func, desc
from flask_login import current_user, AnonymousUserMixin
from models import db, Currency, CryptoCurrency, Transaction, User


def crypto_query(status: str | None = None,
                 sort: str | None = None,
                 search: str | None = None):
    """
    Return a SQLAlchemy query for the crypto list with optional
    status filter, search by symbol, and sort.
    """
    q = (db.session.query(Currency, CryptoCurrency)
         .join(CryptoCurrency, Currency.currency_id == CryptoCurrency.currency_id))

    if status:
        q = q.filter(Currency.status == status)

    if search:
        q = q.filter(Currency.symbol.ilike(f"%{search.strip()}%"))

    if sort == "volume":
        q = q.order_by(desc(CryptoCurrency.trading_vol))
    else:        # default → market_cap
        q = q.order_by(desc(CryptoCurrency.market_cap))

    return q.all()


def top_users(limit: int = 5):
    """
    Return top *limit* users by count(tx) desc.
    """
    sub = (db.session.query(
                Transaction.user_id,
                func.count(Transaction.transaction_id).label("tx_count"))
           .group_by(Transaction.user_id)
           .order_by(desc("tx_count"))
           .limit(limit)
           .subquery())

    return (db.session.query(User, sub.c.tx_count)
            .join(sub, User.user_id == sub.c.user_id)
            .all())


def current_user_name():
    if isinstance(current_user, AnonymousUserMixin):
        return "Welcome to CryptoCase"
    return f"{current_user.name} {current_user.surname}"
