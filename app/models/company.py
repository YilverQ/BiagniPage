from app import db
from datetime import datetime


class Company(db.Model):
    __tablename__ = 'companies'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(100), nullable=False, unique=True)
    wallpaper       = db.Column(db.String(255), nullable=True)
    picture_profile = db.Column(db.String(255), nullable=True)
    description     = db.Column(db.Text, nullable=True)
    facebook_link   = db.Column(db.String(255), nullable=True)
    instagram_link  = db.Column(db.String(255), nullable=True)
    whatsapp_link   = db.Column(db.String(255), nullable=True)
    other_link      = db.Column(db.String(255), nullable=True)
    created_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Company id={self.id}, name={self.name}>'