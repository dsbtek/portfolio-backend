# API Documentation

Base URL: `http://localhost:5000` (Development) or `https://your-api-url.com` (Production)

## Authentication

Protected endpoints require JWT authentication via Bearer token in the Authorization header. The token must be prefixed with "Bearer":

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Example curl command:

```bash
curl -X GET \
  'http://localhost:5000/api/projects' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

#### Register New User

```http
POST /api/auth/register
```

Request Body:

```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

Response (201 Created):

```json
{
    "message": "User created successfully"
}
```

#### Login

```http
POST /api/auth/login
```

Request Body:

```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

Response (200 OK):

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

#### Get Current User Profile

```http
GET /api/auth/me
```

Headers:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response (200 OK):

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
}
```

## Response Formats

### Success Response

```json
{
    "data": {}, // Requested data
    "message": "Operation successful" // Optional success message
}
```

### Error Response

```json
{
    "error": "Error message",
    "status": 400 // HTTP status code
}
```

## Endpoints

### Blog Posts

#### Get All Blog Posts

```http
GET /api/blog
```

Response:

```json
[
    {
        "title": "Sample Blog Post",
        "excerpt": "Short preview of the post",
        "content": "Full blog post content",
        "date": "2023-08-15T10:30:00",
        "author": "John Doe",
        "imageUrl": "https://example.com/image.jpg",
        "tags": ["tech", "programming"],
        "slug": "sample-blog-post",
        "readingTime": "5 min"
    }
]
```

#### Get Single Blog Post

```http
GET /api/blog/<slug>
```

Response:

```json
{
    "title": "Sample Blog Post",
    "excerpt": "Short preview of the post",
    "content": "Full blog post content",
    "date": "2023-08-15T10:30:00",
    "author": "John Doe",
    "imageUrl": "https://example.com/image.jpg",
    "tags": ["tech", "programming"],
    "slug": "sample-blog-post",
    "readingTime": "5 min"
}
```

#### Create Blog Post (Protected)

```http
POST /api/blog
```

Request Body:

```json
{
    "title": "New Blog Post",
    "excerpt": "Short preview",
    "content": "Full content",
    "author": "John Doe",
    "imageUrl": "https://example.com/image.jpg",
    "tags": ["tech", "programming"],
    "slug": "new-blog-post"
}
```

### Projects

#### Get All Projects

```http
GET /api/projects
```

Response:

```json
[
    {
        "title": "Project Name",
        "description": "Project description",
        "technologies": ["React", "Python", "PostgreSQL"],
        "imageUrl": "https://example.com/project.jpg",
        "githubUrl": "https://github.com/username/project",
        "liveUrl": "https://project-demo.com",
        "slug": "project-name",
        "details": "Detailed project information"
    }
]
```

#### Get Single Project

```http
GET /api/projects/<slug>
```

Response:

```json
{
    "title": "Project Name",
    "description": "Project description",
    "technologies": ["React", "Python", "PostgreSQL"],
    "imageUrl": "https://example.com/project.jpg",
    "githubUrl": "https://github.com/username/project",
    "liveUrl": "https://project-demo.com",
    "slug": "project-name",
    "details": "Detailed project information"
}
```

#### Create Project (Protected)

```http
POST /api/projects
```

Request Body:

```json
{
    "title": "New Project",
    "description": "Project description",
    "technologies": ["React", "Python", "PostgreSQL"],
    "imageUrl": "https://example.com/project.jpg",
    "githubUrl": "https://github.com/username/project",
    "liveUrl": "https://project-demo.com",
    "slug": "new-project",
    "details": "Detailed project information"
}
```

### Services

#### Get All Services

```http
GET /api/services
```

Response:

```json
[
    {
        "title": "Service Name",
        "description": "Service description",
        "icon": "service-icon",
        "capabilities": ["Feature 1", "Feature 2"],
        "slug": "service-name"
    }
]
```

#### Get Single Service

```http
GET /api/services/<slug>
```

Response:

```json
{
    "title": "Service Name",
    "description": "Service description",
    "icon": "service-icon",
    "capabilities": ["Feature 1", "Feature 2"],
    "slug": "service-name"
}
```

### Experience

#### Get All Experiences

```http
GET /api/experience
```

Response:

```json
[
    {
        "company": "Company Name",
        "position": "Job Title",
        "period": "Jan 2020 - Present",
        "description": "Job description",
        "technologies": ["React", "Python", "AWS"]
    }
]
```

#### Create Experience (Protected)

```http
POST /api/experience
```

Request Body:

```json
{
    "company": "Company Name",
    "position": "Job Title",
    "period": "Jan 2020 - Present",
    "description": "Job description",
    "technologies": ["React", "Python", "AWS"]
}
```

### Contact

#### Get Contact Information

```http
GET /api/contact
```

Response:

```json
{
    "email": "contact@example.com",
    "linkedin": "https://linkedin.com/in/username",
    "github": "https://github.com/username",
    "twitter": "https://twitter.com/username"
}
```

#### Update Contact Information (Protected)

```http
POST /api/contact
```

Headers:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

Request Body:

```json
{
    "email": "contact@example.com",
    "linkedin": "https://linkedin.com/in/username",
    "github": "https://github.com/username",
    "twitter": "https://twitter.com/username"
}
```

Response (201 Created):

```json
{
    "message": "Contact information updated successfully"
}
```

#### Submit Contact Form Message

```http
POST /api/contact/message
```

Request Body:

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, I'd like to discuss a project."
}
```

Response (201 Created):

```json
{
    "message": "Message sent successfully"
}
```

## Error Codes

| Status Code | Description           |
| ----------- | --------------------- |
| 200         | Success               |
| 201         | Created               |
| 400         | Bad Request           |
| 401         | Unauthorized          |
| 403         | Forbidden             |
| 404         | Not Found             |
| 500         | Internal Server Error |

## Rate Limiting

-   API requests are limited to 100 requests per minute per IP address
-   Protected endpoints are limited to 50 requests per minute per token

## Data Models

### Blog Post

-   `title` (string, required): Post title
-   `excerpt` (string, required): Short preview
-   `content` (string, required): Full post content
-   `date` (datetime): Publication date
-   `author` (string, required): Author name
-   `imageUrl` (string): Featured image URL
-   `tags` (array): List of tags
-   `slug` (string, required): URL-friendly identifier
-   `readingTime` (string): Estimated reading time

### Project

-   `title` (string, required): Project name
-   `description` (string, required): Short description
-   `technologies` (array, required): List of technologies used
-   `imageUrl` (string, required): Project screenshot
-   `githubUrl` (string): GitHub repository URL
-   `liveUrl` (string): Live demo URL
-   `slug` (string, required): URL-friendly identifier
-   `details` (string, required): Detailed description

### Service

-   `title` (string, required): Service name
-   `description` (string, required): Service description
-   `icon` (string, required): Service icon identifier
-   `capabilities` (array, required): List of features/capabilities
-   `slug` (string, required): URL-friendly identifier

### Experience

-   `company` (string, required): Company name
-   `position` (string, required): Job title
-   `period` (string, required): Employment period
-   `description` (string, required): Job description
-   `technologies` (array, required): Technologies used

## Testing

Example curl commands for testing:

```bash
# Login and get token
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"securepassword123"}' \
  http://localhost:5000/api/auth/login

# Use token in protected endpoint
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"contact@example.com"}' \
  http://localhost:5000/api/contact

# Submit contact form
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","message":"Hello"}' \
  http://localhost:5000/api/contact/message
```
