FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# No correr como root dentro del contenedor.
RUN useradd --create-home mesaviva && chown -R mesaviva /app
USER mesaviva

EXPOSE 8000
# Local
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Deploy
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_demo && python manage.py runserver 0.0.0.0:${PORT:-10000}"]
