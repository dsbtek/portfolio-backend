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
        posts = BlogPost.query.all()
        return [{
            'title': post.title,
            'excerpt': post.excerpt,
            'content': post.content,
            'date': post.date.isoformat() if post.date else None,
            'author': post.author,
            'imageUrl': post.image_url,
            'tags': post.tags,
            'slug': post.slug,
            'readingTime': post.reading_time
        } for post in posts]


@ns.route('/<slug>')
@ns.param('slug', 'The blog slug')
class ProjectResource(Resource):
    @ns.doc('get_project')
    @ns.response(200, 'Success', blog_model)
    @ns.response(404, 'Project not found')
    def get(self, slug):
        """Get a project by slug"""
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
