import unittest
from unittest.mock import patch
from app import create_app

class TestTokenInvalido(unittest.TestCase):

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
        
        token_invalido = "token_invalido"
        
        # Simular una solicitud para validar el token
        response = self.client.post('/api/users/user_validate_token', json={
            'token': token_invalido
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json)
        print(f"error: {response.json['error']}")

if __name__ == '__main__':
    unittest.main()
