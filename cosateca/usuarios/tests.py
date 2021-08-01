from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Usuario

class UsuarioTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.save()
        self.usuario = Usuario(user=self.u, telefono=123456789)

    def tearDown(self):
        self.client = None

    def test_login_ok(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }

        response = self.client.post('/login/', answers)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
    
    def test_login_fail(self):
        answers = {
                'username': 'impostor',
                'password': 'impostor1234'
            }

        response = self.client.post('/login/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[-1], 'usuarios/login.html')

    def test_registro_ok(self):
        answers = {
                'username': 'usuario_bueno',
                'password1': 'usuario1234',
                'password2': 'usuario1234',
                'email': 'test@test.com',
                'telefono': '234567890'
            }

        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.last().username, 'usuario_bueno')
        self.assertEqual(Usuario.objects.last().user, User.objects.last())
    
    def test_registro_fail_username_existente(self):
        answers = {
                'username': 'prueba',
                'password1': 'usuario1234',
                'password2': 'usuario1234',
                'email': 'existente@existente.com',
                'telefono': '111111111'
            }

        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(User.objects.last().email, 'existente@existente.com')


