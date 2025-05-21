from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .services import create_user, authenticate

def register_routes(bp):
    @bp.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            try:
                create_user(
                  request.form["email"],
                  request.form["name"],
                  request.form["surname"],
                  request.form["password"]
                )
                flash("Account created. Please log in.", "success")
                return redirect(url_for("auth.login"))
            except ValueError as err:
                flash(str(err), "danger")
        return render_template("auth/register.html")

    @bp.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = authenticate(
              request.form["email"],
              request.form["password"]
            )
            if user:
                login_user(user)
                flash("Logged in.", "success")
                return redirect(url_for("home.index"))
            flash("Invalid credentials", "danger")
        return render_template("auth/login.html")

    @bp.get("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out.", "info")
        return redirect(url_for("home.index"))
