from flask import Blueprint
from .routes import register_routes

bp = Blueprint(
    "wallet", __name__,
    url_prefix="/wallet",
    template_folder="templates"
)

register_routes(bp)
