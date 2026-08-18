from django.urls import include, path

from . import views

app_name = 'menu'

productos_patterns = [
    path('', views.producto_list, name='home'),
    path('crear/', views.producto_create, name='producto-create'),
    path('<int:pk>/', views.producto_detail, name='producto-detail'),
    path('<int:pk>/editar/', views.producto_update, name='producto-edit'),
    path('<int:pk>/eliminar/', views.producto_delete, name='producto-delete'),
]

urlpatterns = [
    path('', views.log_in, name='log-in'),
    path('salir/', views.log_out, name='log-out'),
    path('categorias/', views.categoria_list, name='categoria-list'),
    path('categorias/crear/', views.categoria_create, name='categoria-create'),
    path('productos/', include(productos_patterns)),
]
