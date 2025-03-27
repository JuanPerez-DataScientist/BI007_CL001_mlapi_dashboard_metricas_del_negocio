from fastapi import FastAPI
import os
from typing import List, Dict
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
#pandas only supports SQLAlchemy connectable (engine/connection)
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from fastapi.responses import JSONResponse

from generators import preprocesamiento, generar_metricas_mensuales, generar_metricas_clientes, generar_metricas_cohortes
app = FastAPI()

# Variables de entorno con nombres correctos
DB_HOST = os.getenv("DATABASE_HOST", "mysql_service")
DB_USER = os.getenv("DATABASE_USER", "root")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "admin")
DB_NAME = os.getenv("DATABASE_NAME", "empresa01")
DB_PORT = int(os.getenv("MYSQL_PORT", 3306))  # Agregar el puerto


def get_db_engine():
    try:
        db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_url)
        print("Conexión exitosa a la base de datos")
        return engine
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None
@app.get("/")
def read_root():
    return {"message": "API de Machine Learning!"}

@app.get("/ventas_mensuales")
def get_ventas_mensuales():
    engine = get_db_engine()
    if not engine:
        return JSONResponse(content={"error": "No se pudo conectar a la base de datos"}, status_code=500)
    try:
        df = pd.read_sql("SELECT * FROM onlineretail2b;", con=engine)
        result = preprocesamiento(df).to_dict(orient='records')
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/metricas_mensuales")
def get_metricas_mensuales():
    engine = get_db_engine()
    if not engine:
        return JSONResponse(content={"error": "No se pudo conectar a la base de datos"}, status_code=500)
    try:
        df = pd.read_sql("SELECT * FROM onlineretail2b;", con=engine)
        df = preprocesamiento(df)
        result = generar_metricas_mensuales(df).to_dict(orient='records')
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/metricas_clientes")
def get_metricas_clientes():
    engine = get_db_engine()
    if not engine:
        return JSONResponse(content={"error": "No se pudo conectar a la base de datos"}, status_code=500)
    try:
        df = pd.read_sql("SELECT * FROM onlineretail2b;", con=engine)
        df = preprocesamiento(df)
        result = generar_metricas_clientes(df).to_dict(orient='records')
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/metricas_cohortes")
def get_metricas_cohortes():
    engine = get_db_engine()
    if not engine:
        return JSONResponse(content={"error": "No se pudo conectar a la base de datos"}, status_code=500)
    try:
        df = pd.read_sql("SELECT * FROM onlineretail2b;", con=engine)
        df = preprocesamiento(df)
        result = generar_metricas_cohortes(df).to_dict(orient='records')
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
