from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import client_routes, vehicle_routes, auth_routes
    app.register_blueprint(client_routes.bp)
    app.register_blueprint(vehicle_routes.bp)
    app.register_blueprint(auth_routes.bp)

    return app
