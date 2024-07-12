# Path: mainSonda/modules/postgres/templates/token/user_token.py
# Package: mainSonda.modules.postgres.templates.token
# Desc: Módulo para manejar la creación y manejo de tokens en la base de datos
# Developer: Vachir00
# # # Importar módulos
import logging
import secrets
import string
import hashlib
# # # Importar módulos internos

# # Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def generate_token(*, seed = None):
    if seed is not None:
        
        try:
            seed = str(seed)
        except Exception as e:
            logger.error(f"Error al convertir la semilla a string. ErrorDetail: {str(e)}")
            return False, {'error': 'Error al convertir la semilla a string.',
                        'error_detail': str(e)}
        
        try:
            # # Generar un token
            alphabet = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(alphabet) for _ in range(256))

            # Mezclar el token con la semilla
            seed_bytes = seed.encode()  # Convertir la semilla a bytes
            token_bytes = token.encode()  # Convertir el token a bytes
            hashed = hashlib.sha256(seed_bytes + token_bytes)  # Hash de la semilla y el token
            final_token = hashed.hexdigest()  # Convertir el hash a una cadena hexadecimal

            return True, final_token
        except Exception as e:
            logger.error(f"Error al generar el token2. ErrorDetail: {str(e)}")
            return False, {'error': 'Error al generar el token.',
                        'error_detail': str(e)}
    try:
        # # Generar un token
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(256))
        return True, token
    except Exception as e:
        logger.error(f"Error al generar el token1. ErrorDetail: {str(e)}")
        return False, {'error': 'Error al generar el token.',
                       'error_detail': str(e)}