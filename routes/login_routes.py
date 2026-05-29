from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.csv_service import get_usuarios
from functools import wraps

login_bp = Blueprint('login_bp', __name__)

def role_required(roles_permitidos):
    """
    Si el usuario no está logueado, va a /login.
    Si el usuario no tiene el rol permitido, va a una página de acceso denegado.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if 'usuario_id' not in session:
                return redirect(url_for('login_bp.login'))
            
            user_role = session.get('usuario_rol')
            if user_role not in roles_permitidos:
                return redirect(url_for('login_bp.access_denied'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuarios = get_usuarios()
        
        for user in usuarios:
            if user['email'] == email and user['password'] == password:
  
                session['usuario_id'] = user['id']
                session['usuario_nombre'] = user['nombre']
                session['usuario_rol'] = user['rol']
                
                if user['rol'] == 'ADMINISTRADOR':
                    return redirect(url_for('categoria_bp.listar_categorias'))
                else:
                    return redirect(url_for('home_bp.index'))
                    
        flash('Correo o contraseña incorrectos', 'error')
        return redirect(url_for('login_bp.login'))
        
    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.index'))


@login_bp.route('/access-denied')
def access_denied():
    return render_template('access-denied.html')