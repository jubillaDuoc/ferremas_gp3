import json
import logging

# Configura el logger para el módulo de monitoreo
logger = logging.getLogger(__name__)

def get_config():
    try:
        # Lee el archivo de configuración
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        # Registra el error con el logger en lugar de imprimirlo
        logger.error(f"Error al obtener la configuración: {e}")
        return None

def get_secrets():
    try:
        # Lee el archivo de secretos
        with open('secrets.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        # Registra el error con el logger en lugar de imprimirlo
        logger.error(f"Error al obtener los secretos: {e}")
        return None

def get_mainKey():
    try:
        # # Obtiene la clave principal del archivo de secretos
        secrets = get_secrets()
        return secrets['mainKey']
    except Exception as e:
        # Registra el error con el logger en lugar de imprimirlo
        logger.error(f"Error al obtener la clave principal: {e}")
        return None
