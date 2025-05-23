from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from models import db, User           # shared db + model registry
import models                         # populate metadata
from pages import register_all_blueprints

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY              = os.getenv("SECRET_KEY", "dev-secret"),
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    db.init_app(app)
    Migrate(app, db)

    lm = LoginManager(app)
    lm.login_view = "auth.login"

    @lm.user_loader
    def load_user(uid):
        return User.query.get(int(uid))

    register_all_blueprints(app)

    @app.get("/")
    def root():
        return redirect(url_for("home.index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
