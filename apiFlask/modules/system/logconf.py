import logging
from logging.handlers import RotatingFileHandler
import json

def init_logging(app):
    # Leer el archivo config.json para la configuración del logger
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        log_path = config['path_logs']
        log_level = config['log_level']
    
    # Configurar el nivel de log y el formato globalmente
    logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=log_path)

    # Configurar el logger de la aplicación con RotatingFileHandler
    handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=1)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Añadir el handler al logger de la aplicación Flask
    app.logger.addHandler(handler)
    app.logger.setLevel(getattr(logging, log_level))

    # Configurar el logger de Werkzeug para usar el mismo handler
    logging.getLogger('werkzeug').name = 'internal_logs'
    logging.getLogger('werkzeug').handlers = []
    logging.getLogger('werkzeug').addHandler(handler)
    logging.getLogger('werkzeug').propagate = False
