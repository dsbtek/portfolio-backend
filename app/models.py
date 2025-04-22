from app import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(500), nullable=True)  # Make it nullable
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    twitter = db.Column(db.String(200))

    def __repr__(self):
        return f'<Contact {self.email}>'
