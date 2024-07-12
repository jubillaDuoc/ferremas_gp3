import unittest
from unittest.mock import patch
from app import create_app

class TestRegistroUsuario(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('modules.auth.moduleUserABM.UsersModel')
    def test_creacion_pedido(self, MockABM):
        # Configurar el mock de ABM
        MockABM.return_value.save_user.return_value = True
        MockABM.return_value.get_id_user.return_value = 1

        # Simular una solicitud de creación de pedido usando el token
        response = self.client.post('/api/users/user_create', json={
            'email': "somemail@mail.com",
            'passwd': "somepass",
            'nombre_user': "somename"
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()
