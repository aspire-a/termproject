from flask import Blueprint
from .routes import register_routes

bp = Blueprint(
    "market_details", __name__,
    url_prefix="/market/details",
    template_folder="templates"
)

register_routes(bp)
