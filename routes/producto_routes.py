from flask import Blueprint, render_template, request, redirect, url_for
from routes.login_routes import role_required

import os
from werkzeug.utils import secure_filename

from services.csv_service import (
    get_productos,
    get_categorias,
    add_producto,
    update_producto,
    delete_producto
)

producto_bp = Blueprint('producto_bp', __name__)

UPLOAD_FOLDER = 'static/img'


# LISTAR
@producto_bp.route('/productos')
@role_required(['ADMINISTRADOR'])
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
@role_required(['ADMINISTRADOR'])
def crear_producto():

    categorias = get_categorias()

    if request.method == 'POST':

        imagen = request.files['imagen']

        nombre_imagen = ''

        if imagen and imagen.filename:
            nombre_imagen = secure_filename(imagen.filename)
            imagen.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    nombre_imagen
                )
            )

        nuevo_producto = {
            "nombre": request.form['nombre'],
            "precio": float(request.form['precio']),
            "categoria_id": int(request.form['categoria_id']),
            "imagen": nombre_imagen
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
@role_required(['ADMINISTRADOR'])
def editar_producto(id):

    productos = get_productos()
    categorias = get_categorias()

    producto = next(
        (p for p in productos if int(p['id']) == id),
        None
    )

    if request.method == 'POST':

        nombre_imagen = producto['imagen']

        imagen = request.files.get('imagen')

        if imagen and imagen.filename:

            nombre_imagen = secure_filename(
                imagen.filename
            )

            imagen.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    nombre_imagen
                )
            )

        producto_actualizado = {
            "id": id,
            "nombre": request.form['nombre'],
            "precio": float(request.form['precio']),
            "categoria_id": int(request.form['categoria_id']),
            "imagen": nombre_imagen
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
@role_required(['ADMINISTRADOR'])
def eliminar_producto(id):

    delete_producto(id)

    return redirect(
        url_for('producto_bp.listar_productos')
    )