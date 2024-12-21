from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializa las extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    # Inicializa la base de datos y migraciones
    db.init_app(app)
    migrate.init_app(app, db)


    # Importa tus modelos
    from app.models import Company


    # Función para cargar la compañía antes de cada solicitud
    @app.before_request
    def load_company():
        g.company = Company.query.first()


    # Registrar blueprints usando la función del módulo blueprints
    from .blueprints import register_blueprints
    register_blueprints(app)


    return app