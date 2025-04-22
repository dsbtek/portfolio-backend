import pytest
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, BlogPost, Project, Service, Experience, Contact, AboutMe

# Load test environment variables
load_dotenv('.env.test')


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL')
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app, client):
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()

    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_contact(app):
    with app.app_context():
        contact = Contact(
            email='test@example.com',
            linkedin='https://linkedin.com/in/test',
            github='https://github.com/test',
            twitter='https://twitter.com/test',
            msg=''  # Add default empty message
        )
        db.session.add(contact)
        db.session.commit()
        return contact
