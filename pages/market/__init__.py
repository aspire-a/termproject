from flask import Blueprint
from .routes import register_routes

bp = Blueprint(
    "market", __name__,
    url_prefix="/market",
    template_folder="templates"
)

register_routes(bp)
