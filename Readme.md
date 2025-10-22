# Métricas y KPIs para Inteligencia de Negocios

## Generador de Informes Interactivos de Métricas y KPIs para BI

Sistema Generador de Informes Interactivos de Inteligencia de Negocios (GIIN) ejecutado sobre una arquitectura de microservicios en contenedores Docker. El sistema consume datos de una base de datos MySQL para aplicar Aprendizaje Automatizado (ML) e implementar una API con FastAPI que disponibiliza las métricas y KPIs de un negocio retail. Estas métricas y KPIs son consumidas por un tablero interactivo web (Dashboard) implementado en Streamlit.

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura del Repositorio](#estructura-del-repositorio)
4. [Tecnologías Utilizadas](#tecnologías-utilizadas)
5. [Requisitos Previos](#requisitos-previos)
6. [Instalación y Configuración](#instalación-y-configuración)
7. [Uso del Sistema](#uso-del-sistema)
8. [Datos y Base de Datos](#datos-y-base-de-datos)
9. [API Endpoints](#api-endpoints)
10. [Colaboración](#colaboración)
11. [Preguntas Frecuentes](#preguntas-frecuentes)

## Descripción General

Este proyecto implementa una solución completa de Business Intelligence (BI) para análisis de datos de retail utilizando una arquitectura de microservicios. El sistema permite:

* Análisis de datos de ventas retail
* Generación de métricas y KPIs automatizados
* Visualización interactiva de datos
* Aplicación de algoritmos de Machine Learning
* API REST para consumo de datos
* Dashboard web interactivo

## Arquitectura del Sistema

El sistema está compuesto por los siguientes microservicios:

* **MySQL Container**: Base de datos para almacenamiento de datos de ventas
* **FastAPI Backend**: API REST para procesamiento de datos y ML
* **Jupyter Notebooks**: Entorno de desarrollo y análisis de datos
* **Streamlit Frontend**: Dashboard web interactivo
* **Scrapy App**: Herramientas de web scraping (opcional)

## Estructura del Repositorio

```
├── datasets/
│   └── OnlineRetail2b.csv          # Dataset principal de ventas retail
├── mysql_container/
│   ├── crear_database_empresa01.sql # Script de creación de BD
│   └── mysql_data/                 # Datos persistentes de MySQL
├── recursos/
│   ├── cargar.py                   # Script de carga de datos
│   ├── retail_kpis.pbix           # Dashboard Power BI
│   └── ventas_retail/             # Recursos adicionales
├── fastapi_backend.git/           # Código del backend FastAPI
├── jupyter_notebooks.git/        # Notebooks de análisis
├── streamlit_frontend.git/       # Frontend web interactivo
├── scrapy_app.git/              # Aplicación de web scraping
└── README.md                     # Este archivo
```

**Nota**: Este repositorio contiene únicamente las carpetas `.git` con el código fuente. Los archivos `compose.yaml` y `Dockerfile` de cada contenedor se mantienen en un repositorio separado para la estructura general del proyecto.

## Tecnologías Utilizadas

### Backend y Procesamiento

* **Python**: 3.11.x - Lenguaje principal
* **FastAPI**: Framework web para APIs REST
* **SQLAlchemy**: ORM para base de datos
* **MySQL**: Base de datos relacional
* **Pandas**: 1.5.3 - Manipulación de datos
* **NumPy**: 1.20.3 - Computación numérica
* **Scikit-learn**: Machine Learning

### Análisis y Visualización

* **Jupyter Notebooks**: Análisis interactivo
* **Streamlit**: Dashboard web
* **Matplotlib**: 3.8.1 - Visualización básica
* **Seaborn**: 0.12.2 - Visualización estadística
* **Plotly**: 5.15.0 - Visualización interactiva

### Estadísticas y ML

* **Statsmodels**: 0.14.0 - Modelos estadísticos
* **SciPy**: 1.11.3 - Computación científica
* **KMeans Clustering**: Segmentación de clientes

### Infraestructura

* **Docker**: Containerización
* **Docker Compose**: Orquestación de servicios

## Requisitos Previos

* **Docker** instalado (Docker Desktop o Engine)
* **Docker Compose** (moderno: `docker compose`) o versión legacy `docker-compose`
* **Git** para clonar los repositorios de código
* Al menos **4GB de RAM** disponible para los contenedores
* **Puertos disponibles**: 3306 (MySQL), 8000 (FastAPI), 8888 (Jupyter), 8501 (Streamlit)

## Instalación y Configuración

### 1. Preparación del Entorno

* **Clonar antes**: [url-repositorio-principal](https://github.com/JuanPerez-DataScientist/docker_multiple)

```bash
# Clonar este repositorio principal
git clone <url-repositorio-principal>
cd <nombre-repositorio>

# Clonar los submódulos de código (desde sus respectivos repositorios)
git clone <url-fastapi-backend> fastapi_backend
git clone <url-jupyter-notebooks> jupyter_notebooks  
git clone <url-streamlit-frontend> streamlit_frontend
git clone <url-scrapy-app> scrapy_app
```

### 2. Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DATABASE_HOST=mysql_service
DATABASE_USER=root
DATABASE_PASSWORD=admin
DATABASE_NAME=checkpoint_m2
MYSQL_PORT=3306

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Jupyter
JUPYTER_TOKEN=tu_token_seguro

# Streamlit
STREAMLIT_PORT=8501
```

### 3. Inicialización del Sistema

```bash
# Construir y levantar todos los servicios
docker compose up --build

# O en background
docker compose up -d --build
```

## Uso del Sistema

### Acceso a los Servicios

Una vez iniciado el sistema, los servicios están disponibles en:

* **FastAPI**: [http://localhost:8000](http://localhost:8000)
  * Documentación automática: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Jupyter Notebooks**: [http://localhost:8888](http://localhost:8888)
  * Token disponible en los logs del contenedor
* **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
* **MySQL**: `localhost:3306` (para conexiones externas)

### Comandos Útiles

```bash
# Ver logs de todos los servicios
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs -f fastapi_backend

# Parar todos los servicios
docker compose down

# Parar y eliminar volúmenes (¡cuidado con los datos!)
docker compose down -v

# Reiniciar un servicio específico
docker compose restart mysql_service
```

## Datos y Base de Datos

### Dataset Principal

El sistema utiliza el dataset **OnlineRetail2b.csv** que contiene:

* **InvoiceNo**: Número de factura
* **Quantity**: Cantidad de productos
* **UnitPrice**: Precio unitario
* **InvoiceDate**: Fecha de la transacción
* **CustomerID**: ID del cliente
* **Country**: País del cliente

### Estructura de Base de Datos

La base de datos `checkpoint_m2` incluye las siguientes tablas principales:

* **canal_venta**: Canales de venta (Telefónica, OnLine, Presencial)
* **producto**: Catálogo de productos con precios
* **venta**: Transacciones de ventas con relaciones FK
* **onlineretail2b**: Datos cargados desde el CSV

## API Endpoints

### FastAPI Endpoints Disponibles

* **GET** `/guardar_ventas`: Carga datos desde CSV a la base de datos
* **GET** `/ventas_mensuales`: Obtiene promedios de ventas mensuales
* **GET** `/docs`: Documentación interactiva de la API
* **GET** `/health`: Estado de salud del servicio

### Ejemplo de Uso de la API

```python
import requests

# Cargar datos
response = requests.get("http://localhost:8000/guardar_ventas")
print(response.json())

# Obtener ventas mensuales
response = requests.get("http://localhost:8000/ventas_mensuales")
ventas = response.json()
```

## Colaboración

### Cómo Contribuir

1. **Fork** el repositorio principal
2. **Clona** tu fork localmente
3. **Crea** una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
4. **Realiza** tus cambios y commits
5. **Push** a tu fork: `git push origin feature/nueva-funcionalidad`
6. **Crea** un Pull Request

### Estándares de Código

* Seguir **PEP 8** para código Python
* Documentar funciones y clases
* Incluir tests para nuevas funcionalidades
* Usar **type hints** en Python
* Commits descriptivos en español

### Estructura de Commits

```
tipo(alcance): descripción breve

Descripción más detallada si es necesaria

- Cambio específico 1
- Cambio específico 2
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Preguntas Frecuentes

### **¿Cómo reinicio la base de datos?**

Para reiniciar completamente la base de datos:

```bash
docker compose down -v
docker compose up --build
```

**Nota**: Esto eliminará todos los datos almacenados.

### **¿Qué hacer si un servicio no inicia correctamente?**

1. Verificar logs: `docker compose logs nombre_servicio`
2. Verificar puertos disponibles: `netstat -tulpn | grep :8000`
3. Reiniciar servicio específico: `docker compose restart nombre_servicio`
4. Reconstruir si es necesario: `docker compose up --build nombre_servicio`

### **¿Cómo agregar nuevos datos al sistema?**

Opciones disponibles:

* Reemplazar el archivo `datasets/OnlineRetail2b.csv`
* Usar el endpoint `/guardar_ventas` para cargar nuevos datos
* Conectar directamente a MySQL en puerto 3306
* Usar Jupyter notebooks para análisis exploratorio

### **¿El sistema funciona en producción?**

Este sistema está diseñado para **desarrollo, prototipado y demos**. Para producción se recomienda:

* Configurar variables de entorno seguras
* Usar bases de datos externas
* Implementar autenticación y autorización
* Configurar reverse proxy (nginx)
* Monitoreo y logging centralizados
