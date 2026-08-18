from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse_lazy


class BaseNombre(models.Model):
    """Base abstracta: todo lo que se nombra en la carta se audita igual."""

    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    actualizado = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre


class Categoria(BaseNombre):
    orden = models.PositiveIntegerField(
        default=0, verbose_name='Orden en la carta'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']

    def get_delete_url(self):
        return reverse_lazy('menu:categoria-delete', kwargs={'pk': self.pk})


class Producto(BaseNombre):
    descripcion = models.CharField(max_length=256, verbose_name='Descripción')
    imagen = models.ImageField(
        upload_to='productos', blank=True, verbose_name='Imagen'
    )
    # Precio en pesos chilenos: la moneda no usa decimales, un entero evita
    # errores de redondeo al totalizar un pedido.
    precio = models.PositiveIntegerField(
        verbose_name='Precio (CLP)', validators=[MinValueValidator(1)]
    )
    disponible = models.BooleanField(
        default=True, verbose_name='Disponible hoy'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,  # una categoría con productos no se borra
        verbose_name='Categoría',
        related_name='productos',
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['categoria__orden', 'nombre']

    def get_edit_url(self):
        return reverse_lazy('menu:producto-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('menu:producto-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse_lazy('menu:producto-detail', kwargs={'pk': self.pk})
