from app import db

class AboutMe(db.Model):
    __tablename__ = 'about_me'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.String(500))  # URL to profile image
    resume_url = db.Column(db.String(500))     # URL to resume/CV
    skills = db.Column(db.ARRAY(db.String(50)))
    interests = db.Column(db.ARRAY(db.String(100)))
    location = db.Column(db.String(200))