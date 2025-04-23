from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Add database initialization route
    @app.route('/init-db', methods=['POST'])
    def init_db():
        try:
            db.create_all()
            return {"message": "Database tables created successfully!"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    # Register blueprints
    from app.routes import docs, auth, projects, blog, services, contact, experience, about
    app.register_blueprint(docs.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(experience.bp)
    app.register_blueprint(about.bp)

    # Register all API namespaces
    docs.register_namespaces()

    return app
