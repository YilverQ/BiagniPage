from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
import os
from app.models import Product, Brand, Category, Company
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename


admin = Blueprint('admin', __name__, url_prefix='/admin')
UPLOAD_FOLDER = 'app/static/img/profile/'

# Función para validar los tipos de archivo
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.route('/dashboard')
def dashboard():
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    new_products_last_month = Product.query.filter(Product.created_at > one_month_ago).count()

    # Consultas para obtener las estadísticas
    total_products = Product.query.count()  # Número total de productos
    total_brands = Brand.query.count()  # Número total de marcas
    total_categories = Category.query.count()  # Número total de categorías
    average_product_price = db.session.query(db.func.avg(Product.price)).scalar()  # Promedio de precios de productos
    available_products = Product.query.filter_by(availability=True).count()  # Productos disponibles
    unavailable_products = Product.query.filter_by(availability=False).count()  # Productos no disponibles

    # Última fecha de actualización (puede ser la más reciente entre los productos)
    last_updated_product = Product.query.order_by(Product.updated_at.desc()).first()

    # Obtener las fechas y conteos de productos por fecha
    product_dates = db.session.query(db.func.date(Product.created_at).label('date'), db.func.count().label('count'))\
                              .group_by(db.func.date(Product.created_at))\
                              .order_by(db.func.date(Product.created_at)).all()

    # Preparar los datos para el gráfico
    dates = [date[0].strftime('%Y-%m-%d') for date in product_dates]
    counts = [count[1] for count in product_dates]

    
    return render_template(
        'admin/dashboard.html',
        total_products=total_products,
        total_brands=total_brands,
        total_categories=total_categories,
        average_product_price=average_product_price,
        available_products=available_products,
        unavailable_products=unavailable_products,
        last_updated_product=last_updated_product,
        new_products_last_month=new_products_last_month,
        dates=dates,
        counts=counts
    )



@admin.route('/config', methods=['GET', 'POST'])
def config():
    company = Company.query.first()

    if request.method == 'POST':
        # Actualizar la información básica
        company.name = request.form['name']
        company.description = request.form['description']
        company.facebook_link = request.form['facebook_link']
        company.instagram_link = request.form['instagram_link']
        company.whatsapp_link = request.form['whatsapp_link']
        company.other_link = request.form['other_link']

        # Manejar la actualización de imágenes
        if 'wallpaper' in request.files:
            wallpaper = request.files['wallpaper']
            if wallpaper and allowed_file(wallpaper.filename):
                filename = secure_filename(wallpaper.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                wallpaper.save(filepath)
                company.wallpaper = filename

        if 'picture_profile' in request.files:
            picture_profile = request.files['picture_profile']
            if picture_profile and allowed_file(picture_profile.filename):
                filename = secure_filename(picture_profile.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                picture_profile.save(filepath)
                company.picture_profile = filename

        # Guardar los cambios en la base de datos
        db.session.commit()
        flash('Configuración actualizada correctamente', 'success')
        return redirect(url_for('admin.config'))

    return render_template('admin/config.html', company=company)


#Vemos un preview de como queda la tienda
@admin.route('/preview')
def preview():
    company = Company.query.first()

    # Obtener los primeros 10 productos más recientes
    products = Product.query.order_by(Product.updated_at.desc()).limit(12).all()

    return render_template(
        'admin/preview.html',
        company=company,
        products=products
    )