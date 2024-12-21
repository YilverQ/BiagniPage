from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Category
from app import db

category = Blueprint('category', __name__)

#Ver lista de Categorías
@category.route('/categories', methods=['GET'])
def show():
    # Número de categorías por página
    per_page = 10

    # Obtener el número de página desde la URL (por defecto será 1 si no se proporciona)
    page = request.args.get('page', 1, type=int)

    # Obtener el término de búsqueda desde la URL (si lo hay)
    search = request.args.get('search', '', type=str)

    # Consultar y filtrar categorías por nombre (si se proporciona un término de búsqueda)
    query = Category.query.order_by(Category.name.asc())

    if search:
        query = query.filter(Category.name.ilike(f'%{search}%'))  # Filtrado por nombre, insensible a mayúsculas

    # Realizar la paginación
    categories = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('category/show.html', categories=categories, search=search)





#Crear una nueva Categoría
@category.route('/categories/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']

        # Verificar si el nombre de la marca ya existe
        item_exists = Category.query.filter_by(name=name).first()
        if item_exists:
            flash('Ya existe un elemento con ese nombre. Por favor, elige otro.', 'danger')
            return redirect(url_for('category.create'))


        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Categoría agregada exitosamente', 'success')
        return redirect(url_for('category.show'))
    
    return render_template('category/create.html')


#Editar Categoría
@category.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']

        # Verificar si el nombre de la categoría ya existe y no es la misma categoría que estamos editando
        item_exists = Category.query.filter_by(name=name).first()
        if item_exists and item_exists.id != category.id:
            flash('Ya existe un elemento con ese nombre. Por favor, elige otro.', 'danger')
            return redirect(url_for('category.edit', id=category.id))

        # Actualizar el nombre de la categoría
        category.name = name
        db.session.commit()
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('category.show'))

    return render_template('category/edit.html', category=category)


#Eliminar Categoría
@category.route('/categories/delete/<int:id>', methods=['POST'])
def delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('category.show'))