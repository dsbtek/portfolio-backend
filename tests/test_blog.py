import pytest
from app import db
from app.models import BlogPost


@pytest.fixture
def sample_blog_post(app):
    with app.app_context():
        post = BlogPost(
            title='Test Post',
            excerpt='Test excerpt',
            content='Test content',
            author='Test Author',
            slug='test-post',
            reading_time=5
        )
        db.session.add(post)
        db.session.commit()

        # Verify the post exists
        saved_post = BlogPost.query.filter_by(slug='test-post').first()
        assert saved_post is not None

        return post.slug


def test_get_all_posts(client, sample_blog_post):
    response = client.get('/api/blog/')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['title'] == 'Test Post'


def test_get_single_post(client, sample_blog_post):
    slug = sample_blog_post
    response = client.get(f'/api/blog/{slug}')  # Removed trailing slash
    assert response.status_code == 200
    assert response.json['title'] == 'Test Post'


def test_create_post(client, auth_headers):
    response = client.post('/api/blog/',
                           headers=auth_headers,
                           json={
                               'title': 'New Post',
                               'excerpt': 'New excerpt',
                               'content': 'New content',
                               'author': 'Test Author',
                               'slug': 'new-post',
                               'readingTime': 3
                           }
                           )
    assert response.status_code == 201
