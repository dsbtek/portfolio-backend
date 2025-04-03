from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.ARRAY(db.String(100)), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    github_url = db.Column(db.String(500))
    live_url = db.Column(db.String(500))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    details = db.Column(db.Text, nullable=False)