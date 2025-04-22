from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import Experience
from app import db
from .docs import experience_ns as ns

# Blueprint for route registration
# Added trailing slash
bp = Blueprint('experience', __name__, url_prefix='/api/experience/')

# Models for Swagger documentation
experience_model = ns.model('Experience', {
    'company': fields.String(required=True, description='Company name'),
    'position': fields.String(required=True, description='Job position'),
    'period': fields.String(required=True, description='Employment period'),
    'description': fields.String(required=True, description='Job description'),
    'technologies': fields.List(fields.String, description='Technologies used')
})


@ns.route('/')
class ExperienceList(Resource):
    @ns.doc('list_experiences')
    @ns.response(200, 'Success', [experience_model])
    def get(self):
        """List all experience entries"""
        experiences = Experience.query.all()
        return [{
            'company': exp.company,
            'position': exp.position,
            'period': exp.period,
            'description': exp.description,
            'technologies': exp.technologies
        } for exp in experiences]

    @ns.doc('create_experience', security='Bearer')
    @ns.expect(experience_model)
    @ns.response(201, 'Experience created')
    @ns.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new experience"""
        data = request.get_json()
        experience_data = {
            'company': data.get('company'),
            'position': data.get('position'),
            'period': data.get('period'),
            'description': data.get('description'),
            'technologies': data.get('technologies')
        }
        try:
            experience = Experience(**experience_data)
            db.session.add(experience)
            db.session.commit()
            return {'message': 'Experience created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('update_an_experience', security='Bearer')
    @ns.expect(experience_model)
    @ns.response(200, 'Experience updated')
    @ns.response(404, 'Experience not found')
    @jwt_required()
    def put(self, id):
        """Update an Experience"""
        experienc = Experience.query.filter_by(id=id).first_or_404()
        data = request.get_json()
        try:
            experienc.company = data.get('company', experienc.company)
            experienc.position = data.get('position', experienc.position)
            experienc.period = data.get('period', experienc.period)
            experienc.description = data.get(
                'description', experienc.description)
            experienc.technologies = data.get(
                'technologies', experienc.technologies)
            db.session.commit()
            return {'message': 'An Experience updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('delete_project', security='Bearer')
    @ns.response(200, 'Project deleted')
    @ns.response(404, 'Contact not found')
    @jwt_required()
    def delete(self, id):
        """Delete an Experience"""
        project = Experience.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(project)
            db.session.commit()
            return {'message': 'An Experience deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
