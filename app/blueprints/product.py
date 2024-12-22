from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Product, Category, Brand
from app import db
import os
from werkzeug.utils import secure_filename


product = Blueprint('product', __name__)
UPLOAD_FOLDER = 'app/static/img/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#Formatos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Ver lista de Productos
@product.route('/products', methods=['GET'])
def show():
    # Número de productos por página
    per_page = 10

    # Obtener el número de página desde la URL (por defecto será 1 si no se proporciona)
    page = request.args.get('page', 1, type=int)

    # Obtener el término de búsqueda desde la URL (si lo hay)
    search = request.args.get('search', '', type=str)

    # Consultar y ordenar productos por fecha de actualización
    query = Product.query.order_by(Product.updated_at.desc())

    # Aplicar filtro de búsqueda si se proporciona
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    # Realizar la paginación
    products = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('product/show.html', products=products, search=search)


# Crear un producto nuevo
@product.route('/products/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name            = request.form['name']
        categories      = request.form.getlist('categories')
        picture         = request.files.get('picture')

        # Verificar si el nombre del producto ya existe
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product:
            flash('Ya existe un producto con ese nombre. Por favor, elige otro.', 'danger')
            return redirect(url_for('product.create'))

        # Guardar la imagen si existe y es válida
        picture_filename = None
        if picture and allowed_file(picture.filename):
            picture_filename = secure_filename(picture.filename)
            picture.save(os.path.join(UPLOAD_FOLDER, picture_filename))

        # Crear el nuevo producto
        new_product = Product(
            name        = name,
            description = request.form['description'],
            price       = float(request.form['sale_price']),
            availability= 'availability' in request.form,
            brand_id    = int(request.form['brand']),
            image       = picture_filename
        )
        
        # Asociar las categorías al producto
        for category_id in categories:
            category = Category.query.get(category_id)
            new_product.categories.append(category)

        # Agregar el nuevo producto a la base de datos
        db.session.add(new_product)
        db.session.commit()

        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('product.show'))

    # Obtener Productos y categorías para llenar los selectores
    brands = Brand.query.all()
    categories = Category.query.all()

    return render_template('product/create.html', brands=brands, categories=categories)



# Editar una Producto
# Editar un Producto
@product.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Product.query.get_or_404(id)  # Buscar el producto por su ID
    if request.method == 'POST':
        name = request.form['name']
        categories = request.form.getlist('categories')
        picture = request.files.get('picture')

        # Verificar si el nombre del producto ya existe y no es el mismo que el producto actual
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product and existing_product.id != product.id:
            flash('Ya existe un producto con ese nombre. Por favor, elige otro.', 'danger')
            return redirect(url_for('product.edit', id=product.id))

        # Actualizar los datos del producto
        product.name = name
        product.description = request.form['description']
        product.price = float(request.form['sale_price'])
        product.availability = 'availability' in request.form
        product.brand_id = int(request.form['brand'])

        # Si se sube una nueva imagen, guardar la nueva imagen
        if picture and allowed_file(picture.filename):
            # Eliminar la imagen anterior si existe
            if product.image:
                old_image_path = os.path.join(UPLOAD_FOLDER, product.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)  # Eliminar la imagen anterior

            picture_filename = secure_filename(picture.filename)
            picture.save(os.path.join(UPLOAD_FOLDER, picture_filename))
            product.image = picture_filename  # Actualizar la imagen del producto

        # Actualizar las categorías del producto
        product.categories.clear()  # Eliminar las categorías anteriores
        for category_id in categories:
            category = Category.query.get(category_id)
            product.categories.append(category)

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('product.show'))

    # Obtener marcas y categorías para llenar los selectores
    brands = Brand.query.all()
    categories = Category.query.all()

    return render_template('product/edit.html', product=product, brands=brands, categories=categories)



# Eliminar un Producto
@product.route('/products/delete/<int:id>', methods=['POST'])
def delete(id):
    # Obtener el producto por su ID
    product = Product.query.get_or_404(id)

    # Eliminar la imagen del producto si existe
    if product.image:
        image_path = os.path.join(UPLOAD_FOLDER, product.image)
        if os.path.exists(image_path):
            os.remove(image_path)  # Eliminar la imagen

    # Eliminar las asociaciones en la tabla intermedia 'product_categories' si es necesario
    for category in product.categories:
        product.categories.remove(category)

    # Eliminar el producto
    db.session.delete(product)
    db.session.commit()

    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('product.show'))

