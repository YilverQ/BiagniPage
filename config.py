import os
import secrets

class Config:
    # Configuración básica
    SECRET_KEY = secrets.token_hex(16)

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:root@localhost/biagni'
    SQLALCHEMY_TRACK_MODIFICATIONS = False