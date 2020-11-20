import os

from flask import Flask


def create_app(config=None):
    """ Flask app factory that creates and configure the app.
    Args:
        test_config (str): python configuration filepath
    Returns: Flask application
    """
    app = Flask(__name__)

    if config:
        app.config.update(config)

    # instance dir
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # blueprints
    from src.application.blueprints import home
    app.register_blueprint(home.bp)

    return app
