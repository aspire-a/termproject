from flask import Blueprint
from .routes import register_routes

bp = Blueprint(
    "issue", __name__,
    url_prefix="/issue",
    template_folder="templates"    # (HTML will be added later)
)

register_routes(bp)
