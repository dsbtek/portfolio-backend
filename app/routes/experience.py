from flask import Blueprint, jsonify
from app.models import Experience

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