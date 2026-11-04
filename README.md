# Unidad 5 CLN - Proyecto Base y Pruebas Automatizadas

## 1. Instalación
Para configurar el proyecto localmente, ejecuta los siguientes comandos en tu terminal de Windows:
1. Crear el entorno virtual: `py -3.11 -m venv .venv`
2. Activar el entorno virtual: `.\.venv\Scripts\Activate.ps1`
3. Instalar las dependencias: `python -m pip install -r requirements.txt`

## 2. Comandos Principales
* **Ejecutar las pruebas:** `python -m pytest -v`
* **Validar estilo de código (Linter):** `ruff check src tests`
* **Generar reporte de cobertura (Mínimo 80%):** `pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80`

## 3. Arquitectura de Puertos y Adaptadores
El proyecto utiliza una arquitectura que aísla las reglas de negocio de la infraestructura:
* **Dominio:** Contiene las entidades, Value Objects y reglas de negocio aisladas. No importa SQLAlchemy ni bibliotecas externas.
* **Repositorio:** Separa el dominio del ORM (SQLAlchemy) y la base de datos (SQLite), usando Unit of Work para controlar el commit y rollback.
* **Pasarela de pago:** Se maneja como un puerto externo. En las pruebas unitarias, se evita el acoplamiento a proveedores reales sustituyéndola con mocks para simular aprobaciones, rechazos o timeouts.
* **Bus de eventos:** Encargado de la mensajería del sistema. 

*Notas importantes: El proyecto base es un ejemplo de pedidos, no la solución del PIA. La política de cancelación impide cancelar pedidos enviados, incluso para administradores. El pipeline (GitHub Actions) realiza verificaciones de build, cobertura y linting, no despliegue productivo.*
