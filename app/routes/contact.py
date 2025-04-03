from flask import Blueprint, jsonify
from app.models import Contact

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