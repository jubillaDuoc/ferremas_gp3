import logging
import json

from models.modelsProductos.modelSubTipoProducto import SubtipoProducto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def man_create_subtipo(nombre_subtipo, id_tipo):
    try:
        # Instanciar clase Subtipo
        subtipo = SubtipoProducto()
        
        # Configurar subtipo
        subtipo.set_nombre(nombre_subtipo)
        subtipo.set_tipo(id_tipo)
        
        # Guardar subtipo
        check_save = subtipo.insert_subtipo()
        if not check_save:
            return False, {'error': 'Error al guardar el subtipo.'}
        
        # Validar subtipo creado
        subtipo = None
        subtipo = SubtipoProducto().get_subtipo_by_name(nombre_subtipo)
        if not subtipo:
            return False, {'error': 'Error al validar el subtipo creado.'}
        subtipo = None
        
        # Devolver la respuesta
        logger.info(f"Subtipo {nombre_subtipo} creado exitosamente.")
        return True, {'message': 'Subtipo creado exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para crear un subtipo
        logger.error(f"Error al procesar solicitud para crear un subtipo: {e}")
        return False, {'error': 'Error al crear el subtipo.',
                       'error_detail': str(e)}
        
def man_get_subtipos():
    try:
        # Obtener subtipos
        subtipos = SubtipoProducto().get_subtipos()
        if not subtipos:
            return False, {'error': 'Error al obtener los subtipos.'}
        
        # Devolver la respuesta
        return True, {'subtipos': subtipos}
    except Exception as e:
        # Error al procesar la solicitud para obtener subtipos
        logger.error(f"Error al procesar solicitud para obtener subtipos: {e}")
        return False, {'error': 'Error al obtener los subtipos.',
                       'error_detail': str(e)}
        
def man_get_subtipo_by_id(id_subtipo):
    try:
        # Obtener subtipo
        subtipo = SubtipoProducto().get_subtipo_by_id(id_subtipo)
        if not subtipo:
            return False, {'error': 'Error al obtener el subtipo.'}
        
        # Devolver la respuesta
        return True, {'subtipo': subtipo}
    except Exception as e:
        # Error al procesar la solicitud para obtener un subtipo
        logger.error(f"Error al procesar solicitud para obtener un subtipo: {e}")
        return False, {'error': 'Error al obtener el subtipo.',
                       'error_detail': str(e)}
        
def man_get_subtipo_by_name(nombre_subtipo):
    try:
        # Obtener subtipo
        subtipo = SubtipoProducto().get_subtipo_by_name(nombre_subtipo)
        if not subtipo:
            return False, {'error': 'Error al obtener el subtipo.'}
        
        # Devolver la respuesta
        return True, {'subtipo': subtipo}
    except Exception as e:
        # Error al procesar la solicitud para obtener un subtipo
        logger.error(f"Error al procesar solicitud para obtener un subtipo: {e}")
        return False, {'error': 'Error al obtener el subtipo.',
                       'error_detail': str(e)}
        
        