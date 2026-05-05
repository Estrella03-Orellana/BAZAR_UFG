from flask import Flask, render_template, redirect, session
import csv
import os

app = Flask(__name__)
app.secret_key = "clave"

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def cargar_productos():
    productos = []
    ruta = os.path.join(BASE_DIR, 'data', 'productos.csv')

    with open(ruta, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            productos.append({
                "id": int(fila["id"]),
                "nombre": fila["nombre"],
                "precio": float(fila["precio"]),
                "categoria_id": int(fila["categoria_id"])
            })
    return productos


def cargar_categorias():
    categorias = []
    ruta = os.path.join(BASE_DIR, 'data', 'categorias.csv')

    with open(ruta, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            categorias.append({
                "id": int(fila["id"]),
                "nombre": fila["nombre"]
            })
    return categorias


productos = cargar_productos()
categorias = cargar_categorias()



@app.route('/')
def index():
    return render_template('cliente/index.html', productos=productos)



@app.route('/agregar/<int:id>')
def agregar(id):
    if 'carrito' not in session:
        session['carrito'] = []

    session['carrito'].append(id)
    session.modified = True
    return redirect('/')



@app.route('/carrito')
def carrito():
    carrito_ids = session.get('carrito', [])
    
    carrito_productos = []
    total = 0

    for p in productos:
        if p["id"] in carrito_ids:
            carrito_productos.append(p)
            total += p["precio"]

    return render_template('cliente/carrito.html', carrito=carrito_productos, total=total)



@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'carrito' in session and id in session['carrito']:
        session['carrito'].remove(id)
        session.modified = True

    return redirect('/carrito')


if __name__ == '__main__':
    app.run(debug=True, port=5001)