from flask import Blueprint, jsonify
from app.models import Service

bp = Blueprint('services', __name__, url_prefix='/api/services')

@bp.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'title': service.title,
        'description': service.description,
        'icon': service.icon,
        'capabilities': service.capabilities,
        'slug': service.slug
    } for service in services])