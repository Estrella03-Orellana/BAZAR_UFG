from flask import Blueprint, render_template, request, redirect, url_for
from routes.login_routes import role_required
import os
from werkzeug.utils import secure_filename

from services.csv_service import (
    get_categorias,
    add_categoria,
    update_categoria,
    delete_categoria
)

categoria_bp = Blueprint('categoria_bp', __name__)


# LISTAR
@categoria_bp.route('/categorias')
@role_required(['ADMINISTRADOR'])
def listar_categorias():

    categorias = get_categorias()

    return render_template(
        'admin/categorias.html',
        categorias=categorias
    )


# CREAR
@categoria_bp.route('/categorias/crear', methods=['GET', 'POST'])
@role_required(['ADMINISTRADOR'])
def crear_categoria():

    if request.method == 'POST':

        nombre = request.form['nombre']

        imagen = request.files['imagen']

        nombre_imagen = secure_filename(imagen.filename)

        ruta_imagen = os.path.join(
            'static',
            'img',
            nombre_imagen
        )

        imagen.save(ruta_imagen)

        nueva_categoria = {
            "nombre": nombre,
            "imagen": nombre_imagen
        }

        add_categoria(nueva_categoria)

        return redirect(
            url_for('categoria_bp.listar_categorias')
        )

    return render_template('admin/crear_categoria.html')


# EDITAR
@categoria_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@role_required(['ADMINISTRADOR'])
def editar_categoria(id):

    categorias = get_categorias()

    categoria = next(
        (c for c in categorias if int(c['id']) == id),
        None
    )

    if request.method == 'POST':

        nombre_imagen = categoria['imagen']

        imagen = request.files['imagen']

        if imagen and imagen.filename != "":

            nombre_imagen = secure_filename(
                imagen.filename
            )

            ruta_imagen = os.path.join(
                'static',
                'img',
                nombre_imagen
            )

            imagen.save(ruta_imagen)

        categoria_actualizada = {
            "id": id,
            "nombre": request.form['nombre'],
            "imagen": nombre_imagen
        }

        update_categoria(categoria_actualizada)

        return redirect(
            url_for('categoria_bp.listar_categorias')
        )

    return render_template(
        'admin/editar_categoria.html',
        categoria=categoria
    )

# ELIMINAR
@categoria_bp.route('/categorias/eliminar/<int:id>')
@role_required(['ADMINISTRADOR'])
def eliminar_categoria(id):

    delete_categoria(id)

    return redirect(
        url_for('categoria_bp.listar_categorias')
    )