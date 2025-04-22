# Portfolio Backend

A Flask-based backend application for a portfolio website. Features include a blog system, project showcase, services, experience tracking, and contact form functionality.

## Tech Stack

-   Flask 2.0.1
-   SQLAlchemy 1.4.23
-   PostgreSQL
-   Flask-JWT-Extended 4.3.1
-   Flask-CORS 3.0.10

## Prerequisites

-   Python 3.10+
-   PostgreSQL
-   pip

## Installation & Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd portfolio-backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages with specific versions:

```bash
pip install flask==2.0.1 \
            werkzeug==2.0.3 \
            SQLAlchemy==1.4.23 \
            flask-sqlalchemy==2.5.1 \
            flask-cors==3.0.10 \
            flask-jwt-extended==4.3.1 \
            python-dotenv==0.19.0 \
            psycopg2-binary==2.9.1
```

4. Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

5. Initialize the database:

```bash
python create_tables.py
```

## Project Structure

```
portfolio-backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   ├── project.py
│   │   ├── service.py
│   │   ├── experience.py
│   │   └── contact.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   ├── projects.py
│   │   ├── services.py
│   │   ├── experience.py
│   │   └── contact.py
│   └── utils/
├── config.py
├── create_tables.py
├── requirements.txt
└── run.py
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

### Services

-   `GET /api/services` - Get all services
-   `GET /api/services/<slug>` - Get single service
-   `POST /api/services` - Create new service (protected)
-   `PUT /api/services/<slug>` - Update service (protected)
-   `DELETE /api/services/<slug>` - Delete service (protected)

### Experience

-   `GET /api/experience` - Get all experiences
-   `POST /api/experience` - Add new experience (protected)
-   `PUT /api/experience/<id>` - Update experience (protected)
-   `DELETE /api/experience/<id>` - Delete experience (protected)

### Contact

-   `POST /api/contact` - Submit contact form

## Authentication

Protected routes require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Development

Run the development server:

```bash
python3 run.py
```

The server will start at `http://localhost:5000`

## Deployment

### Backend (Railway/Heroku)

1. Create a new project on Railway or Heroku
2. Configure environment variables:
    - `DATABASE_URL`
    - `JWT_SECRET_KEY`
    - `CORS_ORIGINS`
3. Connect your GitHub repository
4. Deploy the backend

### Environment Variables

Required environment variables:

```env
# Database configuration
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio

# Security
JWT_SECRET_KEY=your-secret-key-here

# CORS configuration
CORS_ORIGINS=http://localhost:3000,https://your-production-frontend.com
```

## Common Issues & Troubleshooting

### Database Connection

-   Ensure PostgreSQL is running
-   Verify database credentials in `.env`
-   Check database exists: `createdb portfolio`

### Version Conflicts

If you encounter dependency conflicts, install these specific versions:

```bash
pip install werkzeug==2.0.3
pip install flask==2.0.1
pip install SQLAlchemy==1.4.23
pip install Flask-SQLAlchemy==2.5.1
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com
Project Link: [https://github.com/yourusername/portfolio-backend](https://github.com/yourusername/portfolio-backend)
