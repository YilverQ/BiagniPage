from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Brand, Product
from app import db
import os
from werkzeug.utils import secure_filename

brand = Blueprint('brand', __name__)
UPLOAD_FOLDER = 'app/static/img/brands'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#Formatos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Ver lista de Marcas
@brand.route('/brands', methods=['GET'])
def show():
    # Número de marcas por página
    per_page = 10

    # Obtener el número de página desde la URL (por defecto será 1 si no se proporciona)
    page = request.args.get('page', 1, type=int)

    # Obtener el término de búsqueda desde la URL (si lo hay)
    search = request.args.get('search', '', type=str)

    # Consultar y filtrar marcas por nombre (si se proporciona un término de búsqueda)
    query = Brand.query.order_by(Brand.name.asc())

    if search:
        query = query.filter(Brand.name.ilike(f'%{search}%'))  # Filtrado por nombre, insensible a mayúsculas

    # Realizar la paginación
    brands = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('brand/show.html', brands=brands, search=search)


#Crear una Marca
@brand.route('/brands/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        picture = request.files.get('picture')

        # Verificar si el nombre de la marca ya existe
        existing_brand = Brand.query.filter_by(name=name).first()
        if existing_brand:
            flash('Ya existe una marca con ese nombre. Por favor, elige otro.', 'danger')
            return redirect(url_for('brand.create'))

        # Si hay una imagen, guardarla
        if picture and allowed_file(picture.filename):
            filename = secure_filename(picture.filename)
            picture.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = None
        
        # Crear la nueva marca
        new_brand = Brand(name=name, picture=filename)
        db.session.add(new_brand)
        db.session.commit()
        flash('Marca agregada exitosamente', 'success')
        return redirect(url_for('brand.show'))
    
    return render_template('brand/create.html')



# Editar una Marca
@brand.route('/brands/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    brand = Brand.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']

        # Verificar si el nombre de la marca ya existe y no es la misma marca que estamos editando
        existing_brand = Brand.query.filter_by(name=name).first()
        if existing_brand and existing_brand.id != brand.id:
            flash('Ya existe una marca con ese nombre. Por favor, elige otro.', 'danger')
            return redirect(url_for('brand.edit', id=brand.id))

        # Si se proporciona una nueva imagen, eliminar la antigua y guardar la nueva
        picture = request.files.get('picture')
        if picture and allowed_file(picture.filename):
            if brand.picture:
                old_image_path = os.path.join(UPLOAD_FOLDER, brand.picture)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)  # Eliminar la imagen antigua

            filename = secure_filename(picture.filename)
            picture.save(os.path.join(UPLOAD_FOLDER, filename))
            brand.picture = filename  # Actualizar el campo de imagen

        # Actualizar el nombre de la marca
        brand.name = name

        db.session.commit()
        flash('Marca actualizada exitosamente', 'success')
        return redirect(url_for('brand.show'))

    return render_template('brand/edit.html', brand=brand)


# Eliminar una Marca
@brand.route('/brands/delete/<int:id>', methods=['POST'])
def delete(id):
    brand = Brand.query.get_or_404(id)
    
    # Eliminar la imagen de la marca del servidor
    if brand.picture:
        image_path = os.path.join(UPLOAD_FOLDER, brand.picture)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # Eliminar los productos asociados a la marca
    products = Product.query.filter_by(brand_id=brand.id).all()
    for product in products:
        db.session.delete(product)
    
    # Eliminar la marca
    db.session.delete(brand)
    db.session.commit()
    
    flash('Marca y productos eliminados exitosamente', 'success')
    return redirect(url_for('brand.show'))
