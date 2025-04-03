from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    # Specify migrations directory
    migrate.init_app(app, db, directory='migrations')
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Register blueprints
    from app.routes import blog, projects, services, experience, contact, auth
    app.register_blueprint(blog.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(experience.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(auth.bp)

    return app
