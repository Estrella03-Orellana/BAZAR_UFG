from flask import Flask, render_template, redirect, session, request, flash
import csv
import os

from routes.categoria_routes import categoria_bp
from routes.producto_routes import producto_bp
from routes.login_routes import login_bp, role_required

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(categoria_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(login_bp)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def cargar_productos():
    productos = []
    ruta = os.path.join(BASE_DIR, 'data', 'productos.csv')
    if not os.path.exists(ruta):
        return productos
    with open(ruta, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            productos.append({
                "id": int(fila["id"]),
                "nombre": fila["nombre"],
                "precio": float(fila["precio"]),
                "categoria_id": int(fila["categoria_id"]),
                "imagen": fila.get("imagen", "")
            })
    return productos


def cargar_categorias():
    categorias = []
    ruta = os.path.join(BASE_DIR, 'data', 'categorias.csv')
    if not os.path.exists(ruta):
        return categorias
    with open(ruta, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            categorias.append({
                "id": int(fila["id"]),
                "nombre": fila["nombre"],
                "imagen": fila.get("imagen", "")
            })
    return categorias


# ── CLIENTE ──────────────────────────────

@app.route('/')
def index():
    categorias = cargar_categorias()
    return render_template('cliente/index.html', categorias=categorias)


@app.route('/catalogo')
def catalogo():
    productos = cargar_productos()
    categorias = cargar_categorias()
    cat_id = request.args.get('cat', type=int)
    q = request.args.get('q', '').strip()

    filtrados = productos
    if cat_id:
        filtrados = [p for p in filtrados if p['categoria_id'] == cat_id]
    if q:
        filtrados = [p for p in filtrados if q.lower() in p['nombre'].lower()]

    return render_template(
        'cliente/catalogo.html',
        productos=filtrados,
        categorias=categorias,
        cat_activa=cat_id,
        busqueda=q
    )


@app.route('/producto/<int:id>')
def detalle_producto(id):
    productos = cargar_productos()
    categorias = cargar_categorias()
    producto = next((p for p in productos if p['id'] == id), None)
    if not producto:
        return redirect('/catalogo')
    categoria = next((c for c in categorias if c['id'] == producto['categoria_id']), None)
    return render_template(
        'cliente/producto.html',
        producto=producto,
        categoria=categoria,
        categorias=categorias
    )


@app.route('/agregar/<int:id>')
@role_required(['CLIENTE'])
def agregar(id):
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(id)
    session.modified = True
    flash('added')
    ref = request.referrer
    return redirect(ref if ref else '/catalogo')


@app.route('/carrito')
@role_required(['CLIENTE'])
def carrito():
    carrito_ids = session.get('carrito', [])
    productos_cargados = cargar_productos()
    carrito_productos = []
    total = 0
    for p in productos_cargados:
        if p["id"] in carrito_ids:
            carrito_productos.append(p)
            total += p["precio"]
    return render_template(
        'cliente/carrito.html',
        carrito=carrito_productos,
        total=total
    )


@app.route('/eliminar/<int:id>')
@role_required(['CLIENTE'])
def eliminar(id):
    if 'carrito' in session and id in session['carrito']:
        session['carrito'].remove(id)
        session.modified = True
    flash('removed')
    return redirect('/carrito')


@app.route('/historial')
@role_required(['CLIENTE'])
def historial():
    return render_template('cliente/historial.html')


@app.route('/admin/dashboard')
@role_required(['ADMINISTRADOR'])
def admin_dashboard():
    return render_template('admin/dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)