from flask import Blueprint, jsonify, request
from app.models import Contact
from app import db

bp = Blueprint('contact', __name__, url_prefix='/api/contact')


@bp.route('/', methods=['GET'])
def get_contact():
    contact = Contact.query.first()
    if not contact:
        return jsonify({}), 404
    return jsonify({
        'email': contact.email,
        'linkedin': contact.linkedin,
        'github': contact.github,
        'twitter': contact.twitter
    })


@bp.route('/', methods=['POST'])
def submit_contact():
    data = request.get_json()
    contact_data = {
        'name': data.get('name'),
        'email': data.get('email'),
        'message': data.get('message')
    }

    # Process contact form submission here
    # Add your email sending logic

    return jsonify({'message': 'Message sent successfully'}), 201
