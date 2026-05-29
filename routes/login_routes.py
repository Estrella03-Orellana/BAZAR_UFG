from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.csv_service import get_usuarios, add_usuario
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
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('index'))
                    
        flash('Correo o contraseña incorrectos', 'error')
        return redirect(url_for('login_bp.login'))
        
    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@login_bp.route('/access-denied')
def access_denied():
    return render_template('access-denied.html')


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validate passwords match
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('login_bp.register'))
        
        # Check if email already exists
        usuarios = get_usuarios()
        for user in usuarios:
            if user['email'] == email:
                flash('El correo ya está registrado', 'error')
                return redirect(url_for('login_bp.register'))
        
        # Create new user
        nuevo_usuario = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'password': password,
            'rol': 'CLIENTE'
        }
        
        add_usuario(nuevo_usuario)
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('login_bp.login'))
    
    return render_template('register.html')