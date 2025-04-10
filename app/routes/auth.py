from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.models import User
from app import db
from .docs import auth_ns as ns

# Blueprint for route registration
bp = Blueprint('auth', __name__)

# Models for Swagger documentation
login_model = ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

register_model = ns.model('Register', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

user_model = ns.model('User', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'email': fields.String(description='Email address')
})

auth_response = ns.model('AuthResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Nested(user_model, description='User information')
})

error_model = ns.model('Error', {
    'error': fields.String(description='Error message')
})


@ns.route('/login')
class Login(Resource):
    @ns.doc('user_login',
            description='Authenticate user and return access token')
    @ns.expect(login_model)
    @ns.response(200, 'Success', auth_response)
    @ns.response(400, 'Missing fields', error_model)
    @ns.response(401, 'Invalid credentials', error_model)
    def post(self):
        """Login user and return access token"""
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ['username', 'password']):
            return {'error': 'Missing required fields'}, 400

        # Authenticate user
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }

        return {'error': 'Invalid username or password'}, 401


@ns.route('/register')
class Register(Resource):
    @ns.doc('user_registration',
            description='Register new user account')
    @ns.expect(register_model)
    @ns.response(201, 'User created successfully')
    @ns.response(400, 'Validation error', error_model)
    def post(self):
        """Register a new user"""
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ['username', 'email', 'password']):
            return {'error': 'Missing required fields'}, 400

        # Check if username exists
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 400

        # Check if email exists
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already exists'}, 400

        try:
            # Create new user
            user = User(
                username=data['username'],
                email=data['email']
            )
            user.set_password(data['password'])

            # Save to database
            db.session.add(user)
            db.session.commit()

            return {'message': 'User created successfully'}, 201

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400


@ns.route('/check-username/<string:username>')
@ns.param('username', 'Username to check')
class UsernameCheck(Resource):
    @ns.doc('check_username',
            description='Check if username is available')
    @ns.response(200, 'Username available')
    @ns.response(409, 'Username taken', error_model)
    def get(self, username):
        """Check if username is available"""
        if User.query.filter_by(username=username).first():
            return {'error': 'Username is already taken'}, 409
        return {'message': 'Username is available'}, 200


@ns.route('/check-email/<string:email>')
@ns.param('email', 'Email to check')
class EmailCheck(Resource):
    @ns.doc('check_email',
            description='Check if email is available')
    @ns.response(200, 'Email available')
    @ns.response(409, 'Email taken', error_model)
    def get(self, email):
        """Check if email is available"""
        if User.query.filter_by(email=email).first():
            return {'error': 'Email is already registered'}, 409
        return {'message': 'Email is available'}, 200


@ns.route('/me')
class UserProfile(Resource):
    @ns.doc('get_user_profile', security='Bearer')
    @ns.response(200, 'Success', user_model)
    @ns.response(401, 'Unauthorized', error_model)
    @jwt_required()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
