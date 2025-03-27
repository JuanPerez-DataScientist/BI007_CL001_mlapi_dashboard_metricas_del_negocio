import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from datetime import datetime
from itertools import islice
from plotly.subplots import make_subplots
import requests

##################################################################
### Configure App
##################################################################

st.set_page_config(
    page_title="Analysis Dashboard", 
    page_icon="🧊", 
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.html("styles.html")
pio.templates.default = "plotly_white"

# from itertools.batched, used to produce rows of columns
def batched(iterable, n_cols):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n_cols < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n_cols)):
        yield batch

##################################################################
### Data
##################################################################


#@st.cache_data
def download_api_data():
    API_BASE_URL = "http://fastapi_service:8000"
    # Opciones de métricas
    # opcion = st.selectbox("Seleccionar Reporte:", [
    #  "Métricas Mensuales","Ventas Mensuales",  "Métricas de Clientes"
    # ])

    # Mapear opción con endpoint
    # endpoints = { 
    #     "Métricas Mensuales": "/metricas_mensuales",
    #     "Ventas Mensuales": "/ventas_mensuales",
    #     "Métricas de Clientes": "/metricas_clientes",
    # }

    # API_URL = f"{API_BASE_URL}{endpoints[opcion]}"
    API_URL = f"{API_BASE_URL}/metricas_mensuales"

    # Obtener datos de la API
    response = requests.get(API_URL)
    data_json = response.json()
    
    if isinstance(data_json, list) and len(data_json) > 0:
        df = pd.DataFrame(data_json)
    return df


#@st.cache_data
def transform_data_ventas(df):
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], yearfirst=True
    )
    df["FechaPrimeraCompra"] = pd.to_datetime(
        df["FechaPrimeraCompra"], yearfirst=True
    )
    for c in [
        "InvoiceNo",
        "Quantity",
        "UnitPrice",
        "CustomerID",
        "VentaTotal",
        "Cohorte",
    ]:
        df[c] = pd.to_numeric(df[c], "coerce")
    return df
#@st.cache_data
def transform_metricas_mensuales(df):
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], yearfirst=True
    )
    df["FechaPrimeraCompra"] = pd.to_datetime(
        df["FechaPrimeraCompra"], yearfirst=True
    )

    for c in [
        "InvoiceYearMonth",
        "IngresoBruto",
        "CantidadFacturas",
        "TotalProductos",
        "IngresoPromedioItem",
    ]:
        df[c] = pd.to_numeric(df[c], "coerce")

    return df
##################################################################
### App Widgets
##################################################################


def display_card(titulo, valor, porcentaje, comentario, moneda=False):
    with st.container(border=True):
        st.html(f'<span class="formato_tarjeta"></span>')
        tl = st.columns(1)[0]
        vl = st.columns(1)[0]
        pr = st.columns(1)[0]

        with tl:
            st.html(f'<span class="formato_titulo_tarjeta"></span>')
            st.markdown(f"{titulo}")

        with vl:
            st.html(f'<span class="formato_valor_tarjeta"></span>')
            st.markdown(f"{'$' if moneda else ''}{valor:.0f}")
     
        with pr:
            with st.container():
                st.html(f'<span class="formato_porcentaje_tarjeta"></span>')
                negative_gradient = float(porcentaje) < 0
                st.markdown(
                    f":{'red' if negative_gradient else 'green'}[{'▼' if negative_gradient else '▲'} {porcentaje} %]"
                )        

            with st.container():
                st.html(f'<span class="formato_comentario_tarjeta"></span>')
                st.markdown(f"{comentario}")

 
def display_cardlist(df, filtro_mes=None):
    """ Muestra todas las tarjetas en una sola fila con datos de un mes específico o del total """
    if filtro_mes:
        df_filtrado = df[df["InvoiceYearMonth"] == filtro_mes]
    else:
        df_filtrado = df  # Si no hay filtro, se usa todo el dataset (total anual)

    # Calculamos las métricas de la fila seleccionada
    total_ingreso = df_filtrado["IngresoBruto"].sum()
    cantidad_facturas = df_filtrado["CantidadFacturas"].sum()
    total_productos = df_filtrado["TotalProductos"].sum()
    if df_filtrado["IngresoPromedioItem"].sum() > 0: 
        ingreso_promedio = df_filtrado["IngresoPromedioItem"].sum() / df_filtrado["IngresoPromedioItem"].count() 
    else:
        0
    ingreso_neto = total_ingreso * 0.32  # Simulando un margen de 32%
    # Porcentajes de variación (puedes calcularlos en base a otro dataset de comparación)
    variacion_ingreso = 2.3
    variacion_facturas = -4.5
    variacion_productos = 8.5
    variacion_promedio = -10.2
    variacion_neto = 96.9

    # Comentarios adicionales
    comentario_propuesto = "Del Objetivo propuesto"
    comentario_anterior = "Respecto al año anterior"

    # Diseño de las tarjetas
    cols = st.columns(5)
    with cols[0]:
        display_card("Ingresos Brutos", 
                     total_ingreso, 
                     variacion_ingreso, 
                     comentario_anterior, 
                     moneda=True)
    with cols[1]:
        display_card("Cantidad Facturas", cantidad_facturas, variacion_facturas, comentario_anterior)
    with cols[2]:
        display_card("Total Productos", total_productos, variacion_productos, comentario_anterior)
    with cols[3]:
        display_card("Promedio Factura", ingreso_promedio, variacion_promedio, comentario_anterior, moneda=True)
    with cols[4]:
        display_card("Ingreso Neto", ingreso_neto, variacion_neto, comentario_propuesto, moneda=True)


##################################################################
### Main App
##################################################################

df = download_api_data()
#ventas_df = transform_data_ventas(df)
#metricas_mensuales_df = transform_metricas_mensuales(df)
metricas_mensuales_df= df
#all_symbols = list(ticker_df["Ticker"])

st.html('<h1 class="title">Métricas Mensuales</h1>')
# 
#st.table(df)
display_cardlist(df, "201104")

st.divider()

#display_symbol_history(ticker_df, history_dfs)
#display_overview(ticker_df)