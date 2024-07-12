import unittest
from unittest.mock import patch
from app import create_app

class TestCreacionPedido(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('modules.app.modulesPedido.modulePedido.Pedido')
    def test_creacion_pedido(self, MockPedido):
        # Solicitud de inicio de sesión para obtener el token
        login_response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Verificar que el login fue exitoso
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['token']

        # Configurar el mock del pedido
        MockPedido.return_value.get_all_pedidos.return_value = [
            {
                'id_pedido': 1,
                'id_user': 1,
                'fecha_pedido': '2021-10-10',
                'estado_pedido': 'pendiente'
                },
            {
                'id_pedido': 2,
                'id_user': 2,
                'fecha_pedido': '2021-10-10',
                'estado_pedido': 'pendiente'
                }
            ]

        # Simular una solicitud de creación de pedido usando el token
        response = self.client.post('/api/pedidos/get_orders', json={
            'token': token
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json)
        self.assertEqual(len(response.json['orders']), 2)

if __name__ == '__main__':
    unittest.main()
