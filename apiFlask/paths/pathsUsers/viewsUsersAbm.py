# Desc: Módulo para manejar la alta, baja y modificación de usuarios
# Developer: Vachir00
# # Importar módulos
from flask import Blueprint, request, jsonify
import logging
# # Importacion de modulos internos
from modules.auth.moduleUserABM import create_user, update_user_by_id
from modules.auth.moduleUserABM import get_all_users, man_get_user_by_id, man_get_roles, man_get_states, man_get_user_by_email
from modules.system.errors.handlers import register_error_handlers
from modules.system.api_decorators import user_auth_required, user_auth_refresh, admin_auth_refresh

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

# Crear un Blueprint para manejar las rutas de este módulo
user_abm_blueprint = Blueprint('user_abm', __name__)
register_error_handlers(user_abm_blueprint)

# Definir la ruta para crear un usuario
@user_abm_blueprint.route('/user_create', methods=['POST'])
#@user_auth_refresh
def user_create():
    """
    Procesa la solicitud para crear un usuario.

    Returns:
        Si la creación es exitosa, devuelve un objeto JSON con un mensaje de éxito.
        Si la creación falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para crear un usuario.")

        data = request.get_json()
        email = data.get('email')
        passwd = data.get('passwd')
        nombre_user = data.get('nombre_user')

        valid, response = create_user(email, passwd, nombre_user)
        if not valid:
            return jsonify(response), 400

        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error al procesar solicitud para crear un usuario: {e}")
        return {'error': 'Error al crear el usuario.'}, 400

# Definir la ruta para actualizar un usuario
@user_abm_blueprint.route('/user_update', methods=['POST'])
@user_auth_refresh
def user_update():
    """
    Procesa la solicitud para actualizar un usuario.

    Returns:
        Si la actualización es exitosa, devuelve un objeto JSON con un mensaje de éxito.
        Si la actualización falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para actualizar un usuario.")

        data = request.get_json()
        idUser = data.get('idUser')
        passwd = data.get('passwd')
        nombre_user = data.get('nombre_user')

        valid, response = update_user_by_id(id_user=idUser, passwd=passwd, nombre_user=nombre_user)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para actualizar un usuario: {e}")
        return {'error': 'Error al actualizar el usuario.'}

# Definir la ruta para obtener un usuario por correo
@user_abm_blueprint.route('/get_user_by_mail', methods=['POST'])
@user_auth_refresh
def get_user_by_mail():
    """
    Procesa la solicitud para obtener un usuario por su correo.

    Returns:
        Si la solicitud es exitosa, devuelve un objeto JSON con el usuario.
        Si la solicitud falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener un usuario por su ID.")

        data = request.get_json()
        mail_user = data.get('mail_user')

        valid, response = man_get_user_by_email(mail_user)
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener un usuario por su ID: {e}")
        return {'error': 'Error al obtener el usuario.'}
    
###################
# ADMINISTRADORES #
###################

# Crear Usuario por un Administrador
@user_abm_blueprint.route('/admin_user_create', methods=['POST'])
@admin_auth_refresh
def admin_user_create():
    """
    Procesa la solicitud para crear un usuario.

    Returns:
        Si la creación es exitosa, devuelve un objeto JSON con un mensaje de éxito.
        Si la creación falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para crear un usuario.")

        data = request.get_json()
        email = data.get('email')
        passwd = data.get('passwd')
        nombre_user = data.get('nombre_user')
        rol = data.get('id_rol')
        estado = data.get('id_estado')

        valid, response = create_user(email, passwd, nombre_user, rol, estado)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para crear un usuario: {e}")
        return {'error': 'Error al crear el usuario.'}

# Obtener todos los usuarios
@user_abm_blueprint.route('/user_get_all', methods=['POST'])
@admin_auth_refresh
def user_get_all():
    """
    Procesa la solicitud para obtener todos los usuarios.

    Returns:
        Si la solicitud es exitosa, devuelve un objeto JSON con todos los usuarios.
        Si la solicitud falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los usuarios.")
        
        valid, response = get_all_users()
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener todos los usuarios: {e}")
        return {'error': 'Error al obtener los usuarios.'}

# Obtener todos los roles
@user_abm_blueprint.route('/get_roles', methods=['POST'])
@admin_auth_refresh
def get_roles():
    """
    Procesa la solicitud para obtener todos los roles de usuario.

    Returns:
        Si la solicitud es exitosa, devuelve un objeto JSON con todos los roles de usuario.
        Si la solicitud falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los roles de usuario.")
        
        valid, response = man_get_roles()
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener todos los roles de usuario: {e}")
        return {'error': 'Error al obtener los roles de usuario.'}

# Obtener todos los estados
@user_abm_blueprint.route('/get_states', methods=['POST'])
@admin_auth_refresh
def get_states():
    """
    Procesa la solicitud para obtener todos los estados de usuario.

    Returns:
        Si la solicitud es exitosa, devuelve un objeto JSON con todos los estados de usuario.
        Si la solicitud falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los estados de usuario.")
        
        valid, response = man_get_states()
        if not valid: return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener todos los estados de usuario: {e}")
        return {'error': 'Error al obtener los estados de usuario.'}

# Obtener un usuario por su id
@user_abm_blueprint.route('/get_user_by_id', methods=['POST'])
@admin_auth_refresh
def get_user_by_id():
    """
    Procesa la solicitud para obtener un usuario por su ID.

    Returns:
        Si la solicitud es exitosa, devuelve un objeto JSON con el usuario.
        Si la solicitud falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener un usuario por su ID.")

        data = request.get_json()
        id_user = data.get('id_user')

        valid, response = man_get_user_by_id(id_user)
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener un usuario por su ID: {e}")
        return {'error': 'Error al obtener el usuario.'}


# Definir la ruta para actualizar un usuario ADMIN
@user_abm_blueprint.route('/user_update_admin', methods=['POST'])
@admin_auth_refresh
def user_update_admin():
    """
    Procesa la solicitud para actualizar un usuario.

    Returns:
        Si la actualización es exitosa, devuelve un objeto JSON con un mensaje de éxito.
        Si la actualización falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para actualizar un usuario.")

        data = request.get_json()
        idUser = data.get('idUser')
        passwd = data.get('passwd')
        nombre_user = data.get('nombre_user')
        rol = data.get('id_rol')
        estado = data.get('id_estado')

        valid, response = update_user_by_id(id_user=idUser, passwd=passwd, nombre_user=nombre_user, rol=rol, estado=estado)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para actualizar un usuario: {e}")
        return {'error': 'Error al actualizar el usuario.'}
