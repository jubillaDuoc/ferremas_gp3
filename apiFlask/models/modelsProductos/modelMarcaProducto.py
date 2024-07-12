import logging
from modules.postgres import DBConnection

from models.modelsProductos import TABLA_MARCA_PRODUCTO, TABLA_MARCA_PRODUCTO_COLUMNS

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

class MarcaProducto:
    def __init__(self):
        self.idMarcaProducto = None
        self.nombre = None
    
    # Getters
    def get_idMarcaProducto(self):
        return self.idMarcaProducto
    
    def get_nombre(self):
        return self.nombre
    
    # Setters
    def set_idMarcaProducto(self, idMarcaProducto):
        try:
            idMarcaProducto = int(idMarcaProducto)
        except:
            logger.error(f"Error al convertir el ID de la marca de producto a entero.")
            idMarcaProducto = None
        
        if idMarcaProducto <= 0:
            logger.error(f"ID de la marca de producto inválido.")
            idMarcaProducto = None
        
        self.idMarcaProducto = idMarcaProducto
    
    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def get_marcas(self, db_conn = DBConnection()):
        """
        Obtiene todas las marcas de productos de la base de datos.
        
        Returns:
            Una lista de diccionarios con la información de las marcas de productos.
        """
        try:
            # Definir consulta obtener las marcas de productos
            result = db_conn.select_query(from_table=TABLA_MARCA_PRODUCTO)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener las marcas de productos: {e}")
            return None
    
    def get_marca_by_id(self, idMarcaProducto, db_conn = DBConnection()):
        """
        Obtiene la información de una marca de producto específica por su ID.
        
        Args:
            idMarcaProducto (int): El ID de la marca de producto a obtener.
        
        Returns:
            Un diccionario con la información de la marca de producto.
        """
        try:
            # Query the database
            where_definition = "id_marca_producto = %s"
            where_data = (idMarcaProducto,)
            result = db_conn.select_query(from_table=TABLA_MARCA_PRODUCTO, where_condition=where_definition, where_params=where_data)
            if not result:
                logger.error(f"La marca de producto no existe.")
                return None , {'error': 'La marca de producto no existe.'}
            
            logger.info(f"Marca de producto encontrada.")
            
            # Process the query result
            data = result[0]
            self.set_idMarcaProducto(data['id_marca_producto'])
            self.set_nombre(data['nombre_marca_producto'])
            
            return self
            
        except Exception as e:
            logger.error(f"Error al obtener la marca de producto: {e}")
            return None
    
    def get_marca_by_name(self, nombreMarca, db_conn = DBConnection()):
        """
        Obtiene la información de una marca de producto específica por su nombre.
        
        Args:
            nombreMarca (str): El nombre de la marca de producto a obtener.
        
        Returns:
            Un diccionario con la información de la marca de producto.
        """
        try:
            # Query the database for the user role
            where_definition = "nombre_marca_producto = %s"
            where_data = (nombreMarca,)
            result = db_conn.select_query(from_table=TABLA_MARCA_PRODUCTO, where_condition=where_definition, where_params=where_data)
            if not result:
                logger.error(f"La marca de producto no existe.")
                return None , {'error': 'La marca de producto no existe.'}
            
            logger.info(f"Marca de producto encontrada.")
            
            # Process the query result
            data = result[0]
            self.set_idMarcaProducto(data['id_marca_producto'])
            self.set_nombre(data['nombre_marca_producto'])
            
            return self
            
        except Exception as e:
            logger.error(f"Error al obtener la marca de producto: {e}")
            return None
    
    def insert_marca(self, db_conn = DBConnection()):
        """
        Inserta una nueva marca de producto en la base de datos.
        
        Returns:
            True si la marca de producto se insertó correctamente, False en caso contrario.
        """
        
        # Comprobar si la marca de producto ya existe
        marca = MarcaProducto().get_marca_by_name(self.nombre)
        if marca:
            logger.error(f"La marca de producto ya existe.")
            return False
                
        try:
            # Definir consulta insertar
            insert_values = [
                self.get_nombre()
            ]
            
            insert_returning = ['id_marca_producto']
            
            # Insert Query
            result = db_conn.insert_query(table=TABLA_MARCA_PRODUCTO, columns=TABLA_MARCA_PRODUCTO_COLUMNS[1:], values=insert_values, returnData=True, returnColumns=insert_returning)
            if not result:
                return False
            
            # Process the query result
            self.set_idMarcaProducto(result[0][0])
            
            return True
        except Exception as e:
            logger.error(f"Error al insertar la marca de producto: {e}")
            return False
