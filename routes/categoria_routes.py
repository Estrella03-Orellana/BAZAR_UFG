from flask import Blueprint, render_template
from services.csv_service import get_categorias

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias')
def listar_categorias():
    categorias = get_categorias()
    return render_template('categorias.html', categorias=categorias)