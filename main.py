import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.controllers import api


def create_app() -> Flask:
    # Initializing the Flask application
    app = Flask(__name__)

    # Application configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['MYSQL_DATABASE_URI']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Database initialization
    db = SQLAlchemy()
    db.init_app(app)

    # API blueprint recording
    app.register_blueprint(api)
    return app


if __name__ == "__main__":
    app = create_app()

    # Launch the Flask application
    app.run(
        debug=True,
        host=os.environ['APP_HOST'],
        port=int(os.environ['APP_PORT'])
    )
