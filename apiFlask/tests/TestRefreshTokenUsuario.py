import unittest
from unittest.mock import patch
from app import create_app

class TestRefreshTokenUsuario(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_carga_productos(self):
        # Simular una solicitud de inicio de sesión para obtener el token
        login_response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Verificar que el login fue exitoso y obtener el token
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['token']
        
        # Simular una solicitud para Refrescar el token
        response = self.client.post('/api/users/user_refresh_token', json={
            'token': token
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        print(f"message: {response.json['message']}")

if __name__ == '__main__':
    unittest.main()
