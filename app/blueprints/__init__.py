from flask import Blueprint

# Importar los blueprints
from .auth import auth
from .admin import admin
from .category import category
from .brand import brand
from .product import product
from .home import home

# Crear una función para registrar los blueprints en la aplicación
def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(category)
    app.register_blueprint(brand)
    app.register_blueprint(product)
    app.register_blueprint(home)
