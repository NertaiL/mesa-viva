"""Pruebas del CRUD y del control de acceso por perfil.

Ejecutar con: python manage.py test
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto


class CrudProductoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Bebidas', orden=1)
        self.admin = User.objects.create_user('admin', password='clave-larga-123', is_staff=True)
        self.garzon = User.objects.create_user('garzon', password='clave-larga-123')
        self.producto = Producto.objects.create(
            nombre='Limonada', descripcion='Menta y jengibre',
            precio=3500, categoria=self.categoria,
        )

    def test_listado_exige_autenticacion(self):
        respuesta = self.client.get(reverse('menu:home'))
        self.assertEqual(respuesta.status_code, 302)

    def test_admin_crea_producto(self):
        self.client.login(username='admin', password='clave-larga-123')
        self.client.post(reverse('menu:producto-create'), {
            'nombre': 'Pizza margarita', 'descripcion': 'Masa madre',
            'precio': 8900, 'categoria': self.categoria.pk, 'disponible': True,
        })
        self.assertTrue(Producto.objects.filter(nombre='Pizza margarita').exists())

    def test_admin_edita_producto(self):
        self.client.login(username='admin', password='clave-larga-123')
        self.client.post(self.producto.get_edit_url(), {
            'nombre': 'Limonada', 'descripcion': 'Menta y jengibre',
            'precio': 3900, 'categoria': self.categoria.pk, 'disponible': True,
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.precio, 3900)

    def test_borrado_solo_por_post(self):
        self.client.login(username='admin', password='clave-larga-123')
        self.client.get(self.producto.get_delete_url())
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())
        self.client.post(self.producto.get_delete_url())
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_garzon_no_puede_crear(self):
        self.client.login(username='garzon', password='clave-larga-123')
        respuesta = self.client.get(reverse('menu:producto-create'))
        self.assertEqual(respuesta.status_code, 302)

    def test_precio_cero_es_rechazado(self):
        self.client.login(username='admin', password='clave-larga-123')
        self.client.post(reverse('menu:producto-create'), {
            'nombre': 'Item gratis', 'descripcion': 'x',
            'precio': 0, 'categoria': self.categoria.pk,
        })
        self.assertFalse(Producto.objects.filter(nombre='Item gratis').exists())

    def test_filtro_por_categoria(self):
        postres = Categoria.objects.create(nombre='Postres', orden=2)
        Producto.objects.create(nombre='Tiramisú', descripcion='Café', precio=4900, categoria=postres)
        self.client.login(username='garzon', password='clave-larga-123')
        respuesta = self.client.get(reverse('menu:home'), {'categoria': postres.pk})
        self.assertContains(respuesta, 'Tiramisú')
        self.assertNotContains(respuesta, 'Limonada')
