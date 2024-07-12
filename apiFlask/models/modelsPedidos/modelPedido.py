import logging
import json
import datetime
from modules.postgres import DBConnection

from models.modelsPedidos.modelEstadoPedido import EstadoPedido
from models.modelsPedidos import TABLA_PEDIDO_PRODUCTO, TABLA_PEDIDO_PRODUCTO_COLUMNS
from models.modelsPedidos import TABLA_PEDIDOS, TABLA_PEDIDOS_COLUMNS
from models.modelsPedidos import VISTA_PEDIDO_PRODUCTO, VISTA_PEDIDO_PRODUCTO_COLUMNS
from models.modelsPedidos import VISTA_PEDIDO, VISTA_PEDIDO_COLUMNS

# Logger
logger = logging.getLogger(__name__)

class Pedido:
    def __init__(self):
        self.idPedido = None
        self.idUser = None
        self.fechaPedido = None
        self.totalPedido = 0.0
        self.estadoPedido = EstadoPedido()
        self.productos = []
    
    # Getters
    def get_idPedido(self):
        return self.idPedido
    
    def get_idUser(self):
        return self.idUser
    
    def get_fechaPedido(self):
        return self.fechaPedido
    
    def get_totalPedido(self):
        return self.totalPedido
    
    def get_estadoPedido(self):
        return self.estadoPedido
    
    def get_productos(self):
        return self.productos
    
    # Setters
    def set_idPedido(self, idPedido):
        try:
            idPedido = int(idPedido)
        except:
            logger.error(f"Error al convertir el ID del pedido a entero.")
            idPedido = None
        
        if idPedido <= 0:
            logger.error(f"ID del pedido inválido.")
            idPedido = None
            
        self.idPedido = idPedido
    
    def set_idUser(self, idUser):
        try:
            idUser = int(idUser)
        except:
            logger.error(f"Error al convertir el ID del usuario a entero.")
            idUser = None
        
        if idUser <= 0:
            logger.error(f"ID del usuario inválido.")
            idUser = None
            
        self.idUser = idUser
    
    def set_fechaPedido(self, fechaPedido):
        if isinstance(fechaPedido, datetime.datetime):
            self.fechaPedido = fechaPedido
        else:
            logger.error(f"Fecha de pedido inválida.")

    def set_totalPedido(self, totalPedido):
        try:
            totalPedido = float(totalPedido)
        except:
            logger.error(f"Error al convertir el total del pedido a flotante.")
            totalPedido = None
        
        if totalPedido < 0:
            logger.error(f"Total del pedido inválido.")
            totalPedido = None
            
        self.totalPedido = totalPedido
    
    def set_estadoPedido(self, estadoPedido):
        if isinstance(estadoPedido, EstadoPedido):
            self.estadoPedido = estadoPedido
    
    def set_productos(self, productos):
        if not isinstance(productos, list):
            logger.error(f"Productos inválidos.")
            productos = None
        
        for producto in productos:
            if not isinstance(producto, dict):
                logger.error(f"Producto inválido.")
                productos = None
                break
            if 'id_producto' not in producto or 'cantidad_producto' not in producto or 'precio_producto' not in producto:
                logger.error(f"Producto inválido.")
                productos = None
                break
            try:
                producto['id_producto'] = int(producto['id_producto'])
                producto['cantidad_producto'] = int(producto['cantidad_producto'])
                producto['precio_producto'] = float(producto['precio_producto'])
                if producto['id_producto'] <= 0 or producto['cantidad_producto'] <= 0:
                    raise ValueError("Producto inválido.")
            except Exception as e:
                logger.error(f"Error al convertir los datos del producto: {e}")
                productos = None
                break
            
        self.productos = productos
    
    # Métodos
    def to_json(self):
        return {
            'idPedido': self.get_idPedido(),
            'idUser': self.get_idUser(),
            'fechaPedido': self.get_fechaPedido(),
            'totalPedido': self.get_totalPedido(),
            'estadoPedido': self.get_estadoPedido().to_json(),
            'productos': self.get_productos()
        }
    
    def add_total(self, total):
        if total > 0:
            self.totalPedido += total
        else:
            logger.error(f"Total inválido.")
    
    def minus_total(self, total):
        if total > 0:
            self.totalPedido -= total
        else:
            logger.error(f"Total inválido.")
    
    def recalcular_total(self):
        self.totalPedido = 0.0
        for producto in self.productos:
            self.add_total(producto['cantidad_producto'] * producto['precio_producto'])
    
    def add_producto(self, id_producto, cantidad, precio):
        try:
            id_producto = int(id_producto)
            cantidad = int(cantidad)
            precio = float(precio)
            if cantidad <= 0 or precio < 0:
                raise ValueError("Cantidad o precio inválido.")
        except Exception as e:
            logger.error(f"Error al agregar producto: {e}")
            return False
        
        producto = {
            'id_producto': id_producto,
            'cantidad_producto': cantidad,
            'precio_producto': precio
        }
        
        logger.debug(f"Productos antes de agregar: {self.productos}")
        self.productos.append(producto)
        logger.debug(f"Productos después de agregar: {self.productos}")
        
        self.add_total(cantidad * precio)
        return True
    
    def remove_producto(self, id_producto):
        for producto in self.productos:
            if producto['id_producto'] == id_producto:
                self.minus_total(producto['cantidad_producto'] * producto['precio_producto'])
                self.productos.remove(producto)
                return True
        logger.error(f"Producto con id {id_producto} no encontrado.")
        return False
    
    def set_estado(self, nuevo_estado):
        if isinstance(nuevo_estado, EstadoPedido):
            self.estadoPedido = nuevo_estado
        else:
            logger.error(f"Estado del pedido inválido.")
    
    def change_product_quantity(self, idProducto, newQty):
        for producto in self.productos:
            if producto['id_producto'] == idProducto:
                oldQty = producto['cantidad_producto']
                oldPrice = producto['precio_producto']
                self.minus_total(oldQty * oldPrice)
                producto['cantidad_producto'] = newQty
                self.add_total(newQty * oldPrice)
                self.guardar_pedido()
                return True
        logger.error(f"Producto con id {idProducto} no encontrado.")
        return False

    def guardar_pedido(self, db_conn = DBConnection()):
        
        # Asegurar total del pedido
        self.recalcular_total()
        
        if self.idPedido is None:
            values = [
                self.idUser,
                self.fechaPedido,
                self.totalPedido,
                self.estadoPedido.idEstadoPedido
            ]
            result = db_conn.insert_query(table=TABLA_PEDIDOS, columns=TABLA_PEDIDOS_COLUMNS[1:], values=values, returnData=True, returnColumns=['id_pedido'])
            if not result:
                return False
            
            self.idPedido = result[0][0]
            return self.guardar_productos(db_conn)
        else:
            values = [
                self.idUser,
                self.fechaPedido,
                self.totalPedido,
                self.estadoPedido.idEstadoPedido,
                self.idPedido
            ]
            result = db_conn.update_query(table=TABLA_PEDIDOS, set_columns=TABLA_PEDIDOS_COLUMNS[1:], set_values=values, where_condition="id_pedido = %s", where_params=(self.idPedido,))
            if not result:
                return False
            return self.guardar_productos(db_conn)

    def guardar_productos(self, db_conn = DBConnection()):
        db_conn.execute_commit_query(f"DELETE FROM {TABLA_PEDIDO_PRODUCTO} WHERE id_pedido = %s;", (self.idPedido,))

        for producto in self.productos:
            values = [
                self.idPedido,
                producto['id_producto'],
                producto['cantidad_producto'],
                producto['precio_producto']
            ]
            result = db_conn.insert_query(table=TABLA_PEDIDO_PRODUCTO, columns=TABLA_PEDIDO_PRODUCTO_COLUMNS[1:], values=values)
            if not result:
                return False
        
        return True
    
    def get_all_pedidos(self, db_conn = DBConnection()):
        try:
            result = db_conn.select_query(from_table=VISTA_PEDIDO)
            if not result:
                return None
            
            return result
        except Exception as e:
            logger.error(f"Error al obtener los pedidos: {e}")
            return None
    
    def get_alldata_pedido_by_id(self, idPedido, db_conn = DBConnection()):
        try:
            idPedido = int(idPedido)
        except:
            logger.error(f"Error al convertir el ID del pedido a entero.")
            return None
        
        if idPedido <= 0:
            logger.error(f"ID del pedido inválido.")
            return None
        
        try:
            result = db_conn.select_query(from_table=VISTA_PEDIDO, where_condition="id_pedido = %s", where_params=(idPedido,))
            if not result:
                return None
            
            return result[0]
        except Exception as e:
            logger.error(f"Error al obtener el pedido: {e}")
            return None
    
    def get_pedidos_by_idUser(self, idUser, db_conn = DBConnection()):
        try:
            idUser = int(idUser)
        except:
            logger.error(f"Error al convertir el ID del usuario a entero.")
            return None
        
        if idUser <= 0:
            logger.error(f"ID del usuario inválido.")
            return None
        
        try:
            result = db_conn.select_query(from_table=TABLA_PEDIDOS, where_condition="id_user = %s", where_params=(idUser,))
            if not result:
                return None
            
            pedidos = []
            for row in result:
                pedido = self.get_pedido_by_id(row['id_pedido'])
                pedidos.append(pedido.to_json())
            
            return pedidos
        except Exception as e:
            logger.error(f"Error al obtener los pedidos: {e}")
            return None
    
    def get_pedido_by_id(self, idPedido, db_conn = DBConnection()):
        try:
            idPedido = int(idPedido)
        except:
            logger.error(f"Error al convertir el ID del pedido a entero.")
            return None
        
        if idPedido <= 0:
            logger.error(f"ID del pedido inválido.")
            return None
        
        try:
            result = db_conn.select_query(from_table=TABLA_PEDIDOS, where_condition="id_pedido = %s", where_params=(idPedido,))
            if not result:
                return None
            
            # Configurar pedido
            self.set_idPedido(result[0]['id_pedido'])
            self.set_idUser(result[0]['id_user'])
            self.set_fechaPedido(datetime.datetime.strptime(result[0]['fecha_pedido'], '%Y-%m-%dT%H:%M:%S.%f'))
            self.set_totalPedido(result[0]['total_pedido'])
            self.set_estadoPedido(EstadoPedido().get_estado_pedido_by_id(result[0]['id_estado_pedido']))
            
            # Cargar productos del pedido
            result = db_conn.select_query(from_table=VISTA_PEDIDO_PRODUCTO, where_condition="id_pedido = %s", where_params=(idPedido,))
            if result:
                for row in result:
                    producto = {
                        'id_producto': row['id_producto'],
                        'nombre_producto': row['nombre_producto'], # 'nombre_producto' es un campo de la vista
                        'cantidad_producto': row['cantidad_producto'],
                        'precio_producto': row['precio_producto']
                    }
                    self.productos.append(producto)
            else:
                self.productos = []
            
            return self
        except Exception as e:
            logger.error(f"Error al obtener el pedido: {e}")
            return None
    
    def get_carrito_by_idUser(self, idUser, db_conn = DBConnection()):
        try:
            idUser = int(idUser)
        except:
            logger.error(f"Error al convertir el ID del usuario a entero.")
            return None
        
        if idUser <= 0:
            logger.error(f"ID del usuario inválido.")
            return None
        
        try:
            result = db_conn.select_query(from_table=TABLA_PEDIDOS, where_condition="id_user = %s AND id_estado_pedido = %s", where_params=(idUser,1))
            if not result:
                return None
            
            # Configurar pedido
            self.set_idPedido(result[0]['id_pedido'])
            self.set_idUser(result[0]['id_user'])
            self.set_fechaPedido(datetime.datetime.strptime(result[0]['fecha_pedido'], '%Y-%m-%dT%H:%M:%S.%f'))
            self.set_totalPedido(result[0]['total_pedido'])
            self.set_estadoPedido(EstadoPedido().get_estado_pedido_by_id(result[0]['id_estado_pedido']))
            
            # Cargar productos del pedido
            result = db_conn.select_query(from_table=VISTA_PEDIDO_PRODUCTO, where_condition="id_pedido = %s", where_params=(self.get_idPedido(),))
            if not result:
                logger.debug(f"No hay productos en el carrito.")
                result = []
            
            for row in result:
                producto = {
                    'id_producto': row['id_producto'],
                    'nombre_producto': row['nombre_producto'], # 'nombre_producto' es un campo de la vista
                    'cantidad_producto': row['cantidad_producto'],
                    'precio_producto': row['precio_producto']
                }
                self.productos.append(producto)
            
            return self
        except Exception as e:
            logger.error(f"Error al obtener los pedidos: {e}")
            return None
    
    def clear_productos(self):
        self.productos = []
        self.totalPedido = 0.0
        return True
    
    ## FIX: Actualizar el precio de los productos en todos los pedidos con id_estado_pedido especificado
    def update_product_price(self, id_producto, new_price, id_estado, db_conn = DBConnection()):
        try:
            id_producto = int(id_producto)
            new_price = float(new_price)
            if new_price < 0:
                raise ValueError("Precio inválido.")
        except Exception as e:
            logger.error(f"Error al actualizar precio: {e}")
            return False
        
        # Validar id_estado
        estadoInput = EstadoPedido().get_estado_pedido_by_id(id_estado)
        if not isinstance(estadoInput, EstadoPedido):
            logger.error(f"Estado inválido.")
            return False
        
        where_definition = "id_estado_pedido = %s AND id_producto = %s"
        where_data = (id_estado, id_producto)
        
        # Obtener los pedidos con el id_estado especificado
        result = db_conn.select_query(from_table=VISTA_PEDIDO_PRODUCTO, where_condition=where_definition, where_params=where_data)
        if not result:
            return False
        
        pedidos_to_change = {row['id_pedido'] for row in result}
        
        # Actualizar el precio del producto en los pedidos
        for id_pedido in pedidos_to_change:
            where_definition = "id_pedido = %s AND id_producto = %s"
            where_data = (id_pedido, id_producto)
            set_definition = ["precio_producto"]
            set_data = [new_price]
            
            result = db_conn.update_query(table=TABLA_PEDIDO_PRODUCTO, set_columns=set_definition, set_values=set_data, where_condition=where_definition, where_params=where_data)
            if not result:
                return False
        
        return True