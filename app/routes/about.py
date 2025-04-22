from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from app.models import AboutMe
from app import db
from .docs import about_ns as ns

# Blueprint for route registration
bp = Blueprint('about', __name__, url_prefix='/api/about')

# Models for Swagger documentation
about_model = ns.model('AboutMe', {
    'name': fields.String(required=True, description='Full name'),
    'title': fields.String(required=True, description='Professional title'),
    'description': fields.String(required=True, description='About me description'),
    'profile_image': fields.String(description='URL to profile image'),
    'resume_url': fields.String(description='URL to resume/CV'),
    'skills': fields.List(fields.String, description='List of skills'),
    'interests': fields.List(fields.String, description='List of interests/hobbies'),
    'location': fields.String(description='Current location')
})


@ns.route('/')
class AboutMeResource(Resource):
    @ns.doc('get_about_me')
    @ns.response(200, 'Success', about_model)
    @ns.response(404, 'Information not found')
    def get(self):
        """Get about me information"""
        about = AboutMe.query.first()
        if not about:
            return {'message': 'No information available'}, 404

        return {
            'name': about.name,
            'title': about.title,
            'description': about.description,
            'profile_image': about.profile_image,
            'resume_url': about.resume_url,
            'skills': about.skills,
            'interests': about.interests,
            'location': about.location
        }

    @ns.doc('update_about_me', security='Bearer')
    @ns.expect(about_model)
    @ns.response(200, 'Information updated')
    @ns.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Update about me information"""
        data = request.get_json()
        about = AboutMe.query.first()

        if about:
            # Update existing record
            try:
                about.name = data.get('name', about.name)
                about.title = data.get('title', about.title)
                about.description = data.get('description', about.description)
                about.profile_image = data.get(
                    'profile_image', about.profile_image)
                about.resume_url = data.get('resume_url', about.resume_url)
                about.skills = data.get('skills', about.skills)
                about.interests = data.get('interests', about.interests)
                about.location = data.get('location', about.location)

                db.session.commit()
                return {'message': 'Information updated successfully'}
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400
        else:
            # Create new record
            try:
                about = AboutMe(
                    name=data.get('name'),
                    title=data.get('title'),
                    description=data.get('description'),
                    profile_image=data.get('profile_image'),
                    resume_url=data.get('resume_url'),
                    skills=data.get('skills', []),
                    interests=data.get('interests', []),
                    location=data.get('location')
                )
                db.session.add(about)
                db.session.commit()
                return {'message': 'Information created successfully'}, 201
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 400

    @ns.doc('update_about_me', security='Bearer')
    @ns.expect(about_model)
    @ns.response(200, 'Service updated')
    @ns.response(404, 'Service not found')
    @jwt_required()
    def put(self, slug):
        """Update a about me"""
        about_me = AboutMe.query.filter_by(slug=slug).first_or_404()
        data = request.get_json()

        try:
            about_me.title = data.get('title', about_me.title)
            about_me.description = data.get(
                'description', about_me.description)
            about_me.icon = data.get('icon', about_me.icon)
            about_me.capabilities = data.get(
                'capabilities', about_me.capabilities)
            about_me.slug = data.get('slug', about_me.slug)

            db.session.commit()
            return {'message': 'About Me updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @ns.doc('delete_about_me', security='Bearer')
    @ns.response(200, 'About Me deleted')
    @ns.response(404, 'About Me not found')
    @jwt_required()
    def delete(self, slug):
        """Delete a about me"""
        about_me = AboutMe.query.filter_by(slug=slug).first_or_404()
        try:
            db.session.delete(about_me)
            db.session.commit()
            return {'message': 'About Me deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
