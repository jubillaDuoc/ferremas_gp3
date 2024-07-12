import unittest
from unittest.mock import patch
from app import create_app

class TestAgregarProductoPedido(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('modules.app.modulesPedido.modulePedido.Pedido')
    def test_addproduct_pedido(self, MockPedido):
        # Solicitud de inicio de sesión para obtener el token
        login_response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Verificar que el login fue exitoso
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['token']

        # Configurar el mock del pedido
        MockPedido.return_value.get_pedido_by_id.return_value = MockPedido
        MockPedido.return_value.remove_producto.return_value = True
        MockPedido.return_value.guardar_pedido.return_value = True

        # Simular una solicitud de creación de pedido usando el token
        response = self.client.post('/api/pedidos/remove_product_from_order', json={
            'idOrder': "1",
            'idProducto': "1",
            'token': token
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()
