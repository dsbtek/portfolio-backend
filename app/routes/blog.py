from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import BlogPost
from app import db
from datetime import datetime
from .docs import blog_ns as ns

# Blueprint for route registration
bp = Blueprint('blog', __name__, url_prefix='/api/blog')

# Models for Swagger documentation
blog_model = ns.model('Blog', {
    'title': fields.String(required=True, description='Blog post title'),
    'excerpt': fields.String(required=True, description='Blog post excerpt'),
    'content': fields.String(required=True, description='Blog post content'),
    'author': fields.String(description='Blog post author'),
    'imageUrl': fields.String(description='Blog post image URL'),
    'tags': fields.List(fields.String, description='Blog post tags'),
    'slug': fields.String(required=True, description='Blog post slug'),
    'readingTime': fields.Integer(description='Estimated reading time in minutes')
})


@ns.route('/')
class BlogList(Resource):
    @ns.doc('list_posts')
    @ns.response(200, 'Success', [blog_model])
    def get(self):
        """List all blog posts"""
        blogs = BlogPost.query.all()
        return [{
            'title': blog.title,
            'excerpt': blog.excerpt,
            'content': blog.content,
            'date': blog.date.isoformat() if blog.date else None,
            'author': blog.author,
            'imageUrl': blog.image_url,
            'tags': blog.tags,
            'slug': blog.slug,
            'readingTime': blog.reading_time
        } for blog in blogs]

    @ns.doc('create_blog', security='Bearer')
    @ns.expect(blog_model)
    @ns.response(201, 'Block created')
    @ns.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new blog"""
        data = request.get_json()

        blog_data = {
            'title': data.get('title'),
            'excerpt': data.get('excerpt'),
            'content': data.get('content'),
            'image_url': data.get('imageUrl'),
            'author': data.get('author'),
            'tags': data.get('tags'),
            'slug': data.get('slug'),
            'readingTime': data.reading_time

        }

        try:
            blog = BlogPost(**blog_data)
            db.session.add(blog)
            db.session.commit()
            return {'message': 'Blog created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


@ns.route('/<slug>')
@ns.param('slug', 'The blog slug')
class ProjectResource(Resource):
    @ns.doc('get_blog')
    @ns.response(200, 'Success', blog_model)
    @ns.response(404, 'Blog not found')
    def get(self, slug):
        """Get a blog by slug"""
        blog = BlogPost.query.filter_by(slug=slug).first_or_404()
        return {
            'title': blog.title,
            'excerpt': blog.excerpt,
            'content': blog.content,
            'imageUrl': blog.image_url,
            'tags': blog.tags,
            'author': blog.author,
            'slug': blog.slug,
            'date': blog.date.isoformat() if blog.date else None,
            'readingTime': blog.reading_time
        }
