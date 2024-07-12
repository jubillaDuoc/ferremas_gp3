# Importar módulos
from flask import Flask
from modules.system.logconf import init_logging
from paths.routes import register_routes
from flask_cors import CORS

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)

    # Configurar CORS para permitir solicitudes desde http://172.26.203.78:3000
    CORS(app, resources={r"/*": {"origins": "http://172.26.203.78:3000"}})

    # Inicializar la configuración de logging
    init_logging(app)

    # Importacion modulos de la aplicacion
    from modules.system.errors.handlers import register_error_handlers

    # Registrar los manejadores de errores
    register_error_handlers(app)

    # Registrar las rutas
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')