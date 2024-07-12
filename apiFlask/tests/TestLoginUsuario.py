import unittest
from unittest.mock import patch
from app import create_app

class TestLoginUsuario(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_login_usuario(self):

        # Simular una solicitud de inicio de sesión
        response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        print(f"token: {response.json['token']}")

if __name__ == '__main__':
    unittest.main()
