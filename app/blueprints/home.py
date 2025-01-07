from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Product, Company


home = Blueprint('home', __name__, url_prefix='/')

# Tienda Oficial
@home.route('/', methods=['GET'])
def market():
    company = Company.query.first()

    # Número de productos por página
    per_page = 12

    # Obtener el número de página desde la URL (por defecto será 1 si no se proporciona)
    page = request.args.get('page', 1, type=int)

    # Obtener el término de búsqueda desde la URL (si lo hay)
    search = request.args.get('search', '', type=str)

    # Consultar y filtrar productos por nombre (si se proporciona un término de búsqueda)
    query = Product.query.filter(Product.availability == True).order_by(Product.updated_at.desc())

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))  # Filtrado por nombre, insensible a mayúsculas

    # Realizar la paginación
    products = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'home/index.html',
        company=company,
        products=products,
        search=search
    )
