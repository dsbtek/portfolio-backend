from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Experience
from app import db

bp = Blueprint('experience', __name__, url_prefix='/api/experience')


@bp.route('/', methods=['GET'])
def get_experience():
    experiences = Experience.query.all()
    return jsonify([{
        'company': exp.company,
        'position': exp.position,
        'period': exp.period,
        'description': exp.description,
        'technologies': exp.technologies
    } for exp in experiences])


@bp.route('/', methods=['POST'])
@jwt_required()
def create_experience():
    data = request.get_json()
    experience_data = {
        'company': data.get('company'),
        'position': data.get('position'),
        'period': data.get('period'),
        'description': data.get('description'),
        'technologies': data.get('technologies')
    }
    experience_data = {k: v for k,
                       v in experience_data.items() if v is not None}

    experience = Experience(**experience_data)
    db.session.add(experience)
    db.session.commit()

    return jsonify({'message': 'Experience created successfully'}), 201
