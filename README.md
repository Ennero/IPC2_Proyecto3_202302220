# Clasificación de mensajes XML con Flask y Django

Aplicación para cargar diccionarios y mensajes XML, clasificar texto y consultar resúmenes por empresa/fecha, gráficas y documentos PDF. Flask procesa la información y Django ofrece las vistas.

## Requisitos

Python 3.12 o superior y requirements.txt. Ejecutar backend desde backend/ y frontend desde frontend/ para conservar sus rutas relativas.

## Ejecución

Los comandos parten de la raíz del repositorio, salvo donde se indica otra terminal.

```bash
python -m pip install -r requirements.txt
cd backend
python backend.py

# Otra terminal, desde la raíz:
cd frontend
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

## Recorrido de demostración

Abrir http://127.0.0.1:8000 y cargar los XML de entrada/. El frontend se comunica con http://127.0.0.1:5000. Seguir el orden cargar → procesar → consultar para disponer de resultados.

## Organización

Carpetas de la entrega: [`Documetancion/`](Documetancion/), [`backend/`](backend/), [`entrada/`](entrada/), [`frontend/`](frontend/).

## Alcance y límites

Es un clasificador basado en las reglas y diccionarios de la entrega; no se afirma entrenamiento de un modelo ni capacidad de Big Data. El estado y reportes son locales, sin aislamiento multiusuario.

## Contexto y licencia

Trabajo académico o de aprendizaje conservado en el portafolio de [Enner Mendizabal](https://github.com/Ennero). Los créditos de los trabajos en grupo se conservan en sus entregas y manuales.

Consultar [LICENSE](LICENSE) para la licencia de la raíz. Las dependencias y los componentes con avisos o licencias propios conservan sus condiciones.
