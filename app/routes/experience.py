from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import Experience
from app import db
from .docs import experience_ns as ns

# Blueprint for route registration
bp = Blueprint('experience', __name__, url_prefix='/api/experience')

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
