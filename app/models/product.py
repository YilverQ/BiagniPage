from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(100), nullable=False, unique=True)
    description     = db.Column(db.Text, nullable=True)
    price           = db.Column(db.Float, nullable=False) # Precio de Venta
    availability    = db.Column(db.Boolean, nullable=False, default=True)
    image           = db.Column(db.String(255), nullable=True)
    created_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    brand_id        = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    brand           = db.relationship('Brand', backref=db.backref('products', lazy=True))
    categories      = db.relationship('Category', secondary='product_categories', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product id={self.id}, name={self.name}, sale_price={self.sale_price}>'
