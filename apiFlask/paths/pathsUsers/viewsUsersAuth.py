# Desc: Módulo para manejar la autenticación de usuarios
# Developer: Vachir00
# # Importar módulos
from flask import Blueprint, request, jsonify
import logging
# # Importacion de modulos internos
from modules.system.api_decorators import user_auth_required, user_auth_refresh, admin_auth_required, admin_auth_refresh
from modules.auth.moduleUserAuth import user_login_tokenrole
from modules.system.errors.handlers import register_error_handlers

# # Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

# # Crear un Blueprint para manejar las rutas de este módulo
user_login_blueprint = Blueprint('user_login', __name__)
register_error_handlers(user_login_blueprint)

# # Definir la ruta para autenticar un usuario
@user_login_blueprint.route('/user_login', methods=['POST'])
def user_login():
    """
    Procesa la solicitud para autenticar un usuario.

    Returns:
        Si la autenticación es exitosa, devuelve un objeto JSON con un mensaje de éxito y un token de autenticación.
        Si la autenticación falla, devuelve un objeto JSON con un mensaje de error y un código de estado 401.
    """
        
    try:
        logger.debug("Procesando solicitud para autenticar un usuario.")
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        valid, response = user_login_tokenrole(username, password)
        if not valid:
            return jsonify(response), 401
        
        logger.info(f"Usuario {username} autenticado exitosamente.")
        return jsonify({'message': 'Usuario autenticado exitosamente.',
                        'token': response}), 200
    except Exception as e:
        logger.error(f"Error al procesar solicitud para autenticar un usuario: {e}")
        return {'error': 'Login fallido'}, 401

# # Definir la ruta para validar un token
@user_login_blueprint.route('/user_validate_token', methods=['POST'])
@user_auth_required
def user_validate_token():
    """
    Procesa la solicitud para validar un token de usuario.
    
    Returns:
        - Si el token es válido, devuelve la respuesta y el código de estado 200.
        - Si el token no es válido, devuelve la respuesta y el código de estado 401.
        - Si ocurre un error durante el procesamiento, devuelve un diccionario con el mensaje de error y el código de estado 401.
    """
    try:
        return {'message': 'validate_token'}
    except Exception as e:
        logger.error(f"Error al procesar solicitud para validar un token de usuario: {e}")
        return {'error': 'Verificacion de token fallida', 'check_token': False}

# # Definir la ruta para refrescar un token
@user_login_blueprint.route('/user_refresh_token', methods=['POST'])
@user_auth_refresh
def user_refresh_token():
    """
    Procesa la solicitud para refrescar un token de usuario.
    
    Returns:
        - Si el token se refresca correctamente, devuelve la respuesta y el código de estado 200.
        - Si el token no se refresca correctamente, devuelve la respuesta y el código de estado 401.
        - Si ocurre un error durante el procesamiento, devuelve un diccionario con el mensaje de error y el código de estado 401.
    """
    try:
        return {'message': 'refresh_token'}
    except Exception as e:
        logger.error(f"Error al procesar solicitud para refrescar un token de usuario: {e}")
        return {'error': 'Refresco de token fallido', 'check_token': False}

# # Definir la ruta para validar un token de administrador
@user_login_blueprint.route('/admin_validate_token', methods=['POST'])
@admin_auth_required
def admin_validate_token():
    """
    Procesa la solicitud para validar un token de administrador.
    
    Returns:
        - Si el token es válido, devuelve la respuesta y el código de estado 200.
        - Si el token no es válido, devuelve la respuesta y el código de estado 401.
        - Si ocurre un error durante el procesamiento, devuelve un diccionario con el mensaje de error y el código de estado 401.
    """
    try:
        return {'message': 'validate_admin_token'}
    except Exception as e:
        logger.error(f"Error al procesar solicitud para validar un token de administrador: {e}")
        return {'error': 'Verificacion de token fallida', 'check_token': False}

# # Definir la ruta para refrescar un token de administrador
@user_login_blueprint.route('/admin_refresh_token', methods=['POST'])
@admin_auth_refresh
def admin_refresh_token():
    """
    Procesa la solicitud para refrescar un token de administrador.
    
    Returns:
        - Si el token se refresca correctamente, devuelve la respuesta y el código de estado 200.
        - Si el token no se refresca correctamente, devuelve la respuesta y el código de estado 401.
        - Si ocurre un error durante el procesamiento, devuelve un diccionario con el mensaje de error y el código de estado 401.
    """
    try:
        return {'message': 'refresh_admin_token'}
    except Exception as e:
        logger.error(f"Error al procesar solicitud para refrescar un token de administrador: {e}")
        return {'error': 'Refresco de token fallido', 'check_token': False}