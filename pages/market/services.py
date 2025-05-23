from sqlalchemy import func
from models import db, Market, PriceHistory


def open_markets_with_price():
    """
    Return list[(Market, latest_close_price)] for markets with status 'OPEN'.
    """
    # sub-query: each market’s newest close_time
    last = (db.session.query(
                PriceHistory.market_id,
                func.max(PriceHistory.close_time).label("last_time"))
            .group_by(PriceHistory.market_id)
            .subquery())

    # join to fetch the corresponding close_price
    latest_price = (db.session.query(
                        PriceHistory.market_id,
                        PriceHistory.close_price)
                    .join(last, (PriceHistory.market_id == last.c.market_id) &
                                (PriceHistory.close_time == last.c.last_time))
                    .subquery())

    return (db.session.query(Market, latest_price.c.close_price)
            .join(latest_price, Market.market_id == latest_price.c.market_id)
            .filter(Market.status == "OPEN")
            .order_by(Market.name)
            .all())
