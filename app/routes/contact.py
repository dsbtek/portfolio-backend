from flask import Blueprint, request, jsonify
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

contact_message_model = ns.model('ContactMessage', {
    'name': fields.String(required=True, description='Sender name'),
    'email': fields.String(required=True, description='Sender email'),
    'message': fields.String(required=True, description='Message content')
})


@ns.route('/')
class ContactResource(Resource):
    @ns.doc('get_contact_info')
    @ns.response(200, 'Contact information retrieved')
    def get(self):
        """Get contact information"""
        contact = Contact.query.first()
        if not contact:
            return {'error': 'No contact information found'}, 404

        return {
            'email': contact.email,
            'linkedin': contact.linkedin,
            'github': contact.github,
            'twitter': contact.twitter
        }, 200

    @ns.doc('update_contact_info', security='Bearer')
    @ns.expect(contact_info_model)
    @ns.response(200, 'Contact updated')
    @jwt_required()
    def post(self):
        """Update contact information"""
        data = request.get_json()

        # Validate required fields
        if 'email' not in data:
            return {'error': 'Email is required'}, 400

        contact = Contact.query.first()

        try:
            if contact:
                contact.email = data['email']
                contact.linkedin = data.get('linkedin', contact.linkedin)
                contact.github = data.get('github', contact.github)
                contact.twitter = data.get('twitter', contact.twitter)
                contact.msg = contact.msg  # Preserve existing msg value
            else:
                contact = Contact(
                    email=data['email'],
                    linkedin=data.get('linkedin'),
                    github=data.get('github'),
                    twitter=data.get('twitter'),
                    msg=''  # Provide a default value
                )
                db.session.add(contact)

            db.session.commit()
            return {'message': 'Contact information updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


@ns.route('/message/')
class ContactMessageResource(Resource):
    @ns.doc('submit_contact_message')
    @ns.expect(contact_message_model)
    @ns.response(201, 'Message sent')
    def post(self):
        """Submit a contact form message"""
        data = request.get_json()

        if not all(key in data for key in ['name', 'email', 'message']):
            return {'error': 'Missing required fields'}, 400

        try:
            # Here you would typically save the message or send an email
            # For now, we'll just return success
            return {'message': 'Message sent successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 400
