from flask import Blueprint, render_template, request, redirect, url_for

from services.csv_service import (
    get_categorias,
    add_categoria,
    update_categoria,
    delete_categoria
)

categoria_bp = Blueprint('categoria_bp', __name__)


# LISTAR
@categoria_bp.route('/categorias')
def listar_categorias():

    categorias = get_categorias()

    return render_template(
        'admin/categorias.html',
        categorias=categorias
    )


# CREAR
@categoria_bp.route('/categorias/crear', methods=['GET', 'POST'])
def crear_categoria():

    if request.method == 'POST':

        nombre = request.form['nombre']

        nueva_categoria = {
            "nombre": nombre
        }

        add_categoria(nueva_categoria)

        return redirect(
            url_for('categoria_bp.listar_categorias')
        )

    return render_template('admin/crear_categoria.html')


# EDITAR
@categoria_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):

    categorias = get_categorias()

    categoria = next(
        (c for c in categorias if int(c['id']) == id),
        None
    )

    if request.method == 'POST':

        categoria_actualizada = {
            "id": id,
            "nombre": request.form['nombre']
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
def eliminar_categoria(id):

    delete_categoria(id)

    return redirect(
        url_for('categoria_bp.listar_categorias')
    )