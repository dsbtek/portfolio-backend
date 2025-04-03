from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Project
from app import db

bp = Blueprint('projects', __name__, url_prefix='/api/projects')

@bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'title': project.title,
        'description': project.description,
        'technologies': project.technologies,
        'imageUrl': project.image_url,
        'githubUrl': project.github_url,
        'liveUrl': project.live_url,
        'slug': project.slug,
        'details': project.details
    } for project in projects])

@bp.route('/<slug>', methods=['GET'])
def get_project(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    return jsonify({
        'title': project.title,
        'description': project.description,
        'technologies': project.technologies,
        'imageUrl': project.image_url,
        'githubUrl': project.github_url,
        'liveUrl': project.live_url,
        'slug': project.slug,
        'details': project.details
    })