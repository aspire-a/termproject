from flask import render_template
from flask_login import login_required
from . import services as svc


def register_routes(bp):

    @bp.get("/")
    @login_required
    def index():
        rows = svc.open_markets_with_price()
        return render_template("market/index.html", rows=rows)
