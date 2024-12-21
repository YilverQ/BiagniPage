from app import create_app

# Crear instancia de la aplicación
app = create_app()

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
