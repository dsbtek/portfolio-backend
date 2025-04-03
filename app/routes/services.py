from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Service
from app import db

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


@bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    data = request.get_json()
    service_data = {
        'title': data.get('title'),
        'description': data.get('description'),
        'icon': data.get('icon'),
        'capabilities': data.get('capabilities'),
        'slug': data.get('slug')
    }
    service_data = {k: v for k, v in service_data.items() if v is not None}

    service = Service(**service_data)
    db.session.add(service)
    db.session.commit()

    return jsonify({'message': 'Service created successfully'}), 201
