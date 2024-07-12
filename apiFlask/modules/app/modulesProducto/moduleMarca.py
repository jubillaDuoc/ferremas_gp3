import logging
from models.modelsProductos.modelMarcaProducto import MarcaProducto

# Configurar un logger específico para este módulo
logger = logging.getLogger(__name__)

def man_create_marca(nombre_marca):
    try:
        # Instanciar clase Marca
        marca = MarcaProducto()
        
        # Configurar marca
        marca.set_nombre(nombre_marca)
        
        # Guardar marca
        check_save = marca.insert_marca()
        if not check_save:
            return False, {'error': 'Error al guardar la marca.'}
        
        # Validar marca creada
        marca = None
        marca = MarcaProducto().get_marca_by_name(nombre_marca)
        if not marca:
            return False, {'error': 'Error al validar la marca creada.'}
        marca = None
        
        # Devolver la respuesta
        logger.info(f"Marca {nombre_marca} creada exitosamente.")
        return True, {'message': 'Marca creada exitosamente.'}
    except Exception as e:
        # Error al procesar la solicitud para crear una marca
        logger.error(f"Error al procesar solicitud para crear una marca: {e}")
        return False, {'error': 'Error al crear la marca.',
                       'error_detail': str(e)}
        
def man_get_marcas():
    try:
        # Obtener marcas
        marcas = MarcaProducto().get_marcas()
        if not marcas:
            return False, {'error': 'Error al obtener las marcas.'}
        
        # Devolver la respuesta
        return True, {'marcas': marcas}
    except Exception as e:
        # Error al procesar la solicitud para obtener marcas
        logger.error(f"Error al procesar solicitud para obtener marcas: {e}")
        return False, {'error': 'Error al obtener las marcas.',
                       'error_detail': str(e)}
        
def man_get_marca_by_id(id_marca):
    try:
        # Obtener marca
        marca = MarcaProducto().get_marca_by_id(id_marca)
        if not marca:
            return False, {'error': 'Error al obtener la marca.'}
        
        # Devolver la respuesta
        return True, {'marca': marca}
    except Exception as e:
        # Error al procesar la solicitud para obtener marca
        logger.error(f"Error al procesar solicitud para obtener marca: {e}")
        return False, {'error': 'Error al obtener la marca.',
                       'error_detail': str(e)}