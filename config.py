import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    CORS_ORIGINS = os.getenv(
        'CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Add these configurations
    RESTX_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_ERROR_404_HELP = False
    SWAGGER_UI_JSONEDITOR = True  # Add this for better JSON editing in Swagger UI
