from app import db


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    capabilities = db.Column(db.ARRAY(db.String(200)))
    slug = db.Column(db.String(100), unique=True, nullable=False)
