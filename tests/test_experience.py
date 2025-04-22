import pytest
from app import db
from app.models import Experience


@pytest.fixture
def sample_experience(app):
    with app.app_context():
        exp = Experience(
            company='Test Company',
            position='Test Position',
            period='2020-2021',
            description='Test description',
            technologies=['Python', 'Flask']
        )
        db.session.add(exp)
        db.session.commit()
        return exp


def test_get_all_experience(client, sample_experience):
    response = client.get('/api/experience/')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['company'] == 'Test Company'


def test_create_experience(client, auth_headers):
    response = client.post('/api/experience/',
                           headers=auth_headers,
                           json={
                               'company': 'New Company',
                               'position': 'Senior Developer',
                               'period': '2021-Present',
                               'description': 'New role description',
                               'technologies': ['React', 'Node.js']
                           }
                           )
    assert response.status_code == 201
