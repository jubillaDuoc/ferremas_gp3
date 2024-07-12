from flask import jsonify, redirect
import logging

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 Not Found: {error}")  # Registrar el error 404
        return redirect('/web/')

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        logger.warning(f"405 Method Not Allowed: {error}")  # Registrar el error 405
        return jsonify({'error': 'Método no permitido'}), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {error}", exc_info=True)  # Registrar el error 500, incluyendo el stack trace
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        logger.warning(f"401 Unauthorized: {error}")  # Registrar el error 401
        return jsonify({'error': 'No autorizado'}), 401
