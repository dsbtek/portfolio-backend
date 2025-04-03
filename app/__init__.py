from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes import blog, projects, services, experience, contact
    app.register_blueprint(blog.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(experience.bp)
    app.register_blueprint(contact.bp)

    return app