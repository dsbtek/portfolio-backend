import pytest
from app import db
from app.models import AboutMe


@pytest.fixture
def sample_about(app):
    with app.app_context():
        about = AboutMe(
            name='John Doe',
            title='Software Developer',
            description='Test description',
            skills=['Python', 'JavaScript'],
            location='New York'
        )
        db.session.add(about)
        db.session.commit()
        return about


def test_get_about(client, sample_about):
    response = client.get('/api/about/')  # Added trailing slash
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'
    assert response.json['title'] == 'Software Developer'


def test_update_about(client, auth_headers):
    response = client.post('/api/about/',  # Added trailing slash
                           headers=auth_headers,
                           json={
                               'name': 'Jane Doe',
                               'title': 'Full Stack Developer',
                               'description': 'Updated description',
                               'skills': ['Python', 'React'],
                               'location': 'San Francisco'
                           }
                           )
    assert response.status_code in [200, 201]
