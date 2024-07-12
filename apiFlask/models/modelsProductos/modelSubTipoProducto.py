import logging
from modules.postgres import DBConnection

from models.modelsProductos import TABLA_SUBTIPO_PRODUCTO, TABLA_SUBTIPO_PRODUCTO_COLUMNS
from models.modelsProductos.modelTipoProducto import TipoProducto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

class SubtipoProducto:
    def __init__(self):
        self.idSubtipoProducto = None
        self.nombre = None
        self.tipo = TipoProducto()
    
    # Getters
    def get_idSubtipoProducto(self):
        return self.idSubtipoProducto
    
    def get_nombre(self):
        return self.nombre
    
    def get_tipo(self):
        return self.tipo
    
    # Setters
    def set_idSubtipoProducto(self, idSubtipoProducto):
        self.idSubtipoProducto = idSubtipoProducto
    
    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def set_tipo(self, idTipo):
        try:
            idTipo = int(idTipo)
        except:
            logger.error(f"Error al convertir el ID del tipo de producto a entero.")
            idTipo = None
        
        if idTipo <= 0:
            logger.error(f"ID del tipo de producto inválido.")
            idTipo = None
        
        tipo = TipoProducto().get_tipo_by_id(idTipo)
        if not tipo:
            logger.error(f"Error al obtener el tipo de producto.")
            idTipo = None
        
        if isinstance(tipo, TipoProducto):
            self.tipo = tipo
        else:
            logger.error(f"Error al obtener el tipo de producto.")
            self.tipo = None
    
    def get_subtipos(self, db_conn = DBConnection()):
        """
        Obtiene todos los subtipos de productos de la base de datos.
        
        Returns:
            Una lista de diccionarios con la información de los subtipos de productos.
        """
        try:
            
            # Definir consulta obtener los subtipos de productos
            result = db_conn.select_query(from_table=TABLA_SUBTIPO_PRODUCTO)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los subtipos de productos: {e}")
            return None
    
    def get_subtipos_by_tipo(self, idTipo, db_conn = DBConnection()):
        """
        Obtiene los subtipos de productos de un tipo específico.
        
        Args:
            idTipo (int): El ID del tipo de producto.
        
        Returns:
            Una lista de diccionarios con la información de los subtipos de productos.
        """
        try:
            # Compose function
            where_definition = "id_tipo_producto = %s"
            where_data = (idTipo,)
            
            # Execute query
            result = db_conn.select_query(from_table=TABLA_SUBTIPO_PRODUCTO, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los subtipos de productos: {e}")
            return None
    
    def get_subtipo_by_id(self, idSubtipoProducto, db_conn = DBConnection()):
        """
        Obtiene la información de un subtipo de producto específico.
        
        Args:
            idSubtipoProducto (int): El ID del subtipo de producto a obtener.
        
        Returns:
            Un diccionario con la información del subtipo de producto.
        """
        try:
            # Compose function
            where_definition = "id_subtipo_producto = %s"
            where_data = (idSubtipoProducto,)
            
            # Execute query
            result = db_conn.select_query(from_table=TABLA_SUBTIPO_PRODUCTO, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return None
            
            # Procesar el resultado
            data = result[0]
            self.set_idSubtipoProducto(data['id_subtipo_producto'])
            self.set_nombre(data['nombre_subtipo_producto'])
            self.set_tipo(data['id_tipo_producto'])
            
            return self
                
        except Exception as e:
            logger.error(f"Error al obtener el subtipo de producto: {e}")
            return None
    
    def get_subtipo_by_name(self, nombreSubtipo, db_conn = DBConnection()):
        """
        Obtiene la información de un subtipo de producto específico por su nombre.
        
        Args:
            nombreSubtipo (str): El nombre del subtipo de producto a obtener.
        
        Returns:
            Un diccionario con la información del subtipo de producto.
        """
        try:
            # Compose function
            where_definition = "nombre_subtipo_producto = %s"
            where_data = (nombreSubtipo,)
            
            # Execute query
            result = db_conn.select_query(from_table=TABLA_SUBTIPO_PRODUCTO, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return None
            
            # Procesar el resultado
            data = result[0]
            self.set_idSubtipoProducto(data['id_subtipo_producto'])
            self.set_nombre(data['nombre_subtipo_producto'])
            self.set_tipo(data['id_tipo_producto'])
            
            return self
            
        except Exception as e:
            logger.error(f"Error al obtener el subtipo de producto: {e}")
            return None
        
    def insert_subtipo(self, db_conn = DBConnection()):
        """
        Inserta un nuevo subtipo de producto en la base de datos.
        
        Returns:
            True si el subtipo de producto se insertó correctamente, False en caso contrario.
        """
        
        # Comprobar si el subtipo de producto ya existe
        subtipo = SubtipoProducto().get_subtipo_by_name(self.nombre)
        if subtipo:
            logger.error(f"El subtipo de producto ya existe.")
            return False
        
        # Comprobar si el tipo de producto existe
        if not isinstance(self.tipo, TipoProducto):
            logger.error(f"El tipo de producto no es válido.")
            return False
        
        try:
            # Definir consulta insertar
            insert_values = [
                self.get_nombre(),
                self.get_tipo().get_idTipoProducto()
            ]
            
            insert_returning = ['id_subtipo_producto']
            
            # Insert Query
            result = db_conn.insert_query(table=TABLA_SUBTIPO_PRODUCTO, columns=TABLA_SUBTIPO_PRODUCTO_COLUMNS[1:], values=insert_values, returnData=True, returnColumns=insert_returning)
            if not result:
                return False
            
            self.idSubtipoProducto = result[0][0]
            
            return True
        
        except Exception as e:
            logger.error(f"Error al insertar el subtipo de producto: {e}")
            return False
