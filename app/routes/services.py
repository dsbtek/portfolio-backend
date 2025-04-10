from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import Service
from app import db
from .docs import services_ns as ns

# Blueprint for route registration
bp = Blueprint('services', __name__, url_prefix='/api/services')

# Models for Swagger documentation
service_model = ns.model('Service', {
    'title': fields.String(required=True, description='Service title'),
    'description': fields.String(required=True, description='Service description'),
    'icon': fields.String(description='Service icon name/class'),
    'capabilities': fields.List(fields.String, description='List of service capabilities'),
    'slug': fields.String(required=True, description='URL-friendly identifier')
})


@ns.route('/')
class ServiceList(Resource):
    @ns.doc('list_services')
    @ns.response(200, 'Success', [service_model])
    def get(self):
        """List all services"""
        services = Service.query.all()
        return [{
            'title': service.title,
            'description': service.description,
            'icon': service.icon,
            'capabilities': service.capabilities,
            'slug': service.slug
        } for service in services]

    @ns.doc('create_service', security='Bearer')
    @ns.expect(service_model)
    @ns.response(201, 'Service created')
    @ns.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new service"""
        data = request.get_json()

        service_data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'icon': data.get('icon'),
            'capabilities': data.get('capabilities'),
            'slug': data.get('slug')
        }

        try:
            service = Service(**service_data)
            db.session.add(service)
            db.session.commit()
            return {'message': 'Service created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


@ns.route('/<slug>')
@ns.param('slug', 'The service slug')
class ServiceResource(Resource):
    @ns.doc('get_service')
    @ns.response(200, 'Success', service_model)
    @ns.response(404, 'Service not found')
    def get(self, slug):
        """Get a service by slug"""
        service = Service.query.filter_by(slug=slug).first_or_404()
        return {
            'title': service.title,
            'description': service.description,
            'icon': service.icon,
            'capabilities': service.capabilities,
            'slug': service.slug
        }

    @ns.doc('update_service', security='Bearer')
    @ns.expect(service_model)
    @ns.response(200, 'Service updated')
    @ns.response(404, 'Service not found')
    @jwt_required()
    def put(self, slug):
        """Update a service"""
        service = Service.query.filter_by(slug=slug).first_or_404()
        data = request.get_json()

        try:
            service.title = data.get('title', service.title)
            service.description = data.get('description', service.description)
            service.icon = data.get('icon', service.icon)
            service.capabilities = data.get(
                'capabilities', service.capabilities)
            service.slug = data.get('slug', service.slug)

            db.session.commit()
            return {'message': 'Service updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('delete_service', security='Bearer')
    @ns.response(200, 'Service deleted')
    @ns.response(404, 'Service not found')
    @jwt_required()
    def delete(self, slug):
        """Delete a service"""
        service = Service.query.filter_by(slug=slug).first_or_404()
        try:
            db.session.delete(service)
            db.session.commit()
            return {'message': 'Service deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
