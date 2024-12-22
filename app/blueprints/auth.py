from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Company
from app import db
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

admin_user = {
    'username': 'tienda',
    'password': '#tienda#'
}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    company = Company.query.first()
    if not company:
        create_company()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica si el usuario y la contraseña son correctos
        if username == admin_user['username'] and password == admin_user['password']:
            flash('Bienvenida al Dashboard', 'success')
            # Aquí se debería autenticar al usuario con Flask-Login
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales Incorrectas', 'danger')
    
    return render_template('auth/login.html')


def create_company():
    # Diccionario con los datos de la compañía
    company_data = {
        'name': 'Mi Empresa',
        'wallpaper': 'app/static/img/defaul-wallpaper.png',
        'picture_profile': 'app/static/img/default-profile.jpg',
        'description': 'Descripción de mi empresa.',
        'facebook_link': '#',
        'instagram_link': '#',
        'whatsapp_link': '#',
        'other_link': '#',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }

    # Crear una nueva instancia de Company con los datos del diccionario
    new_company = Company(**company_data)

    # Agregar la compañía a la base de datos
    db.session.add(new_company)
    db.session.commit()

    flash('Compañía creada exitosamente', 'success')