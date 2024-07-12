import logging
from modules.postgres import DBConnection as psql

from models.modelsPedidos import TABLA_ESTADO_PEDIDO, TABLA_ESTADO_PEDIDO_COLUMNS

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

class EstadoPedido:
    def __init__(self):
        self.idEstadoPedido = None
        self.nombreEstadoPedido = None
    
    # Getters
    def get_idEstadoPedido(self):
        return self.idEstadoPedido
    
    def get_nombreEstadoPedido(self):
        return self.nombreEstadoPedido
    
    def to_json(self):
        return {
            'id_estado_pedido': self.idEstadoPedido,
            'nombre_estado_pedido': self.nombreEstadoPedido
        }
    
    # Setters
    def set_idEstadoPedido(self, idEstadoPedido):
        try:
            idEstadoPedido = int(idEstadoPedido)
        except:
            logger.error(f"Error al convertir el ID del estado del pedido a entero.")
            idEstadoPedido = None
        
        if idEstadoPedido <= 0:
            logger.error(f"ID del estado del pedido inválido.")
            idEstadoPedido = None
            
        self.idEstadoPedido = idEstadoPedido
    
    def set_nombreEstadoPedido(self, nombreEstadoPedido):
        self.nombreEstadoPedido = nombreEstadoPedido
    
    def get_estados_pedido(self):
        """
        Obtiene todos los estados de pedidos de la base de datos.
        
        Returns:
            Una lista de diccionarios con la información de los estados de pedidos.
        """
        try:
            # Obtener la conexión a la base de datos
            connection = psql()
            
            # Query para obtener los estados de pedidos
            result = connection.select_query(from_table=TABLA_ESTADO_PEDIDO)
            
            if not result:
                return None
                
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener los estados de pedidos de la base de datos: {str(e)}")
            return None
    
    def get_estado_pedido_by_id(self, idEstadoPedido):
        """
        Obtiene la información de un estado de pedido específico.
        
        Args:
            idEstadoPedido (int): El ID del estado de pedido a obtener.
        
        Returns:
            Un diccionario con la información del estado de pedido.
        """
        
        # Validar entrada
        try:
            idEstadoPedido = int(idEstadoPedido)
        except:
            logger.error(f"Error al convertir el ID del estado de pedido a entero.")
            return None
        
        if idEstadoPedido <= 0:
            logger.error(f"ID del estado de pedido inválido.")
            return None
        
        try:
            # Instanciar conexion a la base de datos
            db_connection = psql()
            
            # Definir Query
            where_definition = "id_estado_pedido = %s"
            where_data = (idEstadoPedido,)
            
            # Obtener estado de pedido
            result = db_connection.select_query(from_table=TABLA_ESTADO_PEDIDO, where_condition=where_definition, where_params=where_data)
            if not result:
                return False, {'error': 'Error al obtener el estado de pedido.'}
            
            # Procesar el resultado
            data = result[0]
            self.set_idEstadoPedido(data['id_estado_pedido'])
            self.set_nombreEstadoPedido(data['nombre_estado_pedido'])
            
            return self
        except Exception as e:
            logger.error(f"Error al obtener el estado de pedido: {str(e)}")
            return None
    
    def get_estado_pedido_by_name(self, nombreEstadoPedido):
        """
        Obtiene la información de un estado de pedido específico.
        
        Args:
            nombreEstadoPedido (str): El nombre del estado de pedido a obtener.
        
        Returns:
            Un diccionario con la información del estado de pedido.
        """
        
        try:
            # Instanciar conexion a la base de datos
            db_connection = psql()
            
            # Definir Query
            where_definition = "nombre_estado_pedido = %s"
            where_data = (nombreEstadoPedido,)
            
            # Obtener estado de pedido
            result = db_connection.select_query(from_table=TABLA_ESTADO_PEDIDO, where_condition=where_definition, where_params=where_data)
            if not result:
                return False, {'error': 'Error al obtener el estado de pedido.'}
            
            # Procesar el resultado
            data = result[0]
            self.set_idEstadoPedido(data['id_estado_pedido'])
            self.set_nombreEstadoPedido(data['nombre_estado_pedido'])
            
            return self
        except Exception as e:
            logger.error(f"Error al obtener el estado de pedido: {str(e)}")
            return None