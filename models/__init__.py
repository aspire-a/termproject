from flask_sqlalchemy import SQLAlchemy

# one shared instance
db = SQLAlchemy()

# --- import every table module *after* db created --------------------
from .user     import User
from .wallet   import Wallet, WalletHasCurrency
from .currency import (
    CurrencySymbol, Currency,
    CryptoCurrency, FiatCurrency
)
from .market   import Market, OrderBook, PriceHistory, CurrencyHasMarket
from .trading  import Trade, Order
from .agent    import CustomerServiceAgent, Issue, Transaction
# ---------------------------------------------------------------------

__all__ = [
    "db", "User",
    "Wallet", "WalletHasCurrency",
    "CurrencySymbol", "Currency", "CryptoCurrency", "FiatCurrency",
    "Market", "OrderBook", "PriceHistory", "CurrencyHasMarket",
    "Trade", "Order",
    "CustomerServiceAgent", "Issue", "Transaction",
]
