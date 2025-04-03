from app import db
from datetime import datetime


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500))
    tags = db.Column(db.ARRAY(db.String(50)))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    reading_time = db.Column(db.Integer)
