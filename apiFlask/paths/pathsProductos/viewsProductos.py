# Desc: Módulo para manejar los productos a nivel de API
# Developer: Vachir00

# Por justificación técnica y de seguridad todas las peticiones son POST

# Importar módulos
from flask import Blueprint, request, jsonify
import logging
# Importacion de modulos internos
from modules.system.api_decorators import user_auth_refresh, admin_auth_refresh
from modules.app.modulesProducto.moduleProductos import *
from modules.app.modulesProducto.moduleMarca import *
from modules.app.modulesProducto.moduleSubTipo import *
from modules.app.modulesProducto.moduleTipo import *
from modules.system.errors.handlers import register_error_handlers

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

# Crear un Blueprint para manejar las rutas de este módulo
productos_blueprint = Blueprint('productos', __name__)
register_error_handlers(productos_blueprint)

#############
# ALL USERS #
#############

# Definir la ruta para obtener todos los productos
@productos_blueprint.route('/get_productos', methods=['POST'])
@user_auth_refresh
def path_get_productos():
    """
    Procesa la solicitud para obtener todos los productos.

    Returns:
        Si los productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de productos.
        Si la obtención de los productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los productos.")

        valid, response = man_get_productos()
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener productos por tipo: {e}")
        return {'error': 'Error al obtener los productos.',
                'error_detail': str(e)}

# Definir la ruta para obtener un producto por ID
@productos_blueprint.route('/get_producto_by_id', methods=['POST'])
@user_auth_refresh
def path_get_producto_by_id():
    """
    Procesa la solicitud para obtener un producto por ID.

    Returns:
        Si el producto es obtenido exitosamente, devuelve un objeto JSON con la información del producto.
        Si la obtención del producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener un producto por ID.")

        data = request.get_json()
        id_producto = data.get('id_producto')
        
        if not id_producto:
            return {'error': 'Falta el ID del producto.'}
        
        valid, response = man_get_producto_by_id(id_producto)
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener un producto por ID: {e}")
        return {'error': 'Error al obtener el producto.',
                'error_detail': str(e)}

# Definir la ruta para obtener productos por tipo
@productos_blueprint.route('/get_productos_by_tipo', methods=['POST'])
@user_auth_refresh
def path_get_productos_by_tipo():
    """
    Procesa la solicitud para obtener productos por tipo.

    Returns:
        Si los productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de productos.
        Si la obtención de los productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener productos por tipo.")

        data = request.get_json()
        id_tipo = data.get('id_tipo')

        valid, response = man_get_productos_by_tipo(id_tipo)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener productos por tipo: {e}")
        return {'error': 'Error al obtener los productos.',
                'error_detail': str(e)}

# Definir la ruta para obtener productos por subtipo
@productos_blueprint.route('/get_productos_by_subtipo', methods=['POST'])
@user_auth_refresh
def path_get_productos_by_subtipo():
    """
    Procesa la solicitud para obtener productos por subtipo.

    Returns:
        Si los productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de productos.
        Si la obtención de los productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener productos por subtipo.")

        data = request.get_json()
        id_subtipo = data.get('id_subtipo')

        valid, response = man_get_productos_by_subtipo(id_subtipo)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener productos por subtipo: {e}")
        return {'error': 'Error al obtener los productos.',
                'error_detail': str(e)}

# Definir la ruta para obtener productos por marca
@productos_blueprint.route('/get_productos_by_marca', methods=['POST'])
@user_auth_refresh
def path_get_productos_by_marca():
    """
    Procesa la solicitud para obtener productos por marca.

    Returns:
        Si los productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de productos.
        Si la obtención de los productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener productos por marca.")

        data = request.get_json()
        id_marca = data.get('id_marca')

        valid, response = man_get_productos_by_marca(id_marca)
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener productos por marca: {e}")
        return {'error': 'Error al obtener los productos.',
                'error_detail': str(e)}

# Definir la ruta para obtener todos los tipos de productos
@productos_blueprint.route('/get_tipos', methods=['POST'])
@user_auth_refresh
def path_get_tipos():
    """
    Procesa la solicitud para obtener todos los tipos de productos.

    Returns:
        Si los tipos de productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de tipos de productos.
        Si la obtención de los tipos de productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los tipos de productos.")

        valid, response = man_get_tipos()
        if not valid:
            return response
        
        print(response)

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener tipos de productos: {e}")
        return {'error': 'Error al obtener los tipos de productos.',
                'error_detail': str(e)}

# Definir la ruta para obtener todos los subtipos de productos
@productos_blueprint.route('/get_subtipos', methods=['POST'])
@user_auth_refresh
def path_get_subtipos():
    """
    Procesa la solicitud para obtener todos los subtipos de productos.

    Returns:
        Si los subtipos de productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de subtipos de productos.
        Si la obtención de los subtipos de productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los subtipos de productos.")

        valid, response = man_get_subtipos()
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener subtipos de productos: {e}")
        return {'error': 'Error al obtener los subtipos de productos.',
                'error_detail': str(e)}

# Definir la ruta para obtener todas las marcas de productos
@productos_blueprint.route('/get_marcas', methods=['POST'])
@user_auth_refresh
def path_get_marcas():
    """
    Procesa la solicitud para obtener todas las marcas de productos.

    Returns:
        Si las marcas de productos son obtenidas exitosamente, devuelve un objeto JSON con la lista de marcas de productos.
        Si la obtención de las marcas de productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todas las marcas de productos.")

        valid, response = man_get_marcas()
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener marcas de productos: {e}")
        return {'error': 'Error al obtener las marcas de productos.',
                'error_detail': str(e)}



###################
# ADMINISTRADORES #
###################

# Definir la ruta para crear un producto
@productos_blueprint.route('/create_producto', methods=['POST'])
@admin_auth_refresh
def path_create_producto():
    """
    Procesa la solicitud para crear un producto.

    Returns:
        Si el producto es creado exitosamente, devuelve un objeto JSON con un mensaje de éxito.
        Si la creación del producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para crear un producto.")
        
        data = request.get_json()
        nombre_producto = data.get('nombre_producto')
        stock_producto = data.get('stock_producto')
        id_marca = data.get('id_marca')
        id_subtipo = data.get('id_subtipo')
        precio_producto = data.get('precio_producto')
        
        # Check if the data is valid
        if not nombre_producto or not stock_producto or not id_marca or not id_subtipo or not precio_producto:
            return {'error': 'Faltan datos requeridos para crear el producto.'}
        
        valid, response = man_create_producto(nombre_producto, stock_producto, id_marca, id_subtipo, precio_producto)
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para crear un producto: {e}")
        return {'error': 'Error al crear el producto.',
                'error_detail': str(e)}

# Definir la ruta para actualizar un producto
@productos_blueprint.route('/update_producto', methods=['POST'])
@admin_auth_refresh
def path_update_producto():
    """
    Procesa la solicitud para actualizar un producto.

    Returns:
        Si el producto es actualizado exitosamente, devuelve un objeto JSON con un mensaje de éxito.
        Si la actualización del producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para actualizar un producto.")

        data = request.get_json()
        id_producto = data.get('id_producto')
        nombre_producto = data.get('nombre_producto')
        id_marca = data.get('id_marca')
        id_subtipo = data.get('id_subtipo')
        precio_producto = data.get('precio_producto')
        stock_producto = data.get('stock_producto')

        valid, response = man_update_producto(id_producto, nombre_producto, id_marca, id_subtipo, precio_producto, stock_producto)
        if not valid:
            return response
        
        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para actualizar un producto: {e}")
        return {'error': 'Error al actualizar el producto.',
                'error_detail': str(e)}

# Definir la ruta para obtener todos los productos por un administrador
@productos_blueprint.route('/get_productos_by_admin', methods=['POST'])
@admin_auth_refresh
def path_get_productos_by_admin():
    """
    Procesa la solicitud para obtener todos los productos.

    Returns:
        Si los productos son obtenidos exitosamente, devuelve un objeto JSON con la lista de productos.
        Si la obtención de los productos falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para obtener todos los productos.")

        valid, response = man_get_productos()
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para obtener productos por tipo: {e}")
        return {'error': 'Error al obtener los productos.',
                'error_detail': str(e)}

# Definir la ruta para crear un subtipo de producto
@productos_blueprint.route('/create_subtipo', methods=['POST'])
@user_auth_refresh
def path_create_subtipo():
    """
    Procesa la solicitud para crear un subtipo de producto.

    Returns:
        Si el subtipo de producto es creado exitosamente, devuelve un objeto JSON con un mensaje de éxito.
        Si la creación del subtipo de producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para crear un subtipo de producto.")

        data = request.get_json()
        nombre_subtipo = data.get('nombre_subtipo')

        valid, response = man_create_subtipo(nombre_subtipo)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para crear un subtipo de producto: {e}")
        return {'error': 'Error al crear el subtipo de producto.',
                'error_detail': str(e)}

# Definir la ruta para crear una marca de producto
@productos_blueprint.route('/create_marca', methods=['POST'])
@user_auth_refresh
def path_create_marca():
    """
    Procesa la solicitud para crear una marca de producto.

    Returns:
        Si la marca de producto es creada exitosamente, devuelve un objeto JSON con un mensaje de éxito.
        Si la creación de la marca de producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para crear una marca de producto.")

        data = request.get_json()
        nombre_marca = data.get('nombre_marca')

        valid, response = man_create_marca(nombre_marca)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para crear una marca de producto: {e}")
        return {'error': 'Error al crear la marca de producto.',
                'error_detail': str(e)}

# Definir la ruta para crear un tipo de producto
@productos_blueprint.route('/create_tipo', methods=['POST'])
@user_auth_refresh
def path_create_tipo():
    """
    Procesa la solicitud para crear un tipo de producto.

    Returns:
        Si el tipo de producto es creado exitosamente, devuelve un objeto JSON con un mensaje de éxito.
        Si la creación del tipo de producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para crear un tipo de producto.")

        data = request.get_json()
        nombre_tipo = data.get('nombre_tipo')

        valid, response = man_create_tipo(nombre_tipo)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para crear un tipo de producto: {e}")
        return {'error': 'Error al crear el tipo de producto.',
                'error_detail': str(e)}

# Definir la ruta para actualizar el stock de un producto
@productos_blueprint.route('/update_stock_producto', methods=['POST'])
@user_auth_refresh
def path_update_stock_producto():
    """
    Procesa la solicitud para actualizar el stock de un producto.

    Returns:
        Si el stock del producto es actualizado exitosamente, devuelve un objeto JSON con un mensaje de éxito.
        Si la actualización del stock del producto falla, devuelve un objeto JSON con un mensaje de error y un código de estado 400.
    """
    try:
        logger.debug("Procesando solicitud para actualizar el stock de un producto.")

        data = request.get_json()
        id_producto = data.get('id_producto')
        stock = data.get('stock')

        valid, response = man_update_stock_producto(id_producto, stock)
        if not valid:
            return response

        return response
    except Exception as e:
        logger.error(f"Error al procesar solicitud para actualizar el stock de un producto: {e}")
        return {'error': 'Error al actualizar el stock del producto.',
                'error_detail': str(e)}