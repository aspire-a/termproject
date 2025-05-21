from flask import Flask, render_template
from flask_login import (LoginManager, login_required, current_user)
from flask_migrate import Migrate
from dotenv import load_dotenv
import os, logging

from user import db, bp as user_bp               # import shared objects
from user.model import User

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = "user.login"          # redirect here if needed

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY              = os.getenv("SECRET_KEY", "dev-secret"),
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    db.init_app(app)
    import models
    # -----------------------------------------------------Alembic CLI
    migrate = Migrate()
    migrate.init_app(app, db)  # now `flask db …` works
    # ----------------------------------------------------------------

    login_manager.init_app(app)
    app.register_blueprint(user_bp)

    @app.get("/")
    def home():
        return """render_template("home.html")"""

    @app.get("/dashboard")
    @login_required
    def dashboard():
        return """"render_template("dashboard.html")"""

    # # INFO logs show in console
    # app.logger.setLevel(logging.INFO)
    # with app.app_context():
    #     db.session.execute("SELECT 1")
    #     app.logger.info("✅ Connected to Postgres!")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
