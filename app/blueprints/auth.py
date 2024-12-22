from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__)

admin_user = {
    'username': 'tienda',
    'password': '#tienda#'
}

@auth.route('/login', methods=['GET', 'POST'])
def login():
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