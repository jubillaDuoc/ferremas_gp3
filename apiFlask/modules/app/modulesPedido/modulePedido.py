import logging
import datetime

from models.modelsPedidos.modelPedido import Pedido
from models.modelsPedidos.modelEstadoPedido import EstadoPedido
from models.modelsUsers.modelUser import UsersModel
from models.modelsProductos.modelProducto import Producto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def man_create_order(mailUser, product, status_id=1):
    try:
        logger.info(f"Creating order for user: {mailUser}")
        
        # Obtener ID del usuario
        user = UsersModel().get_user_by_email(mailUser)
        if not isinstance(user, UsersModel):
            logger.error(f"User not found.")
            return None, {'error': 'User not found.'}
        
        idUser = user.get_id_user()
        
        # Instanciar clase Pedido
        order = Pedido()
        order.set_idUser(idUser)
        order.set_fechaPedido(datetime.datetime.now())
        order.set_totalPedido(0)  # Inicialmente 0, se calculará al agregar productos

        # Establecer estado del pedido
        status = EstadoPedido().get_estado_pedido_by_id(status_id)
        if not isinstance(status, EstadoPedido):
            logger.error(f"The order status does not exist.")
            return None, {'error': 'The order status does not exist.'}
        
        order.set_estadoPedido(status)

        # Agregar producto
        order.add_producto(product['id_producto'], product['cantidad_producto'], product['precio_producto'])

        # Guardar pedido
        if not order.guardar_pedido():
            logger.error(f"Error saving the order.")
            return False, {'error': 'Error saving the order.'}
        
        logger.info(f"Order saved successfully.")
        return True, {'message': 'Order created successfully.'}
    except Exception as e:
        # Error al procesar la solicitud para crear un pedido
        logger.error(f"Error processing request to create an order: {e}")
        return False, {'error': 'Error creating the order.',
                       'error_detail': str(e)}

def man_get_carrito_by_user(mailUser):
    try:
        logger.info(f"Getting shopping cart for user: {mailUser}")
        
        # Obtener ID del usuario
        user = UsersModel().get_user_by_email(mailUser)
        if not isinstance(user, UsersModel):
            logger.error(f"User not found.")
            return None, {'error': 'User not found.'}
        
        idUser = user.get_id_user()
        
        logger.debug(f"Getting shopping cart for User ID: {idUser}")
        
        # Obtener carrito del usuario
        order = Pedido()
        carrito = order.get_carrito_by_idUser(idUser)
        
        if not carrito:
            return False, {'error': 'No shopping cart found for the user.'}
        
        carrito = carrito.to_json()
        
        # Enriquecer datos de los productos del carrito con información adicional
        for product in carrito['productos']:
            product_info = Producto().get_producto_by_id(product['id_producto'])
            if product_info:
                product['nombre_producto'] = product_info.get_nombre()
        
        return True, {'order': carrito}
    except Exception as e:
        logger.error(f"Error getting shopping cart: {e}")
        return False, {'error': 'Error getting shopping cart.',
                       'error_detail': str(e)}

def man_update_order_status(idOrder, status_id):
    try:
        # Instanciar clase Pedido
        order = Pedido()
        order = order.get_pedido_by_id(idOrder)
        
        if not order:
            return False, {'error': 'Order not found.'}

        # Establecer nuevo estado del pedido
        status = EstadoPedido().get_estado_pedido_by_id(status_id)
        if not isinstance(status, EstadoPedido):
            logger.error(f"The order status does not exist.")
            return None, {'error': 'The order status does not exist.'}

        order.set_estadoPedido(status)
        
        # Guardar pedido
        if not order.guardar_pedido():
            return False, {'error': 'Error updating the order status.'}
        
        logger.info(f"Order status {idOrder} updated successfully.")
        return True, {'message': 'Order status updated successfully.'}
    except Exception as e:
        # Error al procesar la solicitud para actualizar el estado del pedido
        logger.error(f"Error processing request to update order status: {e}")
        return False, {'error': 'Error updating the order status.',
                       'error_detail': str(e)}

def man_get_order_detail(idOrder):
    try:
        logger.info(f"Getting order details: {idOrder}")

        # Obtener detalles del pedido
        order = Pedido()
        order_info = order.get_pedido_by_id(idOrder)
        
        passtest = 1
        
        if not isinstance(order_info, Pedido):
            return False, {'error': 'Order not found.'}
        
        passtest = 2
        
        orderData = order_info.to_json()
        
        passtest = 3
        
        return True, {'order': orderData}
    except Exception as e:
        logger.error(f"Error getting order details: {e}")
        return False, {'error': 'Error getting order details1.',
                       'error_detail': str(e),
                       'passtest': passtest}


def man_get_order_fulldetail(idOrder):
    try:
        logger.info(f"Getting order details: {idOrder}")

        # Obtener detalles del pedido
        order = Pedido()
        
        order_legacyData = order.get_pedido_by_id(idOrder)
        if not isinstance(order_legacyData, Pedido):
            return False, {'error': 'Order not found.'}
        
        order_info = order.get_alldata_pedido_by_id(idOrder)
        if not order_info:
            return False, {'error': 'Order not found.'}
        
        order_info['productos'] = order_legacyData.get_productos()
        
        return True, {'order': order_info}
    except Exception as e:
        logger.error(f"Error getting order details: {e}")
        return False, {'error': 'Error getting order details1.',
                       'error_detail': str(e),
                       'passtest': passtest}

def man_get_all_orders():
    try:
        logger.info(f"Getting all orders.")
        
        # Obtener pedidos
        order = Pedido()
        orders = order.get_all_pedidos()
        
        if not orders:
            return False, {'error': 'No orders found.'}
        
        return True, {'orders': orders}
    except Exception as e:
        logger.error(f"Error getting all orders: {e}")
        return False, {'error': 'Error getting all orders.',
                       'error_detail': str(e)}

def man_get_user_orders(mailUser):
    try:
        logger.info(f"Getting orders for user: {mailUser}")
        
        # Obtener ID del usuario
        user = UsersModel().get_user_by_email(mailUser)
        if not isinstance(user, UsersModel):
            logger.error(f"User not found.")
            return None, {'error': 'User not found.'}
        
        idUser = user.get_id_user()
        
        # Obtener pedidos del usuario
        order = Pedido()
        orders = order.get_pedidos_by_idUser(idUser)
        
        if not orders:
            return False, {'error': 'No orders found for the user.'}
        
        return True, {'orders': orders}
    except Exception as e:
        logger.error(f"Error getting user orders: {e}")
        return False, {'error': 'Error getting user orders.',
                       'error_detail': str(e)}

def man_add_product_to_order(idOrder, product):
    try:
        logger.debug(f"Adding product to order: {idOrder} product: {product}")
        # Instanciar clase Pedido
        order = Pedido().get_pedido_by_id(idOrder)
        
        logger.debug(f"Order obtained: {order.get_idPedido()}")
        passtest = 1
        if not order:
            return False, {'error': 'Order not found.'}
        
        passtest = 2
        # Agregar producto
        order.add_producto(product['id_producto'], product['cantidad_producto'], product['precio_producto'])
        
        # Guardar pedido
        if not order.guardar_pedido():
            return False, {'error': 'Error adding product to the order.'}
        
        logger.info(f"Product added to order {idOrder} successfully.")
        return True, {'message': 'Product added to order successfully.'}
    except Exception as e:
        logger.error(f"Error adding product to order: {e}")
        return False, {'error': 'Error adding product to the order.',
                       'error_detail': str(e),
                       'passtest': passtest}

def man_remove_product_from_order(idOrder, idProduct):
    try:
        # Instanciar clase Pedido
        order = Pedido()
        order = order.get_pedido_by_id(idOrder)
        
        if not order:
            return False, {'error': 'Order not found.'}

        # Eliminar producto
        order.remove_producto(idProduct)
        
        # Guardar pedido
        if not order.guardar_pedido():
            return False, {'error': 'Error removing product from the order.'}
        
        logger.info(f"Product removed from order {idOrder} successfully.")
        return True, {'message': 'Product removed from order successfully.'}
    except Exception as e:
        logger.error(f"Error removing product from order: {e}")
        return False, {'error': 'Error removing product from the order.',
                       'error_detail': str(e)}

def man_change_product_quantity_from_order(idOrder, idProducto, newQty):
    try:
        # Instanciar clase Pedido
        order = Pedido()
        order = order.get_pedido_by_id(idOrder)
        
        if not order:
            return False, {'error': 'Order not found.'}

        # Cambiar cantidad del producto
        order.change_product_quantity(idProducto, newQty)
        
        # Guardar pedido
        if not order.guardar_pedido():
            return False, {'error': 'Error changing product quantity in the order.'}
        
        logger.info(f"Product quantity changed in order {idOrder} successfully.")
        return True, {'message': 'Product quantity changed in order successfully.'}
    except Exception as e:
        logger.error(f"Error changing product quantity in order: {e}")
        return False, {'error': 'Error changing product quantity in the order.',
                       'error_detail': str(e)}

def man_clear_order(idOrder):
    try:
        # Instanciar clase Pedido
        order = Pedido()
        order = order.get_pedido_by_id(idOrder)
        
        if not order:
            return False, {'error': 'Order not found.'}

        # Limpiar pedido
        order.clear_productos()
        
        # Guardar pedido
        if not order.guardar_pedido():
            return False, {'error': 'Error clearing the order.'}
        
        logger.info(f"Order {idOrder} cleared successfully.")
        return True, {'message': 'Order cleared successfully.'}
    except Exception as e:
        logger.error(f"Error clearing the order: {e}")
        return False, {'error': 'Error clearing the order.',
                       'error_detail': str(e)}

def man_save_order(idOrder):
    try:
        # Instanciar clase Pedido
        order = Pedido()
        order = order.get_pedido_by_id(idOrder)
        
        if not order:
            return False, {'error': 'Order not found.'}
        
        # Guardar pedido
        if not order.guardar_pedido():
            return False, {'error': 'Error saving the order.'}
        
        logger.info(f"Order {idOrder} saved successfully.")
        return True, {'message': 'Order saved successfully.'}
    except Exception as e:
        logger.error(f"Error saving the order: {e}")
        return False, {'error': 'Error saving the order.',
                       'error_detail': str(e)}
        
def man_get_order_states():
    try:
        logger.info(f"Getting order states.")
        
        # Obtener estados de pedido
        states = EstadoPedido().get_estados_pedido()
        
        if not states:
            return False, {'error': 'No order states found.'}
        
        return True, {'states': states}
    except Exception as e:
        logger.error(f"Error getting order states: {e}")
        return False, {'error': 'Error getting order states.',
                       'error_detail': str(e)}