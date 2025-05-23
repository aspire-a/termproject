from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import db, Currency
from . import services as svc


def register_routes(bp):

    @bp.get("/")
    @login_required
    def index():
        wallet, holdings = svc.wallet_summary()
        all_symbols = [c.symbol for c in
                       db.session.query(Currency.symbol)
                       .order_by(Currency.symbol).all()]
        return render_template(
            "wallet/index.html",
            wallet=wallet,
            holdings=holdings,
            symbols=all_symbols  # ← pass to template
        )

    @bp.post("/deposit")
    @login_required
    def do_deposit():
        try:
            svc.deposit(request.form["currency"], request.form["amount"])
            flash("Deposit request received.", "success")
        except ValueError as ve:
            flash(str(ve), "danger")
        except RuntimeError as rer:
            flash("Internal error" + str(rer), "danger")
        return redirect(url_for("wallet.index"))

    @bp.post("/withdraw")
    @login_required
    def do_withdraw():
        try:
            svc.withdraw(request.form["currency"], request.form["amount"])
            flash("Withdraw request submitted.", "success")
        except ValueError as ve:
            flash(str(ve), "danger")
        except RuntimeError as rer:
            flash("Internal error" + str(rer), "danger")
        return redirect(url_for("wallet.index"))
