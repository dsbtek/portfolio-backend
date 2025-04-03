# portfolio-backend

A built  Flask app for the portfolio backend. Features include a blog system, project showcase, and contact form functionality.

## Tech Stack
-   Flask
-   SQLAlchemy
-   PostgreSQL
-   Flask-JWT-Extended
-   Flask-Cors


1. Create a new directory for the backend:

```bash
mkdir backend
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install flask flask-sqlalchemy flask-cors flask-jwt-extended python-dotenv psycopg2-binary
```

4. Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio
JWT_SECRET_KEY=your-secret-key
```

5. Create the following directory structure:

```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   └── utils/
├── config.py
├── requirements.txt
└── run.py
```

6. Basic Flask setup (`run.py`):

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

7. Initialize Flask app (`app/__init__.py`):

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from app.routes import blog, projects, contact
    app.register_blueprint(blog.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(contact.bp)

    return app
```

8. Configuration (`config.py`):

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
```

9. Run the backend server:

```bash
python run.py
```

## Project Structure

```
portfolio/
├──             # Flask backend
    ├── app/
    │   ├── models/      # Database models
    │   ├── routes/      # API endpoints
    │   └── utils/       # Helper functions
    └── config.py        # Backend configuration
```

## API Endpoints

### Blog

-   `GET /api/blog` - Get all blog posts
-   `GET /api/blog/<slug>` - Get single blog post
-   `POST /api/blog` - Create new blog post (protected)
-   `PUT /api/blog/<slug>` - Update blog post (protected)
-   `DELETE /api/blog/<slug>` - Delete blog post (protected)

### Projects

-   `GET /api/projects` - Get all projects
-   `GET /api/projects/<slug>` - Get single project
-   `POST /api/projects` - Create new project (protected)
-   `PUT /api/projects/<slug>` - Update project (protected)
-   `DELETE /api/projects/<slug>` - Delete project (protected)

### Contact

-   `POST /api/contact` - Submit contact form

## Deployment

### Frontend (Vercel)

The easiest way to deploy the Next.js frontend is to use the [Vercel Platform](https://vercel.com/new).

1. Push your code to GitHub
2. Import your repository to Vercel
3. Configure environment variables
4. Deploy

### Backend (Railway/Heroku)

1. Create a new project on Railway or Heroku
2. Configure environment variables
3. Connect your GitHub repository
4. Deploy the backend

## Environment Variables

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Backend (.env)

```env
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio
JWT_SECRET_KEY=your-secret-key
CORS_ORIGIN=http://localhost:3000
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
