import logging
import datetime
from modules.postgres import DBConnection

#from models.modelsProductos.modelProducto import Producto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

# Definir las tablas de la base de datos
from models.modelsProductos import TABLA_PRECIO, TABLA_PRECIO_COLUMNS

class PrecioProducto:
    def __init__(self):
        self.idPrecioProducto = None
        self.idProducto = None
        self.precio = None
        self.fecha = None
    
    # Getters
    def get_idPrecioProducto(self):
        return self.idPrecioProducto
    
    def get_idProducto(self):
        return self.idProducto
    
    def get_precio(self):
        return self.precio
    
    def get_fecha(self):
        return self.fecha
    
    def to_json(self):
        return {
            'idPrecioProducto': self.idPrecioProducto,
            'idProducto': self.idProducto,
            'precio': self.precio,
            'fecha': self.fecha
        }
    
    # Setters
    def set_idProducto(self, idProducto):
        try:
            idProducto = int(idProducto)
        except:
            logger.error(f"Error al convertir el ID del producto a entero.")
            idProducto = None
        
        if idProducto <= 0:
            logger.error(f"ID del producto inválido.")
            idProducto = None
        
        self.idProducto = idProducto
    
    def set_precionew(self, precio):
        try:
            precio = float(precio)
        except:
            logger.error(f"Error al convertir el precio a flotante.")
            precio = None
        
        if precio <= 0:
            logger.error(f"Precio inválido.")
            precio = None
        
        # Get fecha cambio precio
        fecha = datetime.datetime.now()
        
        # Set parameters
        self.precio = precio
        self.fecha = fecha
    
    # Métodos
    
    def get_latest_precio_by_productid(self, id_producto):
        """
        Obtiene el último precio de un producto específico.
        
        Args:
            id_producto (int): El ID del producto.
        
        Returns:
            Clase PrecioProducto con la información del último precio.
        """
        try:
            # Obtener la conexión a la base de datos
            db_connection = DBConnection()
            
            # Definir parametros de la consulta
            orderDesc = "fecha_precio_producto"
            where_definition = "id_producto = %s"
            where_data = (id_producto,)
            queryLimit = 1
            
            # Ejecutar la consulta
            result = db_connection.select_query(from_table=TABLA_PRECIO, where_condition=where_definition, where_params=where_data, order_desc=orderDesc, limit=queryLimit)
            if not result:
                return None
            
            # Procesar el resultado
            data = result[0]
            self.idPrecioProducto = data['id_precio_producto']
            self.idProducto = data['id_producto']
            self.precio = data['precio_producto']
            self.fecha = data['fecha_precio_producto']
            
            return self
        except Exception as e:
            logger.error(f"Error al obtener el último precio del producto: {e}")
            return None
    
    def get_precios_history(self):
        """
        Obtiene el historial de precios de un producto.
        
        Returns:
            Una lista de diccionarios con la información de los precios.
        """
        try:
            # Obtener la conexión a la base de datos
            db_connection = DBConnection()
            
            # Definir parametros de la consulta
            where_definition = "id_producto = %s"
            where_data = (self.idProducto,)
            
            # Ejecutar la consulta
            result = db_connection.select_query(from_table=TABLA_PRECIO, where_condition=where_definition, where_params=where_data)
            if not result:
                return None
            
            return result
        except Exception as e:
            logger.error(f"Error al obtener los precios: {e}")
            return None
    
    def insert_precio(self):
        """
        Inserta un nuevo precio de producto en la base de datos.
        
        Returns:
            True si el precio de producto se insertó correctamente, False en caso contrario.
        """
        try:
            # Obtener la conexión a la base de datos
            db_connection = DBConnection()
            
            # Compose Function
            insert_values = [
                self.idProducto,
                self.precio,
                self.fecha
            ]
            insert_returning = ['id_precio_producto']
            
            # Insert Query
            result = db_connection.insert_query(table=TABLA_PRECIO, columns=TABLA_PRECIO_COLUMNS[1:], values=insert_values, returnData=True, returnColumns=insert_returning)
            if not result:
                return False
            
            self.idPrecioProducto = result[0][0]
            
            return True
        except Exception as e:
            logger.error(f"Error al insertar el precio de producto: {e}")
            return False
        
    