
from datetime import datetime, timezone
from sqlalchemy import desc, and_
from models import (
    db,
    Market,
    PriceHistory,
    Order,
    Trade,
    OrderBook,
    WalletHasCurrency,
    Currency,
)


def latest_price(market_id: int) -> float | None:
    row = (
        db.session.query(PriceHistory.close_price)
        .filter(PriceHistory.market_id == market_id)
        .order_by(PriceHistory.close_time.desc())
        .first()
    )
    return row.close_price if row else None


def place_order(user, market_id: int, order_type: str, qty: float, limit_price: float):
    """
    Insert the taker order, then match it greedily against existing OPEN orders.
    On each match we immediately debit & credit both wallets.
    """
    assert order_type in ("BUY", "SELL")
    book_id = market_id  # 1:1 mapping in your schema

    # 1) Create the new (taker) order
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
    db.session.add(new_order)
    db.session.flush()  # so new_order.order_id is assigned

    # 2) Try to match against existing orders
    _match_orders(new_order)

    # 3) Persist everything
    db.session.commit()
    return new_order


def _decrease(wallet, symbol: str, amount: float):
    """Remove `amount` of `symbol` from `wallet` (error if insufficient)."""
    cur = Currency.query.filter_by(symbol=symbol).first()
    link = WalletHasCurrency.query.filter_by(
        wallet_id=wallet.wallet_id, currency_id=cur.currency_id
    ).first()
    if not link or link.quantity < amount:
        raise ValueError(f"Insufficient {symbol} balance")
    link.quantity -= amount


def _increase(wallet, symbol: str, amount: float):
    """Add `amount` of `symbol` to `wallet` (create link row if needed)."""
    cur = Currency.query.filter_by(symbol=symbol).first()
    link = WalletHasCurrency.query.filter_by(
        wallet_id=wallet.wallet_id, currency_id=cur.currency_id
    ).first()
    if not link:
        link = WalletHasCurrency(
            wallet_id=wallet.wallet_id,
            currency_id=cur.currency_id,
            quantity=0.0,
        )
        db.session.add(link)
    link.quantity += amount


def _symbols_for_market(market_id: int) -> tuple[str, str]:
    """Return (base_symbol, quote_symbol), e.g. ("BNB","USDT")."""
    name = Market.query.get(market_id).name  # e.g. "BTC/USDT"
    base, quote = name.split("/")
    return base, quote


def _match_orders(order: Order):
    """Greedy price/time matching producing Trade rows + settlement per trade."""
    # opposite side
    opp_type = "SELL" if order.type == "BUY" else "BUY"
    # sorting / price condition
    cmp_fn = desc if order.type == "BUY" else (lambda x: x)
    price_cond = (
        Order.price <= order.price if order.type == "BUY" else Order.price >= order.price
    )

    # fetch all candidates
    candidates = (
        Order.query
        .filter(
            and_(
                Order.market_id == order.market_id,
                Order.status == "OPEN",
                Order.type == opp_type,
                price_cond,
            )
        )
        .order_by(cmp_fn(Order.price), Order.creation_time)
        .all()
    )

    qty_left = order.quantity
    base_sym, quote_sym = _symbols_for_market(order.market_id)

    for opp in candidates:
        if qty_left <= 0:
            break

        tradable = min(qty_left, opp.quantity)
        exec_price = opp.price  # taker uses maker’s price

        # 1) Record the trade
        trade = Trade(
            price=exec_price,
            quantity=tradable,
            trade_time=datetime.now(timezone.utc),
            market_id=order.market_id,
        )
        db.session.add(trade)
        db.session.flush()

        # 2) Tie both orders to this trade
        order.trade_id = trade.trade_id
        opp.trade_id = trade.trade_id

        # 3) Update raw quantities & status
        qty_left -= tradable
        opp.quantity -= tradable
        if opp.quantity == 0:
            opp.status = "FILLED"
            opp.close_time = datetime.now(timezone.utc)

        # 4) Immediately settle both wallets
        _settle_wallets(
            base_sym,
            quote_sym,
            buyer=(order if order.type == "BUY" else opp),
            seller=(opp if order.type == "BUY" else order),
            qty=tradable,
            price=exec_price,
        )

    # 5) Finalise taker
    order.quantity = qty_left
    if qty_left == 0:
        order.status = "FILLED"
        order.close_time = datetime.now(timezone.utc)


def _settle_wallets(
    base_sym: str,
    quote_sym: str,
    buyer: Order,
    seller: Order,
    qty: float,
    price: float,
):
    """
    For each trade:
      - buyer pays quote and receives base
      - seller gives base and receives quote
    """
    buyer_wallet = buyer.user.wallet
    seller_wallet = seller.user.wallet

    # Buyer side
    _decrease(buyer_wallet, quote_sym, qty * price)
    _increase(buyer_wallet, base_sym, qty)

    # Seller side
    _decrease(seller_wallet, base_sym, qty)
    _increase(seller_wallet, quote_sym, qty * price)