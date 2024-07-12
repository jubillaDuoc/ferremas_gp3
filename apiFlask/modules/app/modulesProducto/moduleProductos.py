import logging

from models.modelsProductos.modelProducto import Producto
from models.modelsProductos.modelSubTipoProducto import SubtipoProducto
from models.modelsProductos.modelMarcaProducto import MarcaProducto
from models.modelsPedidos.modelPedido import Pedido

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def man_create_producto(nombre_producto, stock_producto, id_marca, id_subtipo, precio_producto):
    try:
        logger.info(f"Creando producto: {nombre_producto}")
        
        # Instanciar clase Producto
        producto = Producto()
        
        # Obtener Marca del producto
        marca = MarcaProducto().get_marca_by_id(id_marca)
        if not isinstance(marca, MarcaProducto):
            logger.error(f"La marca de producto no existe.")
            return None , {'error': 'La marca de producto no existe.'}
        
        # Obtener Subtipo del producto
        subtipo = SubtipoProducto().get_subtipo_by_id(id_subtipo)
        if not isinstance(subtipo, SubtipoProducto):
            logger.error(f"El subtipo de producto no existe.")
            return None , {'error': 'El subtipo de producto no existe.'}
        
        # Configurar producto
        producto.set_nombre(nombre_producto)
        producto.set_stock(stock_producto)
        producto.set_marca(marca)
        producto.set_subtipo(subtipo)
        
        # Guardar producto
        saveProduct = producto.insert_producto()
        
        if not saveProduct:
            logger.error(f"Error al guardar el producto.")
            return False, {'error': 'Error al guardar el producto.'}
        
        logger.info(f"Producto guardado exitosamente.")
        
        if not isinstance(producto.get_idProducto(), int):
            logger.error(f"Error al guardar el producto.")
            return False, {'error': 'Error al guardar el producto.'}
        
        logger.info(f"Producto guardado exitosamente.")
        
        #Check Precio
        try:
            precio_producto = float(precio_producto)
        except Exception as e:
            logger.error(f"Precio inválido.")
            return False, {'error': 'Precio inválido.'}
        
        if not isinstance(precio_producto, float) or precio_producto < 0:
            logger.error(f"Precio inválido.")
            return False, {'error': 'Precio inválido.'}
        
        logger.info(f"Precio válido.")
        
        # Guardar precio
        savePrice = producto.set_newprecio(precio_producto)
        if not savePrice:
            logger.error(f"Error al guardar el precio del producto1.")
            return False, {'error': 'Error al guardar el precio del producto.'}
        
        logger.info(f"Precio guardado exitosamente.")
        
        if not isinstance(producto.get_precio().get_idPrecioProducto(), int):
            logger.error(f"Error al guardar el precio del producto2.")
            return False, {'error': 'Error al guardar el precio del producto.'}      
        
        logger.info(f"Precio guardado exitosamente.")
        
        # Clear producto
        producto = None
        logger.debug(f"Producto limpiado.")
        
        # Devolver la respuesta
        logger.info(f"Producto {nombre_producto} creado exitosamente.")
        return True, {'message': 'Producto creado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para crear un producto
        logger.error(f"Error al procesar solicitud para crear un producto: {e}")
        return False, {'error': 'Error al crear el producto.',
                       'error_detail': str(e)}

def man_update_producto(id_producto, nombre_producto, id_marca, id_subtipo, precio_producto, stock_producto):
    try:
        # Instanciar clase Producto
        producto = Producto()
        
        # Configurar producto
        producto.get_producto_by_id(id_producto)
        producto.set_nombre(nombre_producto)
        
        # Obtener Marca del producto
        marca = MarcaProducto().get_marca_by_id(id_marca)
        if not isinstance(marca, MarcaProducto):
            logger.error(f"La marca de producto no existe.")
            return None , {'error': 'La marca de producto no existe.'}
        
        # Obtener Subtipo del producto
        subtipo = SubtipoProducto().get_subtipo_by_id(id_subtipo)
        if not isinstance(subtipo, SubtipoProducto):
            logger.error(f"El subtipo de producto no existe.")
            return None , {'error': 'El subtipo de producto no existe.'}
        
        producto.set_marca(marca)
        producto.set_subtipo(subtipo)
        producto.set_stock(stock_producto)
        
        # Actualizar producto
        check_update = producto.update_producto()
        if not check_update:
            return False, {'error': 'Error al actualizar el producto.'}
        
        # Actualizar precio
        check_update = producto.set_newprecio(precio_producto)
        if not check_update:
            return False, {'error': 'Error al actualizar el precio del producto.'}
        
        ### FIX: Actualizar precio en los pedidos tomados por el usuario id_estado_pedido=1
        check_update = Pedido().update_product_price(id_producto, precio_producto, 1)
        if not check_update:
            return False, {'error': 'Error al actualizar el precio del producto en los pedidos.'}
        
        # Devolver la respuesta
        logger.info(f"Producto {nombre_producto} actualizado exitosamente.")
        return True, {'message': 'Producto actualizado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para actualizar un producto
        logger.error(f"Error al procesar solicitud para actualizar un producto: {e}")
        return False, {'error': 'Error al actualizar el producto.',
                       'error_detail': str(e)}

def man_update_stock_producto(id_producto, stock):
    try:
        # Instanciar clase Producto
        producto = Producto()
        
        # Configurar producto
        producto.get_producto_by_id(id_producto)
        producto.set_stock(stock)
        
        # Actualizar producto
        check_update = producto.update_producto()
        if not check_update:
            return False, {'error': 'Error al actualizar el stock del producto.'}
        
        # Devolver la respuesta
        logger.info(f"Stock del producto {id_producto} actualizado exitosamente.")
        return True, {'message': 'Stock actualizado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para actualizar stock de un producto
        logger.error(f"Error al procesar solicitud para actualizar stock de un producto: {e}")
        return False, {'error': 'Error al actualizar el stock del producto.',
                       'error_detail': str(e)}

def man_get_productos():
    try:
        logger.info(f"Obteniendo productos.")
        # Obtener productos
        productos_list = Producto().get_productos()
        if not productos_list:
            return False, {'error': 'Error al obtener los prod.'}
        
        # Devolver la respuesta
        return True, {'productos': productos_list}
    except Exception as e:
        # Error al procesar la solicitud para obtener productos
        logger.error(f"Error al procesar solicitud para obtener productos: {e}")
        return False, {'error': 'Error al obtener los prod.',
                       'error_detail': str(e)}
        
def man_get_producto_by_id(id_producto):
    try:
        logger.info(f"Obteniendo producto por id: {id_producto}")
        
        # Obtener productos
        productDetail = Producto().get_producto_by_id(id_producto).to_json()
        if not productDetail:
            return False, {'error': 'Error al obtener el prod.'}
        
        # Procesar el resultado
        return True, {'producto': productDetail}
    except Exception as e:
        # Error al procesar la solicitud para obtener producto
        logger.error(f"Error al procesar solicitud para obtener producto: {e}")
        return False, {'error': 'Error al obtener el producto.1',
                       'error_detail': str(e)}
        
def man_get_productos_by_marca(id_marca):
    try:
        logger.info(f"Obteniendo productos por marca.")
        # Obtener productos
        productos_list = Producto().get_productos_by_marca(id_marca)
        if not productos_list:
            return False, {'error': 'Error al obtener los prod.'}
        
        # Devolver la respuesta
        return True, {'productos': productos_list}
    except Exception as e:
        # Error al procesar la solicitud para obtener productos
        logger.error(f"Error al procesar solicitud para obtener productos: {e}")
        return False, {'error': 'Error al obtener los prod.',
                       'error_detail': str(e)}
        
def man_get_productos_by_tipo(id_tipo):
    try:
        logger.info(f"Obteniendo productos por tipo.")
        
        # Obtener productos
        productos_list = Producto().get_productos_by_tipo(id_tipo)
        if not productos_list:
            return False, {'error': 'Error al obtener los prod.'}
        
        # Devolver la respuesta
        return True, {'productos': productos_list}
    except Exception as e:
        # Error al procesar la solicitud para obtener productos
        logger.error(f"Error al procesar solicitud para obtener productos: {e}")
        return False, {'error': 'Error al obtener los prod.',
                       'error_detail': str(e)}
        
def man_get_productos_by_subtipo(id_subtipo):
    try:
        logger.info(f"Obteniendo productos por subtipo.")
        
        # Obtener productos
        productos_list = Producto().get_productos_by_subtipo(id_subtipo)
        if not productos_list:
            return False, {'error': 'Error al obtener los prod.'}
        
        # Devolver la respuesta
        return True, {'productos': productos_list}
    except Exception as e:
        # Error al procesar la solicitud para obtener productos
        logger.error(f"Error al procesar solicitud para obtener productos: {e}")
        return False, {'error': 'Error al obtener los prod.',
                       'error_detail': str(e)}

def man_update_precio_producto(id_producto, precio):
    try:
        # Instanciar clase Producto
        producto = Producto()
        
        # Configurar producto
        producto.get_producto_by_id(id_producto)
        check_update = producto.set_newprecio(precio)
        if not check_update:
            return False, {'error': 'Error al actualizar el precio del producto.'}
        
        # Devolver la respuesta
        logger.info(f"Precio del producto {id_producto} actualizado exitosamente.")
        return True, {'message': 'Precio actualizado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para actualizar precio de un producto
        logger.error(f"Error al procesar solicitud para actualizar precio de un producto: {e}")
        return False, {'error': 'Error al actualizar el precio del producto.',
                       'error_detail': str(e)}