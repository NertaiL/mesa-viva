from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, LoginForm, ProductoForm
from .models import Categoria, Producto


def admin_required(view):
    """Sólo el perfil administrador escribe en la carta; el garzón sólo la lee."""
    return login_required(user_passes_test(lambda u: u.is_staff)(view))


def log_in(request):
    form = LoginForm(request.POST or None)
    context = {'message': None, 'form': form, 'boton': 'Entrar'}
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, **form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('menu:home')
            context['message'] = 'El usuario ha sido desactivado'
        else:
            context['message'] = 'Usuario o contraseña incorrecta'
    return render(request, 'menu/login.html', context)


@login_required
def log_out(request):
    logout(request)
    return redirect('menu:log-in')


@login_required
def producto_list(request):
    productos = Producto.objects.select_related('categoria')
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    return render(
        request,
        'menu/index.html',
        {
            'productos': productos,
            'categorias': Categoria.objects.all(),
            'categoria_activa': categoria_id,
        },
    )


@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'menu/detail.html', {'producto': producto})


@admin_required
def producto_create(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('menu:home')
    return render(request, 'menu/form.html', {'form': form, 'titulo': 'Nuevo producto'})


@admin_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('menu:home')
    return render(request, 'menu/form.html', {'form': form, 'titulo': 'Editar producto'})


@admin_required
def producto_delete(request, pk):
    """El borrado exige POST: un GET no debe modificar el estado del sistema."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('menu:home')
    return render(request, 'menu/confirm_delete.html', {'objeto': producto})


@login_required
def categoria_list(request):
    return render(
        request,
        'menu/categoria/categoria_list.html',
        {'categorias': Categoria.objects.all()},
    )


@admin_required
def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('menu:categoria-list')
    return render(request, 'menu/form.html', {'form': form, 'titulo': 'Nueva categoría'})
