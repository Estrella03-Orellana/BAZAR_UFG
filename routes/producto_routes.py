from flask import Blueprint, render_template, request, redirect, url_for

from services.csv_service import (
    get_productos,
    get_categorias,
    add_producto,
    update_producto,
    delete_producto
)

producto_bp = Blueprint('producto_bp', __name__)


# LISTAR
@producto_bp.route('/productos')
def listar_productos():

    productos = get_productos()

    categorias = get_categorias()

    return render_template(
        'admin/productos.html',
        productos=productos,
        categorias=categorias
    )


# CREAR
@producto_bp.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():

    categorias = get_categorias()

    if request.method == 'POST':

        nuevo_producto = {
            "nombre": request.form['nombre'],
            "precio": float(request.form['precio']),
            "categoria_id": int(request.form['categoria_id'])
        }

        add_producto(nuevo_producto)

        return redirect(
            url_for('producto_bp.listar_productos')
        )

    return render_template(
        'admin/crear_producto.html',
        categorias=categorias
    )


# EDITAR
@producto_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    productos = get_productos()

    categorias = get_categorias()

    producto = next(
        (p for p in productos if int(p['id']) == id),
        None
    )

    if request.method == 'POST':

        producto_actualizado = {
            "id": id,
            "nombre": request.form['nombre'],
            "precio": float(request.form['precio']),
            "categoria_id": int(request.form['categoria_id'])
        }

        update_producto(producto_actualizado)

        return redirect(
            url_for('producto_bp.listar_productos')
        )

    return render_template(
        'admin/editar_producto.html',
        producto=producto,
        categorias=categorias
    )


# ELIMINAR
@producto_bp.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):

    delete_producto(id)

    return redirect(
        url_for('producto_bp.listar_productos')
    )