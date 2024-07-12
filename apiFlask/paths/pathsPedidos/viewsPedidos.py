# Desc: Módulo para manejar los pedidos a nivel de API
# Developer: Vachir00

# Por justificación técnica y de seguridad todas las peticiones son POST

# Importar módulos
from flask import Blueprint, request, jsonify
import logging
# Importacion de modulos internos
from modules.system.api_decorators import user_auth_refresh, admin_auth_refresh
from modules.system.errors.handlers import register_error_handlers
from modules.app.modulesPedido.modulePedido import *

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

# Crear un Blueprint para manejar las rutas de este módulo
pedidos_blueprint = Blueprint('pedidos', __name__)
register_error_handlers(pedidos_blueprint)

# Ruta para crear un pedido
@pedidos_blueprint.route('/create_order', methods=['POST'])
@user_auth_refresh
def create_order():
    try:
        # Obtener datos del pedido
        mailUser = request.json.get('mailUser')
        product = request.json.get('product')
        
        product_requeriments = ['id_producto', 'cantidad_producto', 'precio_producto']
        
        for requeriment in product_requeriments:
            if requeriment not in product:
                return {'error': 'Missing product requeriments.'}
        
        # Crear pedido
        success, response = man_create_order(mailUser, product)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para crear un pedido
        logger.error(f"Error processing request to create an order: {e}")
        return {'error': 'Error creating the order.',
                'error_detail': str(e)}

# Ruta para actualizar el estado de un pedido
@pedidos_blueprint.route('/update_order_status', methods=['POST'])
@user_auth_refresh
def update_order_status():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idOrder')
        status_id = request.json.get('status_id')
        
        # Actualizar estado del pedido
        success, response = man_update_order_status(idOrder, status_id)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para actualizar el estado de un pedido
        logger.error(f"Error processing request to update the order status: {e}")
        return {'error': 'Error updating the order status.',
                'error_detail': str(e)}

# Ruta para obtener los pedidos
@pedidos_blueprint.route('/get_orders', methods=['POST'])
@admin_auth_refresh
def get_orders():
    try:
        # Obtener pedidos
        success, response = man_get_all_orders()
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para obtener los pedidos
        logger.error(f"Error processing request to get orders: {e}")
        return {'error': 'Error getting orders.',
                'error_detail': str(e)}

# Ruta para obtener todos los detalles de un pedido
@pedidos_blueprint.route('/get_order_fulldetail', methods=['POST'])
@user_auth_refresh
def get_order_fulldetail():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idOrder')
        
        # Obtener detalles del pedido
        success, response = man_get_order_fulldetail(idOrder)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para obtener los detalles de un pedido
        logger.error(f"Error processing request to get order details: {e}")
        return {'error': 'Error getting order details.',
                'error_detail': str(e)}

# Ruta para obtener los pedidos de un usuario
@pedidos_blueprint.route('/get_user_orders', methods=['POST'])
@user_auth_refresh
def get_user_orders():
    try:
        # Obtener datos del pedido
        mailUser = request.json.get('mailUser')
        
        # Obtener pedidos del usuario
        success, response = man_get_user_orders(mailUser)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para obtener los pedidos de un usuario
        logger.error(f"Error processing request to get user orders: {e}")
        return {'error': 'Error getting user orders.',
            'error_detail': str(e)}

# Ruta para obtener los detalles de un pedido
@pedidos_blueprint.route('/get_order_detail', methods=['POST'])
@user_auth_refresh
def get_order_detail():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idOrder')
        
        # Obtener detalles del pedido
        success, response = man_get_order_detail(idOrder)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para obtener los detalles de un pedido
        logger.error(f"Error processing request to get order details: {e}")
        return {'error': 'Error getting order details.',
                'error_detail': str(e)}

# Ruta para obtener los estados posibles de un pedido
@pedidos_blueprint.route('/get_order_states', methods=['POST'])
@user_auth_refresh
def get_order_states():
    try:
        # Obtener estados de pedido
        success, response = man_get_order_states()
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para obtener los estados posibles de un pedido
        logger.error(f"Error processing request to get order states: {e}")
        return {'error': 'Error getting order states.',
                'error_detail': str(e)}

# Ruta para agregar productos a un pedido
@pedidos_blueprint.route('/add_product_to_order', methods=['POST'])
@user_auth_refresh
def add_product_to_order():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idOrder')
        product = request.json.get('product')
        
        product_requeriments = ['id_producto', 'cantidad_producto', 'precio_producto']
        
        for requeriment in product_requeriments:
            if requeriment not in product:
                return {'error': 'Missing product requeriments.'}
        
        # Agregar producto al pedido
        success, response = man_add_product_to_order(idOrder, product)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para agregar productos a un pedido
        logger.error(f"Error processing request to add products to an order: {e}")
        return {'error': 'Error adding products to the order.',
                'error_detail': str(e)}

# Ruta para eliminar productos de un pedido
@pedidos_blueprint.route('/remove_product_from_order', methods=['POST'])
@user_auth_refresh
def remove_product_from_order():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idOrder')
        idProduct = request.json.get('idProducto')
        
        # Eliminar producto del pedido
        success, response = man_remove_product_from_order(idOrder, idProduct)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para eliminar productos de un pedido
        logger.error(f"Error processing request to remove products from an order: {e}")
        return {'error': 'Error removing products from the order.',
                'error_detail': str(e)}

# Ruta para cambiar la cantidad de un producto en un pedido
@pedidos_blueprint.route('/change_product_quantity', methods=['POST'])
@user_auth_refresh
def change_product_quantity():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idOrder')
        idProduct = request.json.get('idProduct')
        newQty = request.json.get('newQty')
        
        # Cambiar cantidad de producto en el pedido
        success, response = man_change_product_quantity_from_order(idOrder, idProduct, newQty)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para cambiar la cantidad de un producto en un pedido
        logger.error(f"Error processing request to change the quantity of a product in an order: {e}")
        return {'error': 'Error changing the quantity of a product in the order.',
                'error_detail': str(e)}

# Ruta para cargar el carrito del usuario
@pedidos_blueprint.route('/load_cart', methods=['POST'])
@user_auth_refresh
def load_cart():
    try:
        # Obtener datos del pedido
        mailUser = request.json.get('mailUser')
        logger.debug(f"Loading cart for user {mailUser}")
        
        # Cargar carrito del usuario
        success, response = man_get_carrito_by_user(mailUser)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para cargar el carrito del usuario
        logger.error(f"Error processing request to load the user cart: {e}")
        return {'error': 'Error loading the user cart.',
                'error_detail': str(e)}

# Ruta para vaciar el carrito del usuario
@pedidos_blueprint.route('/clear_order', methods=['POST'])
@user_auth_refresh
def clear_order():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idPedido')
        
        # Vaciar carrito del usuario
        success, response = man_clear_order(idOrder)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para vaciar el carrito del usuario
        logger.error(f"Error processing request to clear the user cart: {e}")
        return {'error': 'Error clearing the user cart.',
                'error_detail': str(e)}

# Ruta para forzar el guardado del pedido
@pedidos_blueprint.route('/save_order', methods=['POST'])
@user_auth_refresh
def save_order():
    try:
        # Obtener datos del pedido
        idOrder = request.json.get('idPedido')
        
        # Guardar pedido
        success, response = man_save_order(idOrder)
        
        return response
    except Exception as e:
        # Error al procesar la solicitud para forzar el guardado del pedido
        logger.error(f"Error processing request to save the order: {e}")
        return {'error': 'Error saving the order.',
                'error_detail': str(e)}