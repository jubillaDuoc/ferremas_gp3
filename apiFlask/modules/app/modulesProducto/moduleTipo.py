import logging
import json

from models.modelsProductos.modelTipoProducto import TipoProducto
from models.modelsProductos.modelSubTipoProducto import SubtipoProducto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def man_create_tipo(nombre_tipo):
    try:
        # Instanciar clase Tipo
        tipo = TipoProducto()
        
        # Configurar tipo
        tipo.set_nombre(nombre_tipo)
        
        # Guardar tipo
        check_save = tipo.insert_tipo()
        if not check_save:
            return False, {'error': 'Error al guardar el tipo.'}
        
        # Validar tipo creado
        tipo = None
        tipo = TipoProducto().get_tipo_by_name(nombre_tipo)
        if not tipo:
            return False, {'error': 'Error al validar el tipo creado.'}
        tipo = None
        
        # Devolver la respuesta
        logger.info(f"Tipo {nombre_tipo} creado exitosamente.")
        return True, {'message': 'Tipo creado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para crear un tipo
        logger.error(f"Error al procesar solicitud para crear un tipo: {e}")
        return False, {'error': 'Error al crear el tipo.',
                       'error_detail': str(e)}
        
def man_get_tipos():
    try:
        logger.info(f"Obteniendo tipos")
        
        # Instanciar clase TIPO
        tipo = TipoProducto()
        
        tipos = tipo.get_tipos()
        if not tipos:
            return False, {'error': 'Error al obtener los tipos.'}
        
        # Procesar el resultado
        return True, {'tipos': tipos}
    except Exception as e:
        # Error al procesar la solicitud para obtener tipos
        logger.error(f"Error al procesar solicitud para obtener tipos: {e}")
        return False, {'error': 'Error al obtener los tipos.',
                       'error_detail': str(e)}
        
def man_get_tipo_by_id(id_tipo):
    try:
        # Obtener tipo
        tipo = TipoProducto().get_tipo_by_id(id_tipo)
        if not tipo:
            return False, {'error': 'Error al obtener el tipo.'}
        
        # Devolver la respuesta
        return True, {'tipo': tipo}
    except Exception as e:
        # Error al procesar la solicitud para obtener un tipo
        logger.error(f"Error al procesar solicitud para obtener un tipo: {e}")
        return False, {'error': 'Error al obtener el tipo.',
                       'error_detail': str(e)}
        
def man_get_subtipos_by_tipo(id_tipo):
    try:
        # Obtener subtipos
        subtipos = SubtipoProducto().get_subtipos_by_tipo(id_tipo)
        if not subtipos:
            return False, {'error': 'Error al obtener los subtipos.'}
        
        # Devolver la respuesta
        return True, {'subtipos': subtipos}
    except Exception as e:
        # Error al procesar la solicitud para obtener subtipos
        logger.error(f"Error al procesar solicitud para obtener subtipos: {e}")
        return False, {'error': 'Error al obtener los subtipos.',
                       'error_detail': str(e)}