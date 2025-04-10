from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import Contact
from app import db
from .docs import contact_ns as ns

# Blueprint for route registration
bp = Blueprint('contact', __name__, url_prefix='/api/contact')

# Models for Swagger documentation
contact_info_model = ns.model('ContactInfo', {
    'email': fields.String(required=True, description='Contact email'),
    'linkedin': fields.String(description='LinkedIn profile URL'),
    'github': fields.String(description='GitHub profile URL'),
    'twitter': fields.String(description='Twitter profile URL')
})


@ns.route('/')
class ContactResource(Resource):
    @ns.doc('get_contact_info')
    @ns.response(200, 'Success', contact_info_model)
    @ns.response(404, 'Contact info not found')
    def get(self):
        """Get contact information"""
        contact = Contact.query.first()
        if not contact:
            return {'message': 'No contact information available'}, 404
        return {
            'email': contact.email,
            'linkedin': contact.linkedin,
            'github': contact.github,
            'twitter': contact.twitter
        }
