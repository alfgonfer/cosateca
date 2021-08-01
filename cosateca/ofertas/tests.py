from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from usuarios.models import Usuario
from .models import Oferta

class OfertasTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.save()
        self.usuario = Usuario(user=self.u, telefono=123456789)
        self.usuario.save()

    def tearDown(self):
        self.client = None

    def test_crear_oferta_ok(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_inventada_imagen',
            'provincia': 'Sevilla'
            }

        response = self.client.post('/ofertas/crear/', answers)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Oferta.objects.last().titulo, 'Oferta de prueba')
    
    def test_crear_oferta_fail(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_inventada_imagen',
            'provincia': ''
            }
        response = self.client.post('/ofertas/crear/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[-1], 'ofertas/crear_oferta.html')
    
    def test_mostrar_oferta_ok(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_inventada_imagen',
            'provincia': 'Sevilla'
            }
        response = self.client.post('/ofertas/crear/', answers)
        oferta = Oferta.objects.last()
        response = self.client.get('/ofertas/'+ str(oferta.id) +'/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[-1], 'ofertas/mostrar_oferta.html')

    def test_mostrar_oferta_fail(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_inventada_imagen',
            'provincia': 'Sevilla'
            }
        response = self.client.post('/ofertas/crear/', answers)
        oferta = Oferta.objects.last()
        response = self.client.get('/ofertas/'+ str(oferta.id+1) +'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='base/error.html')
    
    def test_editar_oferta_no_existente(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_inventada_imagen',
            'provincia': 'Sevilla'
            }
        response = self.client.post('/ofertas/crear/', answers)
        oferta = Oferta.objects.last()
        response = self.client.get('/ofertas/editar/'+ str(oferta.id+1) +'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='base/error.html')

    def test_eliminar_oferta(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
            }

        response = self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_inventada_imagen',
            'provincia': 'Sevilla'
            }
        response = self.client.post('/ofertas/crear/', answers)
        oferta = Oferta.objects.last()
        asnwers = {
            'oferta_id': str(oferta.id)
        }
        response = self.client.post('/ofertas/borrar/', asnwers)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/ofertas/misOfertas/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)