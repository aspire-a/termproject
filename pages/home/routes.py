from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, logout_user
from . import services as svc


def register_routes(bp):

    @bp.route("", methods=["GET"])
    def index():
        # query parameters
        status = request.args.get("status")          # active/inactive/None
        sort   = request.args.get("sort")            # market_cap / volume
        search = request.args.get("q")               # symbol search

        cryptos = svc.crypto_query(status, sort, search)
        leaders = svc.top_users()

        return render_template(
            "home/index.html",
            cryptos=cryptos,
            leaders=leaders,
            user_name=svc.current_user_name(),
            is_auth=current_user.is_authenticated,
            query=request.args
        )

    # top-bar logout action (post redirect get)
    @bp.post("logout")
    @login_required
    def do_logout():
        logout_user()
        return redirect(url_for("home.index"))
