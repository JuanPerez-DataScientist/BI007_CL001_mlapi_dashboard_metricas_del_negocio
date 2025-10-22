<h1 align='center'>
 <b>Métricas y KPIs para Inteligencia de Negocios </b>
</h1>


## **Generador de Informes Interactivos de Métricas y KPIs para BI**


## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)
### General Info
***
 
<b>Sistema Generador de Informes Interactivos de Inteligencia de Negocios GIIN</b> ejecutado sobre una arquitectura de microservicios en contenedores Docker donde se consumen datos de una base de datos  MySQL para aplicar Aprendizaje Automatizado (ML) e implementar una API con FastAPI que disponibiliza las métricas y KPIs de un negocio retail. Estas métricas y KPIs son consumidas por un tablero interactivo web (Dashboard) implementado en Streamlit.

Generador de Informes Interactivos de Métricas y KPIs para BI ejecutado sobre una arquitectura de microservicios  en contenedores Docker con fuente de datos  MySQL de un negocio retail sobre los que se aplica Aprendizaje Automatizado (ML) en una API con FastAPI que disponibiliza las métricas y KPIs para un tablero interactivo web con  Streamlit.


### Screenshot
![Image text](https://www.united-internet.de/fileadmin/user_upload/Brands/Downloads/Logo_IONOS_by.jpg)
## Technologies
***
A list of technologies used within the project:
* [Python](https://example.com): Version 3.9.x
* [Google Colab](https://example.com): Version x.x
* [Numpy](http://www.numpy.org/): Version 1.20.3
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/visualization.html): Version 1.5.3
* [Seaborn](https://seaborn.pydata.org/): Version 0.12.2
* [Matplotlib](https://matplotlib.org/stable/): Version 3.8.1
* [Plotly](https://matplotlib.org/stable/): Version 5.15.0
* [Statsmodels](https://www.statsmodels.org/stable/index.html): Version 0.14.0
* [Scipy](https://docs.scipy.org/doc/scipy/): Version 1.11.3
## Resumen

El objetivo es proporcionar un entorno reproducible donde cada servicio corre en su propio contenedor y se comunican mediante la red definida en `compose.yaml`. Ideal para prototipos, demos y experimentación con ML/data.

## Estructura del repositorio


## Requisitos previos

- Docker instalado (Docker Desktop o Engine).
- Docker Compose (moderno: `docker compose`) o la versión legacy `docker-compose`.
- La estructura de carpetas y archivos general que contiene a todos los contenedores interconectados.
- Las carpetas fastapi_backend, jupyter_backend y streamlit_frontend deben contener los archivos necesarios para cada servicio y ser copiadas respectivamente en las carpetas fastapi_container, jupyter_container y streamlit_container 


## Quick start

Desde la raíz del repositorio:

```powershell
# Construir y levantar todos los servicios en primer plano
docker compose up --build

# O en background
docker compose up -d --build

# Parar y eliminar recursos (contenedores, redes y volúmenes definidos en compose)
docker compose down -v
```

Después de levantar los servicios, habitualmente están disponibles en:

- FastAPI: [http://localhost:8000](http://localhost:8000)
- Jupyter: [http://localhost:8888](http://localhost:8888) (revisa el token en los logs)
- Streamlit: [http://localhost:8501](http://localhost:8501)

## Collaboration
***
Give instructions on how to collaborate with your project.
> Maybe you want to write a quote in this part. 
> It should go over several rows?
> This is how you do it.
## FAQs
***
A list of frequently asked questions
1. **This is a question in bold**
Answer of the first question with _italic words_. 
2. __Second question in bold__ 
To answer this question we use an unordered list:
* First point
* Second Point
* Third point
3. **Third question in bold**
Answer of the third question with *italic words*.
4. **Fourth question in bold**
| Headline 1 in the tablehead | Headline 2 in the tablehead | Headline 3 in the tablehead |
|:--------------|:-------------:|--------------:|
| text-align left | text-align center | text-align right |