from sqlalchemy import func, desc
from flask_login import current_user, AnonymousUserMixin
from models import db, User, Transaction, Market, PriceHistory, Currency, CryptoCurrency
from collections import defaultdict
from decimal import Decimal


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


def _latest_usdt_price(ccy: str) -> Decimal | None:
    """
    Return Decimal close-price converting one unit of *ccy* to USDT,
    based on the newest PriceHistory row of either “CCY/USDT”
    or “USDT/CCY”.  None if no market data.
    """
    pair_a = f"{ccy}/USDT"
    pair_b = f"USDT/{ccy}"

    # find the market id and direction
    mkt = (db.session.query(Market)
           .filter(Market.name.in_([pair_a, pair_b]))
           .first())
    if not mkt:
        return None

    # latest close price
    price_row = (db.session.query(PriceHistory.close_price)
                 .filter(PriceHistory.market_id == mkt.market_id)
                 .order_by(PriceHistory.close_time.desc())
                 .first())
    if not price_row:
        return None

    price = Decimal(str(price_row.close_price))

    # if market is inverse (USDT/CCY), invert the rate
    return price if mkt.name == pair_a else (Decimal("1") / price)


def top_users(limit: int = 5):
    """
    Top *limit* users by **average USD/USDT value** of deposits that are
    APPROVED.  Returns list[(User, avg_usd: Decimal)] sorted desc.
    """

    # 1. pull raw deposits we care about
    deposits = (db.session.query(Transaction)
                .filter(Transaction.status == "COMPLETED",
                        Transaction.type == "DEPOSIT")
                .all())

    if not deposits:
        return []

    # 2. build a price cache for all non-USD(T) symbols encountered
    symbols_needed = {t.currency for t in deposits
                      if t.currency not in ("USD", "USDT")}
    price_cache: dict[str, Decimal | None] = {
        sym: _latest_usdt_price(sym) for sym in symbols_needed
    }

    # 3. per-user aggregation
    totals: defaultdict[int, Decimal] = defaultdict(Decimal)
    counts: defaultdict[int, int]     = defaultdict(int)

    for tx in deposits:
        amt = Decimal(str(tx.amount))
        if tx.currency in ("USD", "USDT"):
            usd_val = amt
        else:
            rate = price_cache.get(tx.currency)
            if rate is None:
                continue                     # skip if no price data
            usd_val = amt * rate

        totals[tx.user_id] += usd_val
        counts[tx.user_id] += 1

    # 4. compute averages & fetch User objects
    entries = []
    if totals:
        users = {u.user_id: u for u in
                 db.session.query(User).filter(User.user_id.in_(totals)).all()}
        for uid, total in totals.items():
            avg = total / counts[uid]
            entries.append((users[uid], avg))

    # 5. sort & limit
    entries.sort(key=lambda tup: tup[1], reverse=True)
    return entries[:limit]


def current_user_name():
    if isinstance(current_user, AnonymousUserMixin):
        return "Welcome to CryptoCase"
    return f"{current_user.name} {current_user.surname}"
