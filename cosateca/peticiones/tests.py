from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from usuarios.models import Usuario
from .models import Peticion

class PeticionesTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.save()
        self.usuario = Usuario(user=self.u, telefono='123456789')
        self.usuario.save()

    def tearDown(self):
        self.client = None

    def test_crear_peticion_ok(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Peticion de prueba',
            'descripcion': 'Esto es una peticion de prueba',
            'provincia': 'Sevilla'
            }

        response = self.client.post('/peticiones/crear/', answers)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Peticion.objects.last().titulo, 'Peticion de prueba')
    
    def test_crear_peticion_fail(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Peticion de prueba',
            'descripcion': 'Esto es una peticion de prueba',
            'provincia': ''
            }
        response = self.client.post('/peticiones/crear/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[-1], 'peticiones/crear_peticion.html')
    
    def test_editar_oferta_no_existente(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'provincia': 'Sevilla'
            }
        response = self.client.post('/peticiones/crear/', answers)
        peticion = Peticion.objects.last()
        response = self.client.get('/peticiones/editar/'+ str(peticion.id+1) +'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='base/error.html')

    def test_eliminar_oferta(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Peticion de prueba',
            'descripcion': 'Esto es una peticion de prueba',
            'provincia': 'Sevilla'
            }
        response = self.client.post('/peticiones/crear/', answers)
        peticion = Peticion.objects.last()
        asnwers = {
            'peticion_id': str(peticion.id)
        }
        response = self.client.post('/peticiones/borrar/', asnwers)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/peticiones/misPeticiones/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)