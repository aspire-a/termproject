from flask import Blueprint
from .routes import register_routes

bp = Blueprint(
    "home", __name__,
    url_prefix="/",  # root URL
    template_folder="templates"
)

register_routes(bp)
