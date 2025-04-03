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

@bp.route('/<slug>', methods=['GET'])
def get_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return jsonify({
        'title': post.title,
        'excerpt': post.excerpt,
        'content': post.content,
        'date': post.date.isoformat(),
        'author': post.author,
        'imageUrl': post.image_url,
        'tags': post.tags,
        'slug': post.slug,
        'readingTime': post.reading_time
    })

@bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    post = BlogPost(**data)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201