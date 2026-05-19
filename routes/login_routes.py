from flask import Blueprint, render_template, request, redirect, url_for
from services.csv_service import get_usuarios

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí iría tu lógica simplificada de validación
        username = request.form.get('username')
        password = request.form.get('password')
        usuarios = get_usuarios()
        
        for user in usuarios:
            if user['username'] == username and user['password'] == password:
                return redirect(url_for('home_bp.index'))
                
        return "Usuario o contraseña incorrectos", 401
        
    return render_template('login.html') # Asumiendo que crearás esta vista