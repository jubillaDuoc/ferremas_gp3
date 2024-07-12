import logging
from modules.postgres import DBConnection

from models.modelsProductos import TABLA_PRODUCTOS, TABLA_PRODUCTOS_COLUMNS, VISTA_PRODUCTOS, VISTA_PRODUCTOS_COLUMNS
from models.modelsProductos.modelMarcaProducto import MarcaProducto
from models.modelsProductos.modelPrecioProducto import PrecioProducto
from models.modelsProductos.modelSubTipoProducto import SubtipoProducto
from models.modelsProductos.modelTipoProducto import TipoProducto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

class Producto:
    def __init__(self):
        self.idProducto = None
        self.nombre = None
        self.marca = MarcaProducto()
        self.stock = None
        self.precio = PrecioProducto()
        self.subtipo = SubtipoProducto()
    
    # Getters
    def get_idProducto(self):
        return self.idProducto
    
    def get_nombre(self):
        return self.nombre
    
    def get_marca(self):
        return self.marca
    
    def get_stock(self):
        return self.stock
    
    def get_precio(self):
        return self.precio
    
    def get_subtipo(self):
        return self.subtipo
    
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
    
    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def set_marca(self, product_trade):
        if isinstance(product_trade, MarcaProducto):
            self.marca = product_trade
    
    def set_stock(self, stock):
        try:
            stock = int(stock)
        except:
            logger.error(f"Error al convertir el stock a entero.")
            stock = None
            
        if stock < 0:
            logger.error(f"Stock inválido.")
            stock = None
            
        self.stock = stock
    
    def set_subtipo(self, subtipoProducto):
        if isinstance(subtipoProducto, SubtipoProducto):
            self.subtipo = subtipoProducto
    
    def set_newprecio(self, precioValue):
        try:
            precioValue = float(precioValue)
        except:
            logger.error(f"Error al convertir el precio a flotante.")
            precioValue = None
            return False
        
        if precioValue < 0:
            logger.error(f"Precio inválido.")
            precioValue = None
            return False
        
        # Set parameters
        self.precio.set_precionew(precioValue)
        self.precio.set_idProducto(self.idProducto)
        self.precio.insert_precio()
        return True
    
    # Métodos genericos
    def to_json(self):
        return {
            'id_producto': self.get_idProducto(),
            'nombre_producto': self.get_nombre(),
            'stock_producto': self.get_stock(),
            'precio_producto': self.get_precio().get_precio(),
            'fecha_precio_producto': self.get_precio().get_fecha(),
            'id_subtipo_producto': self.get_subtipo().get_idSubtipoProducto(),
            'nombre_subtipo_producto': self.get_subtipo().get_nombre(),
            'id_tipo_producto': self.get_subtipo().get_tipo().get_idTipoProducto(),
            'nombre_tipo_producto': self.get_subtipo().get_tipo().get_nombre(),
            'id_marca_producto': self.get_marca().get_idMarcaProducto(),
            'nombre_marca_producto': self.get_marca().get_nombre()
        }
    
    def get_productos(self, db_conn = DBConnection()):
        """
        Obtiene todos los productos de la base de datos.
        
        Returns:
            Una lista de diccionarios con la información de los productos.
        """
        try:
            # Query the database for the users
            result = db_conn.select_query(from_table=VISTA_PRODUCTOS, select_params=VISTA_PRODUCTOS_COLUMNS)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los productos: {e}")
            return None
    
    def get_productos_by_subtipo(self, idSubtipo, db_conn = DBConnection()):
        """
        Obtiene todos los productos de un subtipo específico.
        
        Args:
            idSubtipo (int): El ID del subtipo de producto.
        
        Returns:
            Una lista de diccionarios con la información de los productos.
        """
        
        # Comprobar la entrada
        try:
            idSubtipo = int(idSubtipo)
            if idSubtipo <= 0:
                logger.error(f"ID del subtipo de producto inválido.")
                return None
        except:
            logger.error(f"Error al convertir el ID del subtipo de producto a entero.")
            return None
        
        # Comprobar el ID del subtipo
        if not isinstance(SubtipoProducto().get_subtipo_by_id(idSubtipo), SubtipoProducto):
            logger.error(f"El subtipo de producto no existe.")
            return None
        
        try:
            # Definir consulta obtener los productos
            where_definition = "id_subtipo_producto = %s"
            where_data = (idSubtipo,)
            result = db_conn.select_query(from_table=VISTA_PRODUCTOS, select_params=VISTA_PRODUCTOS_COLUMNS, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los productos: {e}")
            return None
    
    def get_productos_by_marca(self, idMarca, db_conn = DBConnection()):
        """
        Obtiene todos los productos de una marca específica.
        
        Args:
            idMarca (int): El ID de la marca de producto.
        
        Returns:
            Una lista de diccionarios con la información de los productos.
        """
        
        # Comprobar la entrada
        try:
            idMarca = int(idMarca)
            if idMarca <= 0:
                logger.error(f"ID de la marca de producto inválido.")
                return None
        except:
            logger.error(f"Error al convertir el ID de la marca de producto a entero.")
            return None
        
        # Comprobar el ID de la marca
        if not isinstance(MarcaProducto().get_marca_by_id(idMarca), MarcaProducto):
            logger.error(f"La marca de producto no existe.")
            return None
        
        try:
            # Definir consulta obtener los productos
            where_definition = "id_marca_producto = %s"
            where_data = (idMarca,)
            result = db_conn.select_query(from_table=VISTA_PRODUCTOS, select_params=VISTA_PRODUCTOS_COLUMNS, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los productos: {e}")
            return None
    
    def get_productos_by_tipo(self, idTipo, db_conn = DBConnection()):
        """
        Obtiene todos los productos de un tipo específico.
        
        Args:
            idTipo (int): El ID del tipo de producto.
        
        Returns:
            Una lista de diccionarios con la información de los productos.
        """
        
        # Comprobar la entrada
        try:
            idTipo = int(idTipo)
            if idTipo <= 0:
                logger.error(f"ID del tipo de producto inválido.")
                return None
        except:
            logger.error(f"Error al convertir el ID del tipo de producto a entero.")
            return None
        
        # Comprobar el ID del tipo
        if not isinstance(TipoProducto().get_tipo_by_id(idTipo), TipoProducto):
            logger.error(f"El tipo de producto no existe.")
            return None
        
        try:
            # Definir consulta obtener los productos
            where_definition = "id_tipo_producto = %s"
            where_data = (idTipo,)
            result = db_conn.select_query(from_table=VISTA_PRODUCTOS, select_params=VISTA_PRODUCTOS_COLUMNS, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return None
                
            return result
        except Exception as e:
            logger.error(f"Error al obtener los productos: {e}")
            return None
        
    def get_producto_by_id(self, idProducto, db_conn = DBConnection()):
        """
        Obtiene la información de un producto específico.
        
        Args:
            idProducto (int): El ID del producto a obtener.
        
        Returns:
            Un diccionario con la información del producto.
        """
        
        # Validar entrada
        try:
            idProducto = int(idProducto)
            if idProducto <= 0:
                logger.error(f"ID del producto inválido.")
                return None
        except:
            logger.error(f"Error al convertir el ID del producto a entero.")
            return None
        
        try:
            # Definir Query
            where_definition = "id_producto = %s"
            where_data = (idProducto,)
            
            # Obtener producto
            result = db_conn.select_query(from_table=VISTA_PRODUCTOS, select_params=VISTA_PRODUCTOS_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return False, {'error': 'Error al obtener el producto.'}
            
            # Procesar el resultado
            data = result[0]
            self.set_idProducto(data['id_producto'])
            self.set_nombre(data['nombre_producto'])
            self.set_marca(MarcaProducto().get_marca_by_id(data['id_marca_producto']))
            self.set_stock(data['stock_producto'])
            self.precio.get_latest_precio_by_productid(data['id_producto'])
            self.set_subtipo(SubtipoProducto().get_subtipo_by_id(data['id_subtipo_producto']))
            
            return self
        
        except Exception as e:
            logger.error(f"Error al obtener el producto: {e}")
            return None
    
    def insert_producto(self, db_conn = DBConnection()):
        """
        Inserta un nuevo producto en la base de datos.
        
        Returns:
            True si el producto se insertó correctamente, False en caso contrario.
        """
        try:
            # Definir consulta insertar el producto
            insert_values = [
                self.get_nombre(),
                self.get_stock(),
                self.get_subtipo().get_idSubtipoProducto(),
                self.get_marca().get_idMarcaProducto()
                ]
            insert_returning = ['id_producto']
            
            # Insert Query
            result = db_conn.insert_query(table=TABLA_PRODUCTOS, columns=TABLA_PRODUCTOS_COLUMNS[1:], values=insert_values, returnData=True, returnColumns=insert_returning)
            
            if not result:
                return False
            
            self.idProducto = result[0][0]
            if not isinstance(self.idProducto, int):
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error al insertar el producto: {e}")
            return False
    
    def update_producto(self, db_conn = DBConnection()):
        """
        Actualiza la información de un producto en la base de datos.
        
        Returns:
            True si el producto se actualizó correctamente, False en caso contrario.
        """
        try:
            # Compose function
            set_columns = TABLA_PRODUCTOS_COLUMNS[1:]
            set_values = [self.get_nombre(), self.get_stock(), self.get_subtipo().get_idSubtipoProducto(), self.get_marca().get_idMarcaProducto()]
            where_definition = "id_producto = %s"
            where_data = (self.get_idProducto(),)
            
            # Update Query
            result = db_conn.update_query(table=TABLA_PRODUCTOS, set_columns=set_columns, set_values=set_values, where_condition=where_definition, where_params=where_data)
            if not result:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error al actualizar el producto: {e}")
            return False
