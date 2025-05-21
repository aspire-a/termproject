from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from flask_login import (login_user, logout_user, login_required, current_user)
from user.service import create_user, authenticate

bp = Blueprint(
    "user", __name__,
    url_prefix="/user",
    template_folder="templates"
)


# ---------- Register --------------------------------------------------
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        surname = request.form["surname"]
        password = request.form["password"]
        try:
            create_user(email, name, surname, password)
            flash("Account created. Please log in.", "success")
            return redirect(url_for("user.login"))
        except ValueError as err:
            flash(str(err), "danger")
    return render_template("user/register.html")


# ---------- Login -----------------------------------------------------
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = authenticate(email, password)
        if user:
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("user/login.html")


# ---------- Logout ----------------------------------------------------
@bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("user.login"))
