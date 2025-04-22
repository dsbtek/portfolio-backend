from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import Project
from app import db
from .docs import projects_ns as ns

# Blueprint for route registration
bp = Blueprint('projects', __name__, url_prefix='/api/projects')

# Models for Swagger documentation
project_model = ns.model('Project', {
    'title': fields.String(required=True, description='Project title'),
    'description': fields.String(required=True, description='Project description'),
    'technologies': fields.List(fields.String, description='Technologies used'),
    'imageUrl': fields.String(description='Project image URL'),
    'githubUrl': fields.String(description='GitHub repository URL'),
    'liveUrl': fields.String(description='Live demo URL'),
    'slug': fields.String(required=True, description='URL-friendly identifier'),
    'details': fields.String(description='Detailed project information')
})


@ns.route('/')
class ProjectList(Resource):
    @ns.doc('list_projects')
    @ns.response(200, 'Success', [project_model])
    def get(self):
        """List all projects"""
        projects = Project.query.all()
        return [{
            'title': project.title,
            'description': project.description,
            'technologies': project.technologies,
            'imageUrl': project.image_url,
            'githubUrl': project.github_url,
            'liveUrl': project.live_url,
            'slug': project.slug,
            'details': project.details
        } for project in projects]

    @ns.doc('create_project', security='Bearer')
    @ns.expect(project_model)
    @ns.response(201, 'Project created')
    @ns.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new project"""
        data = request.get_json()

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

        try:
            project = Project(**project_data)
            db.session.add(project)
            db.session.commit()
            return {'message': 'Project created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('update_project', security='Bearer')
    @ns.expect(project_model)
    @ns.response(200, 'Project updated')
    @ns.response(404, 'Project not found')
    @jwt_required()
    def put(self, id):
        """Update a Project"""
        project = Project.query.filter_by(id=id).first_or_404()
        data = request.get_json()

        try:
            project.title = data.get('title', project.title)
            project.description = data.get('description', project.description)
            project.technologies = data.get(
                'technologies', project.technologies)
            project.image_url = data.get('image_url', project.image_url)
            project.github_url = data.get('github_url', project.github_url)
            project.live_url = data.get('live_url', project.live_url)
            project.slug = data.get('slug', project.slug)
            project.details = data.get('details', project.details)

            db.session.commit()
            return {'message': 'Project updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('delete_project', security='Bearer')
    @ns.response(200, 'Project deleted')
    @ns.response(404, 'Contact not found')
    @jwt_required()
    def delete(self, id):
        """Delete a Project"""
        project = Project.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(project)
            db.session.commit()
            return {'message': 'Project deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


@ns.route('/<slug>')
@ns.param('slug', 'The project slug')
class ProjectResource(Resource):
    @ns.doc('get_project')
    @ns.response(200, 'Success', project_model)
    @ns.response(404, 'Project not found')
    def get(self, slug):
        """Get a project by slug"""
        project = Project.query.filter_by(slug=slug).first_or_404()
        return {
            'title': project.title,
            'description': project.description,
            'technologies': project.technologies,
            'imageUrl': project.image_url,
            'githubUrl': project.github_url,
            'liveUrl': project.live_url,
            'slug': project.slug,
            'details': project.details
        }
