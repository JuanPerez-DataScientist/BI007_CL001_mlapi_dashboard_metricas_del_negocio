from datetime import datetime, timedelta
import pandas as pd
import numpy as np

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
    #La cohorte de un cliente es tambien el añomes de su primera compra
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
# ------------- fin preprocesamiento ---------#

def generar_ventas_mensuales(df):
    """ Retorna un DataFrame con ventas mensuales."""
    #Elije solo unos campos para evitar hacer muy grande el df 
    ventas_mensuales_df = df[['CustomerID','InvoiceYearMonth','VentaTotal']]
    
    return ventas_mensuales_df
# ------------- fin generar_ventas_mensuales --------- #

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

    #identify which users are active by looking at their revenue per month
    compras_clientes = df.groupby(['CustomerID','InvoiceYearMonth'])['VentaTotal'].sum().reset_index()
    #create retention matrix with crosstab
    matriz_retenciones = pd.crosstab(compras_clientes['CustomerID'], compras_clientes['InvoiceYearMonth']).reset_index()
 
    # Seleccionar los meses a analizar
    months = matriz_retenciones.columns[1:]

    # Crear DataFrame con métricas de retención
    retenciones_df = pd.DataFrame({
        'InvoiceYearMonth': months[1:].astype(int),
        'TotalClientes': [matriz_retenciones[months[i]].sum() for i in range(len(months) - 1)],
        'ClientesRetenidos': [
            matriz_retenciones[(matriz_retenciones[months[i+1]] > 0) & (matriz_retenciones[months[i]] > 0)][months[i+1]].sum()
            for i in range(len(months) - 1)
        ]
    })
    
    # Asignar datos al DataFrame de métricas mensuales
    metricas_mensuales_df[['TotalClientes', 'ClientesRetenidos']] = retenciones_df[['TotalClientes', 'ClientesRetenidos']]
    #metricas_mensuales_df.to_csv('metricas_mensuales', index=False)
    metricas_mensuales_df['InvoiceYearMonth'] = metricas_mensuales_df['InvoiceYearMonth'].astype(str)
    metricas_mensuales_df = metricas_mensuales_df.replace([np.inf, -np.inf], np.nan).fillna(0)
    return metricas_mensuales_df
# ------------- fin generar_metricas_mensuales ---------#


def generar_metricas_clientes(df):
    """Calcula métricas de clientes y retorna un DataFrame con resultados."""
    metricas_clientes_df = df.groupby("CustomerID").agg(
        IngresosTotal=('VentaTotal', 'sum'),
        CantidadCompras=('InvoiceNo', 'nunique'),
        MontoPromedioItem=('VentaTotal', 'mean')
    ).reset_index()
    #metricas_clientes_df.to_csv('metricas_clientes.csv', index=False)
    meses_por_clientes_df = df.groupby('CustomerID')['InvoiceYearMonth'].nunique().reset_index(name='MesesDeCompras')
    metricas_clientes_df = metricas_clientes_df.merge(meses_por_clientes_df, on='CustomerID')
    metricas_clientes_df['ARPUCliente'] = metricas_clientes_df['IngresosTotal'] / metricas_clientes_df['MesesDeCompras']

    return metricas_clientes_df
# ------------- fin generar_metricas_clientes ---------#

def generar_metricas_cohortes(df):
    """Genera un análisis de cohortes basado en las fechas de compra de clientes."""
    #df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: 100*date.year + date.month)
    #df['CohortMonth'] = df.groupby("CustomerID")['InvoiceDate'].transform('min').dt.to_period("M")
    #df['InvoiceYearMonth'] = df['InvoiceDate'].dt.to_period("M")
    #cohort_counts = df.groupby(['CohortMonth', 'InvoiceYearMonth']).agg(NClientes=('CustomerID', 'nunique')).reset_index()
    metricas_cohortes_df = df.groupby(['Cohorte']).agg(ClientesCohorte=('CustomerID', 'nunique')).reset_index()
    # Crear la matriz de retención con crosstab y añadir el cohorte de compra

    
    metricas_clientes_df = pd.DataFrame(generar_metricas_clientes(df))
    #identify which users are active by looking at their revenue per month
    compras_clientes = df.groupby(['CustomerID','InvoiceYearMonth'])['VentaTotal'].sum().reset_index()
    compras_cohorte = pd.crosstab(compras_clientes['CustomerID'], compras_clientes['InvoiceYearMonth']).reset_index()
    
    compras_cohorte = compras_cohorte.merge(metricas_clientes_df[['CustomerID', 'InvoiceYearMonth']], on='CustomerID')
    #create retention matrix with crosstab
    matriz_retenciones = pd.crosstab(compras_clientes['CustomerID'], compras_clientes['InvoiceYearMonth']).reset_index()
    months = matriz_retenciones.columns[1:]
    # Renombrar columnas usando list comprehension
    compras_cohorte.columns = [f"m_{col}" if col != 'InvoiceYearMonth' else col for col in compras_cohorte.columns]

    # Calcular tasas de retención por cohorte
    retention_array = []
    for mes in months:
        cohort_data = {'ClientesCohorte': compras_cohorte[compras_cohorte['InvoiceYearMonth'] == mes].shape[0]}

        # Si no hay clientes en la cohorte, asignar 0 a la retención
        if cohort_data['ClientesCohorte'] > 0:
            cohort_data[mes] = 1  # Retención total en el mes inicial
            cohort_mask = compras_cohorte['InvoiceYearMonth'] == mes
            for next_mes in months[months > mes]:
                # Si no hay clientes retenidos, asignar 0
                cohort_data[next_mes] = np.round(
                    compras_cohorte.loc[cohort_mask, f"m_{next_mes}"].gt(0).sum() / cohort_data['ClientesCohorte'], 2
                ) if cohort_data['ClientesCohorte'] > 0 else 0
        else:
            # Si no hay clientes para esta cohorte, asignar 0
            cohort_data[mes] = 0

        retention_array.append(cohort_data)

        # Crear DataFrame de tasas de retención
        tasas_retencion_cohortes_df = pd.DataFrame(retention_array, index=months)

        # Mostrar tabla de retención
        tasas_retencion_cohortes_df


    return tasas_retencion_cohortes_df
# ------------- fin generar_metricas_cohortes ---------#



