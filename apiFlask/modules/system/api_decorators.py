from flask import request, jsonify
import logging
from functools import wraps
from modules.auth.moduleUserAuth import check_user_token, refresh_user_token, check_admin_token, refresh_admin_token

# # Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def user_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            logger.debug("Procesando solicitud para validar un token de usuario.")
        
            data = request.get_json()
            token = data.get('token')
            
            valid, response = check_user_token(token)
            if not valid:
                return response, 401
            
            logger.info(f"Token de usuario validado exitosamente.")
        except:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Llamar a la función de vista y obtener la respuesta
            response = f(*args, **kwargs)
            
            # Si la respuesta es un objeto JSON, agregar información de validación
            if isinstance(response, dict):
                if response.get('check_token') == False:
                    return response, 401
                print(1)
                response['check_token'] = True
                return response, 200
            else:
                logger.error("Falla en el procesamiento de la solicitud1")
                return 500
        except Exception as e:
            logger.error(f"Falla en el procesamiento de la solicitud: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500          
    return decorated

def user_auth_refresh(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            logger.debug("Procesando solicitud para refrescar un token de usuario.")
        
            data = request.get_json()
            token = data.get('token')
            
            valid, tokenResponse = refresh_user_token(token)
            if not valid:
                return tokenResponse, 401
            
            logger.info(f"Token de usuario refrescado exitosamente.")
        except:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Llamar a la función de vista y obtener la respuesta
            dataResponse = f(*args, **kwargs)
            
            # Si la respuesta es un objeto JSON, agregar información de validación
            if isinstance(dataResponse, dict):
                if dataResponse.get('check_token') == False:
                    return dataResponse, 401
                dataResponse['check_token'] = True
                return dataResponse, 200
            else:
                logger.error("Falla en el procesamiento de la solicitud")
                return 500
        except Exception as e:
            logger.error(f"Falla en el procesamiento de la solicitud: {e}")
            jsonify({'error': 'Error interno del servidor'}), 500
    return decorated

def admin_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            logger.debug("Procesando solicitud para validar un token de administrador.")
        
            data = request.get_json()
            token = data.get('token')
            
            valid, response = check_admin_token(token)
            if not valid:
                return response, 401
            
            logger.info(f"Token de administrador validado exitosamente.")
        except:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Llamar a la función de vista y obtener la respuesta
            response = f(*args, **kwargs)
            
            # Si la respuesta es un objeto JSON, agregar información de validación
            if isinstance(response, dict):
                if response.get('check_token') == False:
                    return response, 401
                response['check_token'] = True
                return response, 200
            else:
                logger.error("Falla en el procesamiento de la solicitud")
                return 500
        except Exception as e:
            logger.error(f"Falla en el procesamiento de la solicitud: {e}")
            return jsonify({'error': 'Error interno del servidor'}), 500          
    return decorated

def admin_auth_refresh(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            logger.debug("Procesando solicitud para refrescar un token de administrador.")
        
            data = request.get_json()
            token = data.get('token')
            
            valid, tokenResponse = refresh_admin_token(token)
            if not valid:
                return tokenResponse, 401
            
            logger.info(f"Token de administrador refrescado exitosamente.")
        except:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Llamar a la función de vista y obtener la respuesta
            dataResponse = f(*args, **kwargs)
            
            # Si la respuesta es un objeto JSON, agregar información de validación
            if isinstance(dataResponse, dict):
                if dataResponse.get('check_token') == False:
                    return dataResponse, 401
                dataResponse['check_token'] = True
                return dataResponse, 200
            else:
                logger.error("Falla en el procesamiento de la solicitud")
                return 500
        except Exception as e:
            logger.error(f"Falla en el procesamiento de la solicitud: {e}")
            jsonify({'error': 'Error interno del servidor'}), 500
    return decorated