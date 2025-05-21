"""
Expose a single `db` instance plus every model so that:

• Alembic's autogenerate sees the full metadata
• Other packages can `from models import Something`
"""

# ---- shared db instance comes from the User feature ------------------
from user.model import db  # do NOT create a new SQLAlchemy()

# ---- core feature group imports (order doesn’t matter) ---------------
# wallet & bridge
from .wallet import Wallet, WalletHasCurrency

# currency hierarchy
from .currency import (
    CurrencySymbol, Currency,
    CryptoCurrency, FiatCurrency
)

# market & price data
from .market import (
    Market, OrderBook, PriceHistory,
    CurrencyHasMarket
)

# trading layer
from .trading import Trade, Order

# customer-support / finance
from .agent import (
    CustomerServiceAgent, Issue, Transaction
)

# ---- what gets re-exported on `from models import *` -----------------
__all__ = [
    # db handle
    "db",
    # wallet
    "Wallet", "WalletHasCurrency",
    # currency
    "CurrencySymbol", "Currency",
    "CryptoCurrency", "FiatCurrency",
    # market
    "Market", "OrderBook", "PriceHistory", "CurrencyHasMarket",
    # trading
    "Trade", "Order",
    # support / finance
    "CustomerServiceAgent", "Issue", "Transaction",
]
