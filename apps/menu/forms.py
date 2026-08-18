from django import forms

from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Campos explícitos: los de auditoría no los edita el usuario.
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen', 'disponible']

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 1:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'orden']


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
