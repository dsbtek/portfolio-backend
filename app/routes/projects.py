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


@bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()

    # Map camelCase to snake_case
    project_data = {
        'title': data.get('title'),
        'description': data.get('description'),
        'technologies': data.get('technologies'),
        'image_url': data.get('imageUrl'),
        'github_url': data.get('githubUrl'),
        'live_url': data.get('liveUrl'),
        'slug': data.get('slug'),
        'details': data.get('details')
    }

    # Remove None values
    project_data = {k: v for k, v in project_data.items() if v is not None}

    project = Project(**project_data)
    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 201


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
