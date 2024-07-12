import unittest
from unittest.mock import patch
from app import create_app

class TestCargaProductos(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('paths.pathsProductos.viewsProductos.man_get_productos')
    def test_carga_productos(self, mock_man_get_productos):

        # Simular una solicitud de inicio de sesión para obtener el token
        login_response = self.client.post('/api/users/user_login', json={
            'username': 'testadmin@example.com',
            'password': 'testadm'
        })

        # Verificar que el login fue exitoso
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['token']

        # Configurar el mock de obtener productos
        mock_man_get_productos.return_value = (True, {'productos': [{'id': 1, 'nombre': 'Producto 1'}, {'id': 2, 'nombre': 'Producto 2'}]})

        # Simular una solicitud para obtener productos usando el token
        response = self.client.post('/api/productos/get_productos', json={
            'token': token
        })

        # Validar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('productos', response.json)
        self.assertEqual(len(response.json['productos']), 2)

if __name__ == '__main__':
    unittest.main()
