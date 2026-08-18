# MesaViva — CRUD de carta

[![Django](https://img.shields.io/badge/Django-5.2%20LTS-092E20?logo=django&logoColor=white)](https://docs.djangoproject.com/en/5.2/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-7%20passing-brightgreen)](#pruebas)

Aplicación web para que un local de comida administre **su carta**: los productos que
vende, sus precios, su disponibilidad del día y las categorías con que se ordenan.

El personal entra con usuario y contraseña, y lo que puede hacer depende de su perfil:
el **administrador** mantiene la carta (crear, editar, eliminar) y el **garzón** sólo la
consulta desde el salón para responder qué hay disponible y a qué precio.

## 🌐 Demo en línea
La aplicación se encuentra desplegada en Render y puede probarse directamente desde el siguiente enlace:
👉 [Acceder a MesaViva](https://mesa-viva-yc4s.onrender.com/)


---

## Capturas

| Ingreso al sistema | Carta vista por el administrador |
|---|---|
| ![Login](capturas/01_login.png) | ![Listado admin](capturas/compacta_02_listado_admin.png) |

| Alta de producto | Ficha del producto |
|---|---|
| ![Crear](capturas/03_crear.png) | ![Detalle](capturas/04_detalle.png) |

| Confirmación de borrado | Categorías |
|---|---|
| ![Eliminar](capturas/06_eliminar.png) | ![Categorías](capturas/07_categorias.png) |

La misma carta vista por un garzón: sin botones de crear, editar ni eliminar.

![Listado garzón](capturas/compacta_08_listado_garzon.png)

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 5.2 LTS (Python 3.13) |
| Base de datos | PostgreSQL 17 con Docker · SQLite si no hay `DATABASE_URL` |
| Plantillas | Django Templates + Materialize CSS |
| Formularios | `django-widget-tweaks` |
| Imágenes | `Pillow` |
| Entorno | Docker + Docker Compose |

---

## Cómo levantarlo

### Con Docker Compose (recomendado)

Levanta Django y PostgreSQL, aplica las migraciones y carga la carta de ejemplo en un
solo comando:

```bash
docker compose up --build
```

La aplicación queda en <http://127.0.0.1:8000/>. Para detener y borrar la base:

```bash
docker compose down -v
```

### Sin Docker (SQLite)

Sin la variable `DATABASE_URL` el proyecto usa SQLite, así que no hace falta instalar
ningún motor de base de datos:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo     # carta de ejemplo + usuarios de prueba
python manage.py runserver
```

### Usuarios de prueba

Los crea `seed_demo`. Son sólo para desarrollo local.

| Usuario  | Contraseña      | Perfil        | Puede                             |
|----------|-----------------|---------------|-----------------------------------|
| `admin`  | `mesaviva-2026` | Administrador | Ver, crear, editar y eliminar     |
| `garzon` | `mesaviva-2026` | Garzón        | Sólo consultar la carta           |

### Variables de entorno

| Variable | Por defecto | Para qué sirve |
|---|---|---|
| `DJANGO_SECRET_KEY` | valor de desarrollo | Firma de sesiones y tokens. **Obligatoria fuera de local.** |
| `DJANGO_DEBUG` | `1` | `0` apaga el modo depuración. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Dominios que el sitio acepta atender. |
| `DATABASE_URL` | — | `postgres://usuario:clave@host:5432/base`. Si falta, se usa SQLite. |

---

## Perfiles y permisos

El control es una única compuerta: `admin_required` en `apps/menu/views.py:9`, que exige
sesión iniciada **y** perfil administrador (`is_staff`). Toda vista que escribe pasa por
ahí; las de lectura sólo exigen sesión iniciada.

| Acción | Anónimo | Garzón | Administrador |
|---|:--:|:--:|:--:|
| Ver la carta y el detalle de un producto | ✗ | ✓ | ✓ |
| Ver las categorías | ✗ | ✓ | ✓ |
| Crear, editar y eliminar productos | ✗ | ✗ | ✓ |
| Crear categorías | ✗ | ✗ | ✓ |

Quien no tiene permiso es redirigido al login; la interfaz además le oculta los botones
que no puede usar, pero el permiso se decide en el servidor, no en la plantilla.

---

## Modelo de datos

```mermaid
erDiagram
    CATEGORIA ||--o{ PRODUCTO : agrupa
    CATEGORIA {
        int  id
        string   nombre
        int      orden
        datetime creado
        datetime actualizado
    }
    PRODUCTO {
        int      id
        string   nombre
        string   descripcion
        int      precio
        bool     disponible
        image    imagen
        int      categoria_id
        datetime creado
        datetime actualizado
    }
```

Tres decisiones que vale la pena explicar:

- **El precio es un entero**, no un decimal: el peso chileno no usa centavos, y un entero
  evita los errores de redondeo que aparecen al sumar un pedido.
- **Una categoría con productos no se puede borrar** (`on_delete=PROTECT`): borrarla
  dejaría productos huérfanos en la carta.
- **`creado` y `actualizado` se llenan solos** en la clase base `BaseNombre`, así que todo
  lo que se nombra en la carta queda auditado igual y sin código repetido.

---

## Rutas

| Método    | Ruta                        | Operación | Perfil mínimo |
|-----------|-----------------------------|-----------|---------------|
| GET/POST  | `/`                         | Login     | —             |
| GET       | `/salir/`                   | Logout    | Garzón        |
| GET       | `/productos/`               | Read (listado, filtrable por categoría) | Garzón |
| GET       | `/productos/<pk>/`          | Read (detalle) | Garzón   |
| GET/POST  | `/productos/crear/`         | Create    | Administrador |
| GET/POST  | `/productos/<pk>/editar/`   | Update    | Administrador |
| GET/POST  | `/productos/<pk>/eliminar/` | Delete    | Administrador |
| GET       | `/categorias/`              | Read      | Garzón        |
| GET/POST  | `/categorias/crear/`        | Create    | Administrador |
| —         | `/admin/`                   | Admin de Django | Administrador |

El borrado **exige POST**: un GET muestra la confirmación y no toca la base, para que
ningún enlace ni precarga del navegador pueda eliminar un producto.

---

## Pruebas

```bash
python manage.py test                            # local
docker compose exec web python manage.py test    # dentro del contenedor
```

Las 7 pruebas de `apps/menu/tests.py` cubren el camino que funciona y el que debe
fallar: listado protegido para anónimos, alta y edición por el administrador, borrado
sólo por POST, garzón sin permiso de creación, rechazo de precio cero y filtro por
categoría.

---

## Estructura del proyecto

```
.
├── manage.py
├── mesaviva/                 # configuración del proyecto y URLconf raíz
│   ├── settings.py           # elige PostgreSQL o SQLite según DATABASE_URL
│   └── urls.py
├── apps/menu/                # la aplicación: carta y categorías
│   ├── models.py             # Categoria y Producto sobre la base BaseNombre
│   ├── views.py              # vistas CRUD + compuerta admin_required
│   ├── forms.py              # ModelForms y formulario de login
│   ├── urls.py               # rutas de la aplicación
│   ├── admin.py              # registro en el admin de Django
│   ├── tests.py              # pruebas de CRUD y permisos
│   ├── management/commands/
│   │   └── seed_demo.py      # carta de ejemplo y usuarios de prueba
│   └── templates/menu/       # plantillas (Materialize CSS)
├── capturas/                 # capturas de pantalla usadas en este README
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Notas para producción

El proyecto viene configurado para desarrollo local. Antes de exponerlo a internet hay
que, como mínimo: definir `DJANGO_SECRET_KEY`, poner `DJANGO_DEBUG=0`, declarar los
dominios reales en `DJANGO_ALLOWED_HOSTS`, cambiar las credenciales de la base y de los
usuarios de demostración, servir los archivos estáticos y subidos desde un servidor web
o almacenamiento externo, y reemplazar `runserver` por un servidor WSGI como Gunicorn.
