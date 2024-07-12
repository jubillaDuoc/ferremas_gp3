# Path: mainSonda/modules/crypto_data.py
# Package: mainSonda.modules
# Desc: Módulo para administrar el cifrado de informacion
# Developer: Vachir00
# # Importar módulos
import logging
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# # Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def to_bytes(data):
    if isinstance(data, str):
        return data.encode()  # Convierte la cadena a bytes usando UTF-8
    elif isinstance(data, dict):
        return json.dumps(data).encode()  # Convierte el diccionario a una cadena JSON y luego a bytes
    else:
        raise TypeError("El tipo de dato no es soportado para la conversión a bytes")

def to_str(data):
    try:
        return base64.b64encode(data).decode()
    except Exception as e:
        logger.error(f"Error al convertir los datos a string: {e}")
        return None

def encrypt_data(data, key):
    """
    Encrypts the given data using AES encryption with the provided key.

    Args:
        data (bytes): The data to be encrypted.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted data.

    """
    try:
        data = to_bytes(data)
        key = to_bytes(key)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        encrypt_data = cipher.iv + ct_bytes
        encrypt_data = to_str(encrypt_data)
        return encrypt_data
    except Exception as e:
        logger.error(f"Error al cifrar los datos: {e}")
        return None

def decrypt_data(data, key):
    """
    Decrypts the given data using the provided key.

    Args:
        data (bytes): The encrypted data to be decrypted.
        key (bytes): The key used for decryption.

    Returns:
        bytes: The decrypted plaintext.

    """
    try:
        key = to_bytes(key)
        data = base64.b64decode(data)   
        iv = data[:AES.block_size]
        ct = data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        pt = pt.decode()  # Use decode() instead of str()
        return pt
    except Exception as e:
        logger.error(f"Error al descifrar los datos: {e}")
        return None