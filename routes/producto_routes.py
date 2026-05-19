from flask import Blueprint, render_template
from services.csv_service import get_productos

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/productos')
def listar_productos():
    productos = get_productos()
    return render_template('productos.html', productos=productos)