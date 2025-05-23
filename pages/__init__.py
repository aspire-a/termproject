import importlib
import pkgutil
from pathlib import Path

def register_all_blueprints(app):
    base = Path(__file__).parent

    # Recursively find every package under pages/
    for finder, module_name, is_pkg in pkgutil.walk_packages([str(base)], prefix=__name__ + "."):
        if not is_pkg:
            continue

        module = importlib.import_module(module_name)
        bp = getattr(module, "bp", None)
        if bp is not None:
            app.register_blueprint(bp)
