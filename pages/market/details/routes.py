from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import services as svc
from models import Market


def register_routes(bp):
    # view page
    @bp.get("/<int:market_id>")
    @login_required
    def view(market_id):
        market = Market.query.get_or_404(market_id)
        price = svc.latest_price(market_id)
        base, quote = market.name.split("/")
        return render_template("market/details/index.html",
                               market=market, price=price,
                               base=base, quote=quote)

    # place order
    @bp.post("/<int:market_id>/order")
    @login_required
    def place(market_id):
        try:
            qty = float(request.form["qty"])
            limit = float(request.form["limit"])
            side = request.form["side"]  # BUY / SELL
            svc.place_order(current_user, market_id, side, qty, limit)
            flash("Order submitted.", "success")
        except ValueError as ve:
            flash(str(ve), "danger")
        except Exception as e:
            flash("Internal error" + str(e), "danger")
        return redirect(url_for("market_details.view", market_id=market_id))
