# Desc: Módulo para definir los modelos de la base de datos
# Developer: Vachir00

# Inicialización de las tablas y vistas de la base de datos

# Sección de productos
TABLA_PRODUCTOS = 'PRODUCTO'
TABLA_PRODUCTOS_COLUMNS = [
    'id_producto',
    'nombre_producto',
    'stock_producto',
    'id_subtipo_producto',
    'id_marca_producto',
]

VISTA_PRODUCTOS = 'producto_view'
VISTA_PRODUCTOS_COLUMNS = [
    'id_producto',
    'nombre_producto',
    'stock_producto',
    'precio_producto',
    'fecha_precio_producto',
    'id_subtipo_producto',
    'nombre_subtipo_producto',
    'id_tipo_producto',
    'nombre_tipo_producto',
    'id_marca_producto',
    'nombre_marca_producto'
]

# Sección de marcas
TABLA_MARCA_PRODUCTO = 'marca_producto'
TABLA_MARCA_PRODUCTO_COLUMNS = [
    'id_marca_producto',
    'nombre_marca_producto',
]

# Sección de tipos de productos
TABLA_TIPO_PRODUCTO = 'tipo_producto'
TABLA_TIPO_PRODUCTO_COLUMNS = [
    'id_tipo_producto',
    'nombre_tipo_producto',
]

# Sección de subtipos de productos
TABLA_SUBTIPO_PRODUCTO = 'subtipo_producto'
TABLA_SUBTIPO_PRODUCTO_COLUMNS = [
    'id_subtipo_producto',
    'nombre_subtipo_producto',
    'id_tipo_producto',
]

# Sección de precios de productos
TABLA_PRECIO = 'precio_producto'
TABLA_PRECIO_COLUMNS = [
    'id_precio_producto',
    'id_producto',
    'precio_producto',
    'fecha_precio_producto',
]