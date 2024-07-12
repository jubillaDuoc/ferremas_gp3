import unittest
from unittest.mock import patch
from app import create_app

class TestCambioContraseña(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('modules.auth.moduleUserABM.UsersModel')
    def test_creacion_pedido(self, MockABM):
        # Solicitud de inicio de sesión para obtener el token
        login_response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Verificar que el login fue exitoso
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['token']
        
        # Configurar el mock de ABM
        MockABM.return_value.get_user_by_id.return_value = MockABM
        MockABM.return_value.get_id_user.return_value = 1
        MockABM.return_value.update_user.return_value = True

        # Simular una solicitud de creación de pedido usando el token
        response = self.client.post('/api/users/user_update', json={
            'idUser': "1",
            'passwd': "somepass123",
            'nombre_user': "somename",
            'token': token
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()
