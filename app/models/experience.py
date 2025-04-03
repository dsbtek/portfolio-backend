from app import db


class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.ARRAY(db.String(50)))
