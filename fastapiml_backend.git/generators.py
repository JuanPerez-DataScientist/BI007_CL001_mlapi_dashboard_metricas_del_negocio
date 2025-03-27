from datetime import datetime, timedelta
import pandas as pd

def preprocesamiento(df):
    """Realiza limpieza y procesamiento de datos de ventas."""
    df = df.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce')
    df["VentaTotal"] = df["Quantity"] * df["UnitPrice"]
    df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: 100*date.year + date.month)
    # Crear variable  FechaPrimeraCompra y MesAñoPriemeraCompra por cliente
    metricas_clientes_df= df.groupby(['CustomerID'])['InvoiceDate'].min().reset_index()
    metricas_clientes_df.columns = ['CustomerID','FechaPrimeraCompra']
    #converting the type of Invoice Date Field from string to datetime.
    metricas_clientes_df['FechaPrimeraCompra'] = pd.to_datetime(metricas_clientes_df['FechaPrimeraCompra'])
    metricas_clientes_df['YearMonthPrimeraCompra'] = metricas_clientes_df['FechaPrimeraCompra'].map(lambda date: 100*date.year + date.month)
    #La cohorte de un cliente es tambien el mes de su primera compra
    # metricas_clientes_df['Cohorte'] = metricas_clientes_df['FechaPrimeraCompra'].map(lambda date: 100*date.year + date.month)
    metricas_clientes_df['Cohorte']= metricas_clientes_df['YearMonthPrimeraCompra']
    df = pd.merge(df, metricas_clientes_df, on='CustomerID')
    df['tipoCliente'] = 'Nuevo'
    df.loc[df['InvoiceYearMonth']>df['Cohorte'],'tipoCliente'] = 'Repite'
    #df['InvoiceYearMonth'] = df['InvoiceYearMonth'].astype(str)
    # Guardarmos el DataFrame en un archivo CSV
    #df.to_csv('ventas_mensuales.csv', index=False)
    df['FechaPrimeraCompra'] = df['FechaPrimeraCompra'].astype(str)
    df['InvoiceDate'] = df['InvoiceDate'].astype(str)


    return df

def generar_metricas_mensuales(df):
    """Calcula métricas mensuales y retorna un DataFrame con resultados."""
    
    #df['InvoiceYearMonth'] = df['InvoiceDate'].dt.to_period("M")
    metricas_mensuales_df = df.groupby('InvoiceYearMonth').agg(
        IngresoBruto=('VentaTotal', 'sum'),
        CantidadFacturas=('InvoiceNo', 'nunique'),
        TotalProductos=('Quantity', 'sum'),
        IngresoPromedioItem=('VentaTotal', 'mean'),
        ClientesActivos=('CustomerID', 'nunique')
    ).reset_index()
    metricas_mensuales_df.to_csv('metricas_mensuales', index=False)
    metricas_mensuales_df['InvoiceYearMonth'] = metricas_mensuales_df['InvoiceYearMonth'].astype(str)
    return metricas_mensuales_df

def generar_metricas_clientes(df):
    """Calcula métricas de clientes y retorna un DataFrame con resultados."""
    metricas_clientes_df = df.groupby("CustomerID").agg(
        TotalGasto=('VentaTotal', 'sum'),
        CantidadCompras=('InvoiceNo', 'nunique'),
        PromedioGastoCompra=('VentaTotal', 'mean')
    ).reset_index()
    #metricas_clientes_df.to_csv('metricas_clientes.csv', index=False)
    return metricas_clientes_df

def generar_metricas_cohortes(df):
    """Genera un análisis de cohortes basado en las fechas de compra de clientes."""
    #df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: 100*date.year + date.month)
    #df['CohortMonth'] = df.groupby("CustomerID")['InvoiceDate'].transform('min').dt.to_period("M")
    #df['InvoiceYearMonth'] = df['InvoiceDate'].dt.to_period("M")
    #cohort_counts = df.groupby(['CohortMonth', 'InvoiceYearMonth']).agg(NClientes=('CustomerID', 'nunique')).reset_index()
    metricas_cohortes_df = df.groupby(['Cohorte']).agg(ClientesCohorte=('CustomerID', 'nunique')).reset_index()
    #metricas_cohortes_df.to_csv('metricas_cohortes.csv', index=False)
    return metricas_cohortes_df


