from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import BlogPost
from app import db

bp = Blueprint('blog', __name__, url_prefix='/api/blog')


@bp.route('/', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([{
        'title': post.title,
        'excerpt': post.excerpt,
        'content': post.content,
        'date': post.date.isoformat(),
        'author': post.author,
        'imageUrl': post.image_url,
        'tags': post.tags,
        'slug': post.slug,
        'readingTime': post.reading_time
    } for post in posts])


@bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()

    # Extract reading time value and convert to integer
    reading_time = data.get('readingTime')
    if isinstance(reading_time, str):
        # Extract number from string like "5 min"
        reading_time = int(reading_time.split()[0])

    # Map camelCase to snake_case
    blog_data = {
        'title': data.get('title'),
        'excerpt': data.get('excerpt'),
        'content': data.get('content'),
        'author': data.get('author'),
        'image_url': data.get('imageUrl'),
        'tags': data.get('tags'),
        'slug': data.get('slug'),
        'reading_time': reading_time  # Now it's an integer
    }

    # Remove None values
    blog_data = {k: v for k, v in blog_data.items() if v is not None}

    post = BlogPost(**blog_data)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201
