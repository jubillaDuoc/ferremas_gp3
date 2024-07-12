# Desc: Definición de las rutas de la aplicación
# Developer: Vachir00

# Importar rutas
# # Modulos de Usuario
from paths.pathsUsers.viewsUsersAuth import user_login_blueprint
from paths.pathsUsers.viewsUsersAbm import user_abm_blueprint
from paths.pathsProductos.viewsProductos import productos_blueprint
from paths.pathsPedidos.viewsPedidos import pedidos_blueprint

# Definir prefix de las rutas
USERS_API_PREFIX = '/api/users'
PRODUCTOS_API_PREFIX = '/api/productos'
PEDIDOS_API_PREFIX = '/api/pedidos'

def register_routes(app):
    app.register_blueprint(user_login_blueprint, url_prefix=USERS_API_PREFIX)
    app.register_blueprint(user_abm_blueprint, url_prefix=USERS_API_PREFIX)
    app.register_blueprint(productos_blueprint, url_prefix=PRODUCTOS_API_PREFIX)
    app.register_blueprint(pedidos_blueprint, url_prefix=PEDIDOS_API_PREFIX)
    