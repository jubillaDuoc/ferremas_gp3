import logging
from datetime import datetime, timedelta
import json
from modules.postgres import DBConnection
from modules.system.generate_token import generate_token
from modules.system.crypto_data import encrypt_data, decrypt_data
from modules.system.get_config import get_mainKey

TABLA_USERS = 'USERS'
TABLA_USERS_COLUMNS = [
    'id_user',
    'nombre_user',
    'email_user',
    'passwd_user',
    'id_user_rol',
    'id_user_state'
]

VISTA_USERS = 'users_view'
VISTA_USERS_COLUMNS = [
    'id_user',
    'nombre_user',
    'passwd_user',
    'email_user',
    'id_user_rol',
    'nombre_user_rol',
    'id_user_state',
    'nombre_user_state'
]

VISTA_USERS_SECURE_COLUMNS = [
    'id_user',
    'nombre_user',
    'email_user',
    'id_user_rol',
    'nombre_user_rol',
    'id_user_state',
    'nombre_user_state'
]

TABLA_USERS_TOKEN = 'USERS_TOKEN'
TABLA_USERS_TOKEN_COLUMNS = [
    'token_session',
    'created_at_session',
    'valid_from_session',
    'valid_to_session',
    'id_user'
]

TABLA_USERS_ROLE = 'USERS_ROLE'
TABLA_USERS_ROLE_COLUMNS = [
    'id_user_rol',
    'nombre_user_rol'
]

TABLA_USERS_STATE = 'USERS_STATE'
TABLA_USERS_STATE_COLUMNS = [
    'id_user_state',
    'nombre_user_state'
]









