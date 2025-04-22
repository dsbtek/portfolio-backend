import pytest
from app import db
from app.models import Project

@pytest.fixture
def sample_project(app):
    with app.app_context():
        project = Project(
            title='Test Project',
            description='Test description',
            technologies=['Python', 'Flask'],
            slug='test-project'
        )
        db.session.add(project)
        db.session.commit()
        return project

def test_get_all_projects(client, sample_project):
    response = client.get('/api/projects')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['title'] == 'Test Project'

def test_get_single_project(client, sample_project):
    response = client.get(f'/api/projects/{sample_project.slug}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Project'

def test_create_project(client, auth_headers):
    response = client.post('/api/projects', 
        headers=auth_headers,
        json={
            'title': 'New Project',
            'description': 'New description',
            'technologies': ['React', 'Node.js'],
            'slug': 'new-project'
        }
    )
    assert response.status_code == 201