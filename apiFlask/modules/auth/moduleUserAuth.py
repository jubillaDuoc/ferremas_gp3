import logging
import json

from models.modelsUsers.modelUser import UsersModel
from models.modelsUsers.modelUserRol import UsersRolModel
from models.modelsUsers.modelUserState import UsersStateModel
from models.modelsUsers.modelUserToken import UsersTokenModel
from modules.system.crypto_data import encrypt_data
from modules.system.get_config import get_mainKey

# # Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def user_login_tokenrole(username, password):
    logger.debug("Procesando solicitud para autenticar un usuario.")
    try:
        # Instanciar clase Usuario
        logger.debug("Instanciando clase Usuario.")
        user = UsersModel()
        logger.debug("Clase Usuario instanciada.")
        
        # Encriptar clave de usuario
        logger.debug("Encriptando clave de usuario.")
        password = encrypt_data(password, get_mainKey())
        logger.debug("Clave de usuario encriptada.")
        
        # Autenticar al usuario
        logger.debug("Autenticando al usuario.")
        idUser = user.check_user_credentials(username, password)
        logger.debug(f"Usuario autenticado: {idUser}")
        if not idUser:
            return False, {'error': 'Usuario o contraseña incorrectos.'}
        
        # Obtener datos del usuario
        logger.debug("Obteniendo datos del usuario.")
        userData = user.get_user_by_id(idUser)
        if not isinstance(userData, UsersModel):
            return False, {'error': 'Error al obtener datos del usuario.'}
        
        # Validar que el usuario esté activo
        logger.debug("Validando estado del usuario.")
        if not userData.is_active():
            return False, {'error': 'Usuario no activo.'}
        
        # Crear un token para el usuario
        token = UsersTokenModel().create_user_token(idUser)
        if not token:
            return False, {'error': 'Error al crear el token.'}
        
        # Devolver la respuesta
        logger.info(f"Usuario {username} autenticado exitosamente.")
        return True, token
    except Exception as e:
        # Error al procesar la solicitud para autenticar un usuario
        logger.error(f"Error al procesar solicitud para autenticar un usuario: {e}")
        return False, {'error': 'Error al autenticar el usuario.',
                       'error_detail': str(e)}

def check_user_token(token):
    try:
        # Validar el token
        validToken = UsersTokenModel().check_user_token(token)
        if not validToken:
            return False, {'error': 'Token inválido.',
                           'check_token': False}
    except Exception as e:
        return False, {'error': 'Error al validar el token.',
                    'error_detail': str(e),
                    'check_token': False}
    return True, {'message': 'Token válido.',
                  'check_token': True}

def refresh_user_token(token):
    try:
        # Refrescar el token
        newToken = UsersTokenModel().refresh_user_token(token)
        if not newToken:
            return False, {'error': 'Error al refrescar el token.',
                           'check_token': False}
    except Exception as e:
        return False, {'error': 'Error al refrescar el token.',
                    'error_detail': str(e),
                    'check_token': False}
    return True, {'message': 'Token refrescado.',
                  'check_token': True}

def check_admin_token(token):
    try:
        # Validar el token
        validToken = UsersTokenModel().check_admin_token(token)
        if not validToken:
            return False, {'error': 'Token inválido.',
                           'check_token': False}
    except Exception as e:
        return False, {'error': 'Error al validar el token.',
                    'error_detail': str(e),
                    'check_token': False}
    return True, {'message': 'Token válido.',
                  'check_token': True}

def refresh_admin_token(token):
    try:
        # Refrescar el token
        newToken = UsersTokenModel().refresh_admin_token(token)
        if not newToken:
            return False, {'error': 'Error al refrescar el token.',
                           'check_token': False}
    except Exception as e:
        return False, {'error': 'Error al refrescar el token.',
                    'error_detail': str(e),
                    'check_token': False}
    return True, {'message': 'Token refrescado.',
                  'check_token': True}