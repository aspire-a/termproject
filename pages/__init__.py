import importlib, pkgutil, pathlib

def register_all_blueprints(app):
    base = pathlib.Path(__file__).parent
    for mod in pkgutil.iter_modules([str(base)]):
        if not mod.ispkg:
            continue
        module = importlib.import_module(f"{__name__}.{mod.name}")
        bp = getattr(module, "bp", None)
        if bp is not None:
            app.register_blueprint(bp)
