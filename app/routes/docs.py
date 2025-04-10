from flask_restx import Api
from flask import Blueprint

# Create Blueprint
bp = Blueprint('swagger_api', __name__)

# Initialize Api with Blueprint
api = Api(bp,
          version='1.0',
          title='Portfolio API',
          description='API documentation for Portfolio Backend',
          doc='/api/docs',
          prefix='/api',
          authorizations={
              'Bearer': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization',
                  'description': 'Enter your Bearer token in the format: **Bearer &lt;JWT&gt;**',
                  'scheme': 'bearer',
                  'bearerFormat': 'JWT'
              }
          },
          security={'Bearer': []},  # This makes Bearer auth global
          ordered=True)

# Create namespaces
auth_ns = api.namespace('auth', description='Authentication operations')
projects_ns = api.namespace('projects', description='Project operations')
services_ns = api.namespace('services', description='Service operations')
experience_ns = api.namespace(
    'experience', description='Experience operations')
blog_ns = api.namespace('blog', description='Blog operations')
contact_ns = api.namespace('contact', description='Contact operations')
about_ns = api.namespace('about', description='About me operations')


def register_namespaces():
    """Register all API namespaces"""
    # Import views to register routes
    from . import auth
    from . import projects
    from . import services
    from . import experience
    from . import blog
    from . import contact
