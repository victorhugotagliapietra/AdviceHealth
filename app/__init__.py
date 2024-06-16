from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import client_routes, vehicle_routes
    app.register_blueprint(client_routes.bp)
    app.register_blueprint(vehicle_routes.bp)

    return app
