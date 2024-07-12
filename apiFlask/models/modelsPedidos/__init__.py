# Desc: Módulo para manipular los modelos de la base de datos
# Developer: Vachir00

# Inicialización de las tablas y vistas de la base de datos

TABLA_PEDIDOS = 'PEDIDO'
TABLA_PEDIDOS_COLUMNS = [
    'id_pedido',
    'id_user',
    'fecha_pedido',
    'total_pedido',
    'id_estado_pedido',
]

TABLA_ESTADO_PEDIDO = 'ESTADO_PEDIDO'
TABLA_ESTADO_PEDIDO_COLUMNS = [
    'id_estado_pedido',
    'nombre_estado_pedido'
]

TABLA_PEDIDO_PRODUCTO = 'PEDIDO_PRODUCTO'
TABLA_PEDIDO_PRODUCTO_COLUMNS = [
    'id_pedido_producto',
    'id_pedido',
    'id_producto',
    'cantidad_producto',
    'precio_producto',
]

VISTA_PEDIDO_PRODUCTO = 'PEDIDO_PRODUCTO_VIEW'
VISTA_PEDIDO_PRODUCTO_COLUMNS = [
    'id_pedido_producto',
    'id_pedido',
    'id_producto',
    'nombre_producto',
    'cantidad_producto',
    'precio_producto',
    'fecha_pedido',
    'total_pedido',
    'id_estado_pedido',
    'nombre_estado_pedido',
]

VISTA_PEDIDO = 'PEDIDO_VIEW'
VISTA_PEDIDO_COLUMNS = [
    'id_pedido',
    'fecha_pedido',
    'total_pedido',
    'id_estado_pedido',
    'nombre_estado_pedido',
    'id_user',
    'nombre_user',
    'email_user',
    'id_user_rol',
    'nombre_user_rol',
    'id_user_state',
    'nombre_user_state',
]