import unittest
from unittest.mock import patch
from app import create_app

class TestVisualizacionDetallesProducto(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('modules.app.modulesProducto.moduleProductos.Producto')
    def test_get_detail_from_product(self, MockProducto):
        # Solicitud de inicio de sesión para obtener el token
        login_response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Verificar que el login fue exitoso
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['token']

        # Configurar el mock del pedido
        MockProducto.return_value.get_producto_by_id.return_value = MockProducto()
        MockProducto.return_value.to_json.return_value = {
            'id_producto': 1,
            'nombre_producto': "productoName",
            'stock_producto': 1,
            'precio_producto': 1000,
            'id_subtipo_producto': 1,
            'nombre_subtipo_producto': "subtipoName",
            'id_tipo_producto': 1,
            'nombre_tipo_producto': "tipoName",
            'id_marca_producto': 1,
            'nombre_marca_producto': "marcaName"
        }

        # Simular una solicitud de creación de pedido usando el token
        response = self.client.post('/api/productos/get_producto_by_id', json={
            'id_producto': "1",
            'token': token
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('producto', response.json)
        self.assertEqual(response.json['producto']['id_producto'], 1)

if __name__ == '__main__':
    unittest.main()
