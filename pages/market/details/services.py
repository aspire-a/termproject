from datetime import datetime, timezone
from sqlalchemy import desc, and_, or_
from models import (
    db, Market, PriceHistory, Order, Trade, OrderBook,
    Wallet, WalletHasCurrency, Currency, User
)


def latest_price(market_id: int) -> float | None:
    row = (db.session.query(PriceHistory.close_price)
           .filter(PriceHistory.market_id == market_id)
           .order_by(PriceHistory.close_time.desc())
           .first())
    return row.close_price if row else None


# ────────────────────────────────────────────────────────────────────
#  Order placement + matching
# ────────────────────────────────────────────────────────────────────
def place_order(user: User, market_id: int, order_type: str,
                qty: float, limit_price: float):
    """
    Insert order then try to match against the order-book.
    On success creates Trade rows, updates wallets, and marks
    orders FILLED / partially filled.
    """
    assert order_type in ("BUY", "SELL")
    book_id = market_id  # 1-to-1 mapping in schema

    new_order = Order(
        type=order_type,
        status="OPEN",
        quantity=qty,
        price=limit_price,
        creation_time=datetime.now(timezone.utc),
        user_id=user.user_id,
        market_id=market_id,
        order_book_id=book_id,
    )
    _reserve_funds(user, market_id, order_type, qty, limit_price)
    db.session.add(new_order)
    db.session.flush()  # so new_order.order_id is set

    _match_orders(new_order)
    db.session.commit()
    return new_order


def _reserve_funds(user: User, market_id: int,
                   order_type: str, qty: float, price: float):
    """Simple balance check / reservation."""
    base_sym, quote_sym = _symbols_for_market(market_id)

    wallet = user.wallet or Wallet(user_id=user.user_id, status="ACTIVE")
    if order_type == "SELL":
        _decrease(wallet, base_sym, qty)  # must exist
    else:  # BUY
        _decrease(wallet, quote_sym, qty * price)  # pay in quote curr


def _decrease(wallet: Wallet, symbol: str, amount: float):
    cur = Currency.query.filter_by(symbol=symbol).first()
    link = WalletHasCurrency.query.filter_by(
        wallet_id=wallet.wallet_id,
        currency_id=cur.currency_id
    ).first()
    if not link or link.quantity < amount:
        raise ValueError("Insufficient balance")
    link.quantity -= amount


def _increase(wallet: Wallet, symbol: str, amount: float):
    cur = Currency.query.filter_by(symbol=symbol).first()
    link = WalletHasCurrency.query.filter_by(
        wallet_id=wallet.wallet_id,
        currency_id=cur.currency_id
    ).first()
    if not link:
        link = WalletHasCurrency(wallet_id=wallet.wallet_id,
                                 currency_id=cur.currency_id,
                                 quantity=0)
        db.session.add(link)
    link.quantity += amount


def _symbols_for_market(market_id: int):
    name = Market.query.get(market_id).name  # e.g. 'BTC/USDT'
    base, quote = name.split("/")
    return base, quote


def _match_orders(order: Order):
    """Greedy price/time matching producing trades."""
    opp_type = "SELL" if order.type == "BUY" else "BUY"

    cmp = desc if order.type == "BUY" else lambda x: x  # BUY wants lowest ask
    price_cond = (op := (Order.price <= order.price) if order.type == "BUY"
    else (Order.price >= order.price))

    candidates = (Order.query
                  .filter(and_(Order.market_id == order.market_id,
                               Order.status == "OPEN",
                               Order.type == opp_type,
                               price_cond))
                  .order_by(cmp(Order.price), Order.creation_time)
                  .all())

    qty_left = order.quantity
    base_sym, quote_sym = _symbols_for_market(order.market_id)

    for opp in candidates:
        if qty_left <= 0:
            break
        tradable = min(qty_left, opp.quantity)
        exec_price = opp.price  # taker uses maker’s price

        # create trade
        trade = Trade(
            price=exec_price,
            quantity=tradable,
            trade_time=datetime.now(timezone.utc),
            market_id=order.market_id
        )
        db.session.add(trade)
        db.session.flush()

        for o in (order, opp):
            o.trade_id = trade.trade_id

        # update quantities & status
        qty_left -= tradable
        opp.quantity -= tradable
        if opp.quantity == 0:
            opp.status = "FILLED"
            opp.close_time = datetime.now(timezone.utc)

        _settle_wallets(base_sym, quote_sym,
                        buyer=(order if order.type == "BUY" else opp),
                        seller=(opp if order.type == "BUY" else order),
                        qty=tradable, price=exec_price)

    # finalise taker order
    order.quantity = qty_left
    if qty_left == 0:
        order.status = "FILLED"
        order.close_time = datetime.now(timezone.utc)


def _settle_wallets(base_sym, quote_sym, buyer, seller, qty, price):
    # buyer gets base, pays quote; seller vice-versa
    buyer_wallet = buyer.user.wallet
    seller_wallet = seller.user.wallet

    _increase(buyer_wallet, base_sym, qty)
    _increase(seller_wallet, quote_sym, qty * price)
