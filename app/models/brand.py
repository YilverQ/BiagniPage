from app import db
from datetime import datetime

class Brand(db.Model):
    __tablename__ = 'brands'

    id 			= db.Column(db.Integer, primary_key=True)
    name 		= db.Column(db.String(100), nullable=False, unique=True)
    picture 	= db.Column(db.String(255), nullable=True)
    created_at 	= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at 	= db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Brand id={self.id}, name={self.name}>'