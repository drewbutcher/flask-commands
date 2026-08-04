import time

from config import config
from flask import Flask

def create_app(config_name) -> Flask:
    """Creates a Flask application Instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(config[config_name])

    # Expose global values to every Jinja template.
    @app.context_processor
    def inject_globals():
        return {
            "time": time,
        }

    from app.routes.mains import bp as mains_blueprint
    app.register_blueprint(mains_blueprint)

    return app
