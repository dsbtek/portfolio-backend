from app import create_app

# Rename 'app' to 'application' for Gunicorn
application = create_app()

# Keep 'app' for local development compatibility
app = application

if __name__ == '__main__':
    app.run()
