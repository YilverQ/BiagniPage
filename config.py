import os
import secrets

class Config:
    # Configuración básica
    SECRET_KEY = secrets.token_hex(16)

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'postgresql://biagni:1234root@biagni.mysql.pythonanywhere-services.com/products_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False