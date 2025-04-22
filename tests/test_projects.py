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
            slug='test-project',
            image_url='http://example.com/image.jpg',
            github_url='http://github.com/example',
            live_url='http://example.com',
            details='Test project details'
        )
        db.session.add(project)
        db.session.commit()

        # Get a fresh instance from the database
        project = Project.query.filter_by(slug='test-project').first()
        return project


def test_get_all_projects(client, sample_project):
    response = client.get('/api/projects/')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['title'] == 'Test Project'


def test_get_single_project(client, sample_project):
    # Ensure we're using the same app context as the fixture
    with client.application.app_context():
        # Verify the project exists in the database
        project = Project.query.filter_by(slug='test-project').first()
        assert project is not None  # Add this check to verify project exists

        # Remove trailing slash to match route definition
        response = client.get(f'/api/projects/{project.slug}')
        assert response.status_code == 200
        assert response.json['title'] == 'Test Project'
        assert response.json['description'] == 'Test description'


def test_create_project(client, auth_headers):
    response = client.post('/api/projects/',
                           headers=auth_headers,
                           json={
                               'title': 'New Project',
                               'description': 'New description',
                               'technologies': ['React', 'Node.js'],
                               'slug': 'new-project',
                               'imageUrl': 'http://example.com/new-image.jpg',
                               'githubUrl': 'http://github.com/new-project',
                               'liveUrl': 'http://example.com/new-project',
                               'details': 'New project detailed information'
                           }
                           )
    assert response.status_code == 201
