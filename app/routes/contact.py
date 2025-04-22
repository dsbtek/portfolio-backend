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

    @ns.doc('create_contact', security='Bearer')
    @ns.expect(contact_info_model)
    @ns.response(201, 'Contact created')
    @ns.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new contact"""
        data = request.get_json()

        contact_data = {
            'email': data.get('email'),
            'linkedin': data.get('linkedin'),
            'github': data.get('github'),
            'twitter': data.get('twitter')
        }

        try:
            contact = Contact(**contact_data)
            db.session.add(contact)
            db.session.commit()
            return {'message': 'Contact created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('update_contact', security='Bearer')
    @ns.expect(contact_info_model)
    @ns.response(200, 'Contact information updated')
    @ns.response(404, 'Contact not found')
    @jwt_required()
    def put(self, id):
        """Update a contact"""
        contact = Contact.query.filter_by(id=id).first_or_404()
        data = request.get_json()

        try:
            contact.email = data.get('email', contact.email)
            contact.linkedin = data.get('linkedin', contact.linkedin)
            contact.github = data.get('github', contact.github)
            contact.twitter = data.get('twitter', contact.twitter)

            db.session.commit()
            return {'message': 'Contact information updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('delete_contact', security='Bearer')
    @ns.response(200, 'Contact deleted')
    @ns.response(404, 'Contact not found')
    @jwt_required()
    def delete(self, id):
        """Delete a contact"""
        service = Contact.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(service)
            db.session.commit()
            return {'message': 'Contact deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
