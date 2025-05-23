from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from models import (
    db, Wallet, WalletHasCurrency,
    Currency, Transaction
)


def _get_or_create_wallet():
    w = Wallet.query.filter_by(user_id=current_user.user_id).first()
    if w:
        return w
    w = Wallet(user_id=current_user.user_id, status="ACTIVE", total_balance=0)
    db.session.add(w)
    db.session.commit()
    return w


def wallet_summary():
    """
    Returns (wallet, list[(Currency.symbol, Quantity)])
    """
    w = _get_or_create_wallet()
    holdings = (db.session.query(Currency.symbol, WalletHasCurrency.quantity)
                .join(WalletHasCurrency,
                      WalletHasCurrency.currency_id == Currency.currency_id)
                .filter(WalletHasCurrency.wallet_id == w.wallet_id)
                .all())
    return w, holdings


def deposit(symbol: str, amount_str: str):
    amount = float(amount_str)
    if amount <= 0:
        raise ValueError("Amount must be positive")

    cur = Currency.query.filter_by(symbol=symbol).first()
    if not cur:
        raise ValueError("Currency not found")

    w = _get_or_create_wallet()

    # upsert into wallet_has_currency
    link = WalletHasCurrency.query.filter_by(
        wallet_id=w.wallet_id,
        currency_id=cur.currency_id
    ).first()
    if not link:
        link = WalletHasCurrency(wallet_id=w.wallet_id,
                                 currency_id=cur.currency_id,
                                 quantity=0.0)
        db.session.add(link)
    link.quantity += amount

    tx = Transaction(
        type="DEPOSIT",
        currency=symbol,
        amount=float(amount),
        status="PENDING",
        request_time=datetime.now(timezone.utc),
        approve_time=None,
        user_id=current_user.user_id,
        agent_id=1
    )

    db.session.add(tx)
    _commit()


def withdraw(symbol: str, amount_str: str):
    amount = float(amount_str)
    if amount <= 0:
        raise ValueError("Amount must be positive")

    cur = Currency.query.filter_by(symbol=symbol).first()
    if not cur:
        raise ValueError("Currency not found")

    w = _get_or_create_wallet()
    link = WalletHasCurrency.query.filter_by(
        wallet_id=w.wallet_id,
        currency_id=cur.currency_id
    ).first()

    if not link or link.quantity < amount:
        raise ValueError("Insufficient balance")

    link.quantity -= amount

    tx = Transaction(
        type="WITHDRAWAL",
        currency=symbol,
        amount=float(amount),
        status="PENDING",
        request_time=datetime.now(timezone.utc),
        approve_time=None,
        user_id=current_user.user_id,
        agent_id=1
    )
    db.session.add(tx)
    _commit()


def _commit():
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        raise RuntimeError("DB error "+ str(err)) from err
