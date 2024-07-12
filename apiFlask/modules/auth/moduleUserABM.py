import logging
import json

from models.modelsUsers.modelUser import UsersModel
from models.modelsUsers.modelUserRol import UsersRolModel
from models.modelsUsers.modelUserState import UsersStateModel
from modules.system.crypto_data import encrypt_data, decrypt_data
from modules.system.get_config import get_mainKey

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

# Crear usuario
def create_user(email, passwd, nombre_user, rol = None, estado = None):
    
    try:
        if rol is None:
            rol = 5
        else:
            rol = int(rol)
        if estado is None:
            estado = 1
        else:
            estado = int(estado)
    except:
        return False, {'error': 'Error en los datos de entrada.'}
    
    try:
        # Validar si el usuario ya existe
        currentUser = UsersModel().get_user_by_email(email)
        
        if currentUser and currentUser.get_email_user() == email:
            return False, {'error': 'El usuario ya existe.'}
        
        # Encriptar clave de usuario
        if passwd:
            passwd = encrypt_data(passwd, get_mainKey())
        else:
            return False, {'error': 'La clave de usuario no puede estar vacía.'}
        
        # Obtener rol del usuario
        newUser_rol = UsersRolModel().get_user_rol_by_id(rol)
        
        if not newUser_rol or not newUser_rol.get_id_user_rol():
            return False, {'error': 'El rol de usuario no existe.'}
        
        # Obtener Estado del usuario
        newUser_state = UsersStateModel().get_user_state_by_id(estado)
        
        if not newUser_state or not newUser_state.get_id_user_state():
            return False, {'error': 'El estado de usuario no existe.'}
        
        # Configurar usuario
        newUser = UsersModel()
        newUser.set_nombre_user(nombre_user)
        newUser.set_email_user(email)
        newUser.set_passwd_user(passwd)
        newUser.set_user_rol(newUser_rol)
        newUser.set_user_state(newUser_state)
        
        # Guardar usuario
        newUser.save_user()
        
        if not isinstance(newUser.get_id_user(), int):
            return None, {'error': 'Error al guardar el usuario.'}
        
        # Devolver la respuesta
        logger.info(f"Usuario {email} creado exitosamente.")
        return True, {'message': 'Usuario creado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para crear un usuario
        logger.error(f"Error al procesar solicitud para crear un usuario: {e}")
        return False, {'error': 'Error al crear el usuario.',
                       'error_detail': str(e)}

# Actualizar usuario
def update_user_by_id(*,
                id_user=None,
                passwd=None,
                nombre_user=None,
                rol=None,
                estado=None):
    try:
        # Instanciar clase Usuario
        user = UsersModel().get_user_by_id(id_user)
        
        if not user or not user.get_id_user():
            return None, {'error': 'El usuario no existe.'}
        
        ## Nuevos valores
        
        # Encriptar clave de usuario
        if passwd:
            passwd = encrypt_data(passwd, get_mainKey())
        
        # Configurar usuario
        if passwd:
            user.set_passwd_user(passwd)
        if nombre_user:
            user.set_nombre_user(nombre_user)
        if rol:
            # Obtener nuevo rol del usuario
            newUser_rol = UsersRolModel().get_user_rol_by_id(rol)
        
            if not newUser_rol or not newUser_rol.get_id_user_rol():
                return False, {'error': 'El rol de usuario no existe.'}
            
            # Process the query result
            user.set_user_rol(newUser_rol)
        if estado:
            # Obtener nuevo Estado del usuario
            newUser_state = UsersStateModel().get_user_state_by_id(estado)
        
            if not newUser_state or not newUser_state.get_id_user_state():
                return False, {'error': 'El estado de usuario no existe.'}
        
            # Process the query result
            user.set_user_state(newUser_state)
        
        # Actualizar usuario
        updateUser = user.update_user()
        
        if not updateUser:
            return False, {'error': 'Error al actualizar el usuario.'}

        logger.info(f"User with ID {user.get_id_user()} updated successfully")
        return True, {'message': 'Usuario actualizado exitosamente.'}
    
    except Exception as e:
        # Error al procesar la solicitud para actualizar un usuario
        logger.error(f"Error al procesar solicitud para actualizar un usuario: {e}")
        return False, {'error': 'Error al actualizar el usuario.',
                       'error_detail': str(e)}

def get_all_users():
    try:
        # Instanciar clase usuario
        userClass = UsersModel()
        
        # Obtener todos los usuarios
        userList = userClass.get_all_users()
        if not userList:
            return False, {'error': 'Error al obtener la lista de usuarios'}
        
        return True, {'users': userList}
    except Exception as e:
        # Error al procesar la solicitud para obtener todos los usuarios
        logger.error(f"Error al procesar solicitud para obtener todos los usuarios: {e}")
        return False, {'error': 'Error al obtener los usuarios.',
                       'error_detail': str(e)}

def man_get_user_by_id(id_user):
    try:
        # Instanciar clase usuario
        userClass = UsersModel()
        
        # Obtener usuario por ID
        user = userClass.get_user_by_id(id_user)
        if not user:
            return False, {'error': 'Error al obtener el usuario'}
        
        userData = user.to_json()
        
        return True, {'user': userData}
    except Exception as e:
        # Error al procesar la solicitud para obtener un usuario por su ID
        logger.error(f"Error al procesar solicitud para obtener un usuario por su ID: {e}")
        return False, {'error': 'Error al obtener el usuario por su ID.',
                       'error_detail': str(e)}

def man_get_roles():
    try:
        # Instanciar clase rol de usuario
        rolClass = UsersRolModel()
        
        # Obtener todos los roles de usuario
        roles = rolClass.get_all_user_roles()
        if not roles:
            return False, {'error': 'Error al obtener la lista de roles de usuario'}
        
        return True, {'roles': roles}
    except Exception as e:
        # Error al procesar la solicitud para obtener todos los roles de usuario
        logger.error(f"Error al procesar solicitud para obtener todos los roles de usuario: {e}")
        return False, {'error': 'Error al obtener los roles de usuario.',
                       'error_detail': str(e)}

def man_get_states():
    try:
        # Instanciar clase estado de usuario
        stateClass = UsersStateModel()
        
        # Obtener todos los estados de usuario
        states = stateClass.get_all_user_states()
        if not states:
            return False, {'error': 'Error al obtener la lista de estados de usuario'}
        
        return True, {'states': states}
    except Exception as e:
        # Error al procesar la solicitud para obtener todos los estados de usuario
        logger.error(f"Error al procesar solicitud para obtener todos los estados de usuario: {e}")
        return False, {'error': 'Error al obtener los estados de usuario.',
                       'error_detail': str(e)}

def man_get_user_by_email(user_mail):
    try:
        # Instanciar clase usuario
        userClass = UsersModel()
        
        # Obtener usuario por email
        user = userClass.get_user_by_email(user_mail)
        if not user.get_id_user():
            return False, {'error': 'Error al obtener el usuario'}
        
        userData = user.to_json()
        
        return True, {'user': userData}
    except Exception as e:
        # Error al procesar la solicitud para obtener un usuario por su email
        logger.error(f"Error al procesar solicitud para obtener un usuario por su email: {e}")
        return False, {'error': 'Error al obtener el usuario por su email.',
                       'error_detail': str(e)}