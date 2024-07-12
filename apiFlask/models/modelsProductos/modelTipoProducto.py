import logging
from modules.postgres import DBConnection

from models.modelsProductos import TABLA_TIPO_PRODUCTO, TABLA_TIPO_PRODUCTO_COLUMNS

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

class TipoProducto:
    def __init__(self):
        self.idTipoProducto = None
        self.nombre = None
    
    # Getters
    def get_idTipoProducto(self):
        return self.idTipoProducto
    
    def get_nombre(self):
        return self.nombre
    
    # Setters
    def set_idTipoProducto(self, idTipoProducto):
        try:
            idTipoProducto = int(idTipoProducto)
        except:
            logger.error(f"Error al convertir el ID del tipo de producto a entero.")
            idTipoProducto = None
            
        if idTipoProducto <= 0:
            logger.error(f"ID del tipo de producto inválido.")
            idTipoProducto = None
            
        self.idTipoProducto = idTipoProducto
    
    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def get_tipos(self, db_conn = DBConnection()):
        """
        Obtiene todos los tipos de productos de la base de datos.
        
        Returns:
            Una lista de diccionarios con la información de los tipos de productos.
        """
        try:
            # Definir consulta obtener los tipos de productos
            result = db_conn.select_query(from_table=TABLA_TIPO_PRODUCTO)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los tipos de productos: {e}")
            return None
    
    def get_tipo_by_id(self, idTipoProducto, db_conn = DBConnection()):
        """
        Obtiene la información de un tipo de producto específico.
        
        Args:
            idTipoProducto (int): El ID del tipo de producto a obtener.
        
        Returns:
            Un diccionario con la información del tipo de producto.
        """
        try:
            # Definir consulta obtener el tipo de producto
            where_definition = "id_tipo_producto = %s"
            where_data = (idTipoProducto,)
            result = db_conn.select_query(from_table=TABLA_TIPO_PRODUCTO, where_condition=where_definition, where_params=where_data)
            if not result:
                return None
            
            # Procesar el resultado
            data = result[0]
            self.set_idTipoProducto(data['id_tipo_producto'])
            self.set_nombre(data['nombre_tipo_producto'])
            
            return self
                
        except Exception as e:
            logger.error(f"Error al obtener el tipo de producto: {e}")
            return None
    
    def get_tipo_by_name(self, nombreTipo, db_conn = DBConnection()):
        """
        Obtiene la información de un tipo de producto específico por su nombre.
        
        Args:
            nombreTipo (str): El nombre del tipo de producto a obtener.
        
        Returns:
            Un diccionario con la información del tipo de producto.
        """
        try:
            # Definir consulta obtener el tipo de producto
            where_definition = "nombre_tipo_producto = %s"
            where_data = (nombreTipo,)
            result = db_conn.select_query(from_table=TABLA_TIPO_PRODUCTO, where_condition=where_definition, where_params=where_data)
            if not result:
                return None
            
            # Procesar el resultado
            data = result[0]
            self.set_idTipoProducto(data['id_tipo_producto'])
            self.set_nombre(data['nombre_tipo_producto'])
            
            return self
            
        except Exception as e:
            logger.error(f"Error al obtener el tipo de producto: {e}")
            return None
    
    def insert_tipo(self, db_conn = DBConnection()):
        """
        Inserta un nuevo tipo de producto en la base de datos.
        
        Returns:
            True si el tipo de producto se insertó correctamente, False en caso contrario.
        """
        
        # Comprobar si el tipo de producto ya existe
        tipo = TipoProducto().get_tipo_by_name(self.nombre)
        if tipo:
            logger.error(f"El tipo de producto ya existe.")
            return False
        
        try:
            # Definir consulta insertar
            insert_values = [
                self.get_nombre()
            ]
            
            insert_returning = ['id_tipo_producto']
            
            # Ejecutar la consulta
            result = db_conn.insert_query(table=TABLA_TIPO_PRODUCTO, columns=TABLA_TIPO_PRODUCTO_COLUMNS[1:], values=insert_values, returnData=True, returnColumns=insert_returning)
            if not result:
                return False
            
            self.set_idTipoProducto(result[0][0])
            
            return True
        except Exception as e:
            logger.error(f"Error al insertar el tipo de producto: {e}")
            return False
