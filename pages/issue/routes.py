from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import services as svc


def register_routes(bp):
    @bp.route("/", methods=["GET", "POST"])
    @login_required
    def index():
        if request.method == "POST":
            try:
                svc.create_issue(request.form["type"],
                                 request.form["description"])
                flash("Issue submitted — our team will contact you.", "success")
                return redirect(url_for("home.index"))
            except ValueError as ve:
                flash(str(ve), "danger")
            except RuntimeError as re:
                flash("Internal error — try again later." + str(re), "danger")

        return render_template(
            "issue/index.html",
            types=svc.ALLOWED_TYPES,
            user=current_user,
        )
