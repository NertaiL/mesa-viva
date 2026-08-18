"""Carga datos de demostración para el despliegue local."""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.menu.models import Categoria, Producto

CARTA = [
    ('Entradas', 1, [
        ('Empanada de queso', 'Masa casera, queso mantecoso', 2500, True),
        ('Papas rústicas', 'Con alioli de la casa', 3900, True),
    ]),
    ('Fondos', 2, [
        ('Pizza margarita', 'Masa madre, albahaca fresca', 8900, True),
        ('Lomo saltado', 'Acompañado de arroz graneado', 10500, True),
        ('Risotto de hongos', 'Hongos salteados y parmesano', 9800, False),
    ]),
    ('Bebidas', 3, [
        ('Limonada de menta', 'Menta y jengibre', 3500, True),
        ('Café espresso', 'Grano de origen', 2200, True),
    ]),
    ('Postres', 4, [
        ('Tiramisú', 'Receta clásica con café', 4900, True),
    ]),
]

USUARIOS = [
    ('admin', 'mesaviva-2026', True),
    ('garzon', 'mesaviva-2026', False),
]


class Command(BaseCommand):
    help = 'Crea categorías, productos y usuarios de prueba.'

    def handle(self, *args, **options):
        for nombre, orden, productos in CARTA:
            categoria, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={'orden': orden}
            )
            for prod_nombre, descripcion, precio, disponible in productos:
                Producto.objects.get_or_create(
                    nombre=prod_nombre,
                    defaults={
                        'descripcion': descripcion,
                        'precio': precio,
                        'disponible': disponible,
                        'categoria': categoria,
                    },
                )

        for username, password, is_staff in USUARIOS:
            usuario, creado = User.objects.get_or_create(
                username=username, defaults={'is_staff': is_staff, 'is_superuser': is_staff}
            )
            if creado:
                usuario.set_password(password)
                usuario.save()

        self.stdout.write(self.style.SUCCESS(
            f'Datos cargados: {Categoria.objects.count()} categorías, '
            f'{Producto.objects.count()} productos, {User.objects.count()} usuarios.'
        ))
