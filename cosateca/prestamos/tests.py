from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from usuarios.models import Usuario
from ofertas.models import Oferta
from .models import Notificacion, Prestamo
from peticiones.models import Peticion

class PrestamosTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='usuario1')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.save()
        self.usuario = Usuario(user=self.u, telefono='123456789')
        self.usuario.save()

        self.u2 = User(username='usuario2')
        self.u2.set_password('usuario1234')
        self.u2.email = 'prueba2@gmail.com'
        self.u2.save()
        self.usuario2 = Usuario(user=self.u2, telefono='123456780')
        self.usuario2.save()

    def tearDown(self):
        self.client = None

    def test_solicitar_oferta(self):
        answers = {
            'username': 'usuario1',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta de prueba',
            'descripcion': 'Esto es una oferta de prueba',
            'imagen': 'url_imagen_inventada',
            'provincia': 'Sevilla'
            }
        self.client.post('/ofertas/crear/', answers)
        self.client.get('/logout/')

        answers = {
            'username': 'usuario2',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)

        oferta = Oferta.objects.last()
        response = self.client.post('/prestamos/solicitar/', {'oferta_id': str(oferta.id)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notificacion.objects.last().telefono, '0')

    def test_prestar_peticion(self):
        answers = {
            'username': 'usuario1',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Peticion de prueba',
            'descripcion': 'Esto es una peticion de prueba',
            'provincia': 'Sevilla'
            }
        self.client.post('/peticiones/crear/', answers)
        self.client.get('/logout/')

        answers = {
            'username': 'usuario2',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)

        peticion = Peticion.objects.last()
        response = self.client.post('/prestamos/prestar/', {'peticion_id': str(peticion.id)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notificacion.objects.last().telefono, self.usuario2.telefono)

        prestamo = Prestamo.objects.last()
        self.assertEqual(prestamo.prestador, self.usuario2.user.username)
        self.assertEqual(prestamo.recibidor, self.usuario.user.username)

    def test_prestar_notificacion(self):
        answers = {
            'username': 'usuario1',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)
        
        answers = {
            'titulo': 'Oferta2',
            'descripcion': 'Segunda oferta de prueba',
            'imagen': 'url_imagen_inventada',
            'provincia': 'Sevilla'
            }
        self.client.post('/ofertas/crear/', answers)
        self.client.get('/logout/')

        answers = {
            'username': 'usuario2',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)

        oferta = Oferta.objects.last()
        self.client.post('/prestamos/solicitar/', {'oferta_id': str(oferta.id)})

        self.assertEqual(Notificacion.objects.last().oferta_id, oferta.id)
        self.assertEqual(Notificacion.objects.last().telefono, '0')
        self.client.get('/logout/')

        answers = {
            'username': 'usuario1',
            'password': 'usuario1234'
            }
        self.client.post('/login/', answers)

        response = self.client.post('/prestamos/prestar_notificacion/', {'oferta_id':str(oferta.id), 'nombre_recibidor': self.usuario2.user.username})
        self.assertEqual(response.status_code, 302)
        notificacion = Notificacion.objects.get(id=2)
        prestamo = Prestamo.objects.last()
        self.assertEqual(prestamo.recibidor, self.usuario2.user.username)
        self.assertEqual(notificacion.telefono, self.usuario.telefono)
    