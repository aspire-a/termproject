from flask import Blueprint
from .routes import register_routes

bp = Blueprint("auth", __name__,
               url_prefix="/auth",
               template_folder="templates")

register_routes(bp)
