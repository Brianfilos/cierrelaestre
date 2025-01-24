import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CIERRE", layout="wide")

st.title("Cargar y visualizar múltiples archivos CSV")

# Función para cargar y mostrar un archivo CSV
def cargar_csv(label):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file is not None:
        try:
            # Leer el archivo CSV con delimitador `;`
            df = pd.read_csv(file, encoding="latin1", sep=";")
            # Mostrar el DataFrame
            st.write(f"Vista previa del archivo: {label}")
            st.dataframe(df)
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None

def cargar_csv2(label):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file is not None:
        try:
            # Leer el archivo CSV con delimitador `;`
            df = pd.read_csv(file, encoding="latin1", sep=",")
            # Mostrar el DataFrame
            st.write(f"Vista previa del archivo: {label}")
            st.dataframe(df)
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None

def cargar_excel(label):
    file = st.file_uploader(label, type=["xlsx"], key=label)
    if file is not None:
        try:
            # Leer el archivo Excel
            df = pd.read_excel(file, engine="openpyxl")
            # Mostrar el DataFrame
            st.write(f"Vista previa del archivo: {label}")
            st.dataframe(df)
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None


st.write("2. Archivo CSV (Ejecución Presupuestal - Egresos)")
df2 = cargar_csv("Cargar archivo CSV (Ejecución Presupuestal Egresos)")

st.write("3. Archivo CSV (Ejecución Presupuestal - Ingresos)")
df3 = cargar_csv("Cargar archivo CSV (Ejecución Presupuestal Ingresos)")

st.write("4. Archivo CSV (EJECUCION CONSOLIDADA DE INGRESOS Y GASTOS)")
df4 = cargar_csv("Cargar archivo CSV (EJECUCION CONSOLIDADA DE INGRESOS Y GASTOS)")

st.write("5. Archivo CSV ( Boletín De Caja)")
df5 = cargar_excel("Cargar archivo XLSX ( Boletín De Caja)")

st.write("6. Archivo CSV (Reporte De Cuentas Por Pagar)")
df6 = cargar_csv("Cargar archivo CSV (Reporte De Cuentas Por Pagar)")

st.write("7. Archivo CSV (Comprobante De Egreso Consolidado Por Rubro)")
df7 = cargar_excel("Cargar archivo XLSX (Comprobante De Egreso Consolidado Por Rubro)")


# Verificar si no se cargaron archivos
if all(df is None or df.empty for df in [ df2, df3,df4,df5,df6,df7]):
    st.warning("Por favor, carga al menos un archivo CSV para continuar.")
    
if all(df is None or df.empty for df in [df2, df3, df4, df5, df6, df7]):
    st.warning("Por favor, carga al menos un archivo CSV para continuar.")

if df3 is not None:  # Verifica que df3 haya sido cargado correctamente
    if " FUENTE FINANCIACION" in df3.columns:  # Verifica que la columna ' FUENTE FINANCIACION' exista
        try:
            # Separar la columna ' FUENTE FINANCIACION' por el segundo guion "-"
            columnas_separadas = df3[" FUENTE FINANCIACION"].str.split("-", n=2, expand=True)
            
            # Combinar la primera y segunda partes para formar 'Parte_1'
            df3["Parte_1"] = columnas_separadas[0] + "-" + columnas_separadas[1]

            # Asignar el resto del texto después del segundo guion a 'Parte_2'
            df3["Parte_2"] = columnas_separadas[2] if columnas_separadas.shape[1] > 2 else None
            
            # Eliminar valores NaN o vacíos en 'Parte_1' si es necesario
            df3["Parte_1"].fillna('No Disponible', inplace=True)

            # Mostrar el DataFrame actualizado
            st.write("Vista previa del archivo con la columna ' FUENTE FINANCIACION' separada:")
            st.dataframe(df3)
        except Exception as e:
            st.error(f"Error al procesar la columna ' FUENTE FINANCIACION': {e}")
    else:
        st.warning("La columna ' FUENTE FINANCIACION' no existe en el archivo cargado.")
else:
    st.warning("No se ha cargado el archivo CSV (Ejecución Presupuestal Ingresos).")



if df3 is not None:  # Verifica que el DataFrame df3 esté cargado
    if "Parte_1" in df3.columns and "Parte_2" in df3.columns and "TOTAL RECAUDO" in df3.columns:  # Verifica que existan las columnas necesarias
        try:
            # Eliminar puntos como separadores de miles y reemplazar coma por punto como separador decimal
            df3["TOTAL RECAUDO"] = df3["TOTAL RECAUDO"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

            # Convertir la columna 'TOTAL RECAUDO' a numérico
            df3["TOTAL RECAUDO"] = pd.to_numeric(df3["TOTAL RECAUDO"], errors="coerce")

            # Reemplazar valores NaN con 0 en caso de errores
            df3["TOTAL RECAUDO"].fillna(0, inplace=True)

            # Agrupar por 'Parte_1' y 'Parte_2' y sumar 'TOTAL RECAUDO'
            df_agrupado = df3.groupby(["Parte_1", "Parte_2"])["TOTAL RECAUDO"].sum().reset_index()

            # Convertir a formato de pesos colombianos
            df_agrupado["Total Recaudo Agrupado"] = df_agrupado["TOTAL RECAUDO"].apply(
                lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            # Eliminar la columna duplicada si no es necesaria
            df_agrupado.drop(columns=["TOTAL RECAUDO"], inplace=True)

            # Mostrar el DataFrame agrupado
            st.write("total Recaudo por fuente de financiacion en ejecucion de ingresos:")
            st.dataframe(df_agrupado)
        except Exception as e:
            st.error(f"Error al procesar 'TOTAL RECAUDO': {e}")
    else:
        st.warning("No se encontraron las columnas 'Parte_1', 'Parte_2' o 'TOTAL RECAUDO' en el DataFrame.")
else:
    st.warning("No se ha cargado el archivo CSV (Ejecución Presupuestal Ingresos).")

if df3 is not None:  # Verifica que el DataFrame df3 esté cargado
    if "Parte_1" in df3.columns and "Parte_2" in df3.columns and "PRESUPUESTO DEFINITIVO" in df3.columns:  # Verifica que existan las columnas necesarias
        try:
            # Eliminar puntos como separadores de miles y reemplazar coma por punto como separador decimal
            df3["PRESUPUESTO DEFINITIVO"] = df3["PRESUPUESTO DEFINITIVO"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

            # Convertir la columna 'PRESUPUESTO DEFINITIVO' a numérico
            df3["PRESUPUESTO DEFINITIVO"] = pd.to_numeric(df3["PRESUPUESTO DEFINITIVO"], errors="coerce")

            # Reemplazar valores NaN con 0 en caso de errores
            df3["PRESUPUESTO DEFINITIVO"].fillna(0, inplace=True)

            # Agrupar por 'Parte_1' y 'Parte_2' y sumar 'PRESUPUESTO DEFINITIVO'
            df_agrupado2 = df3.groupby(["Parte_1", "Parte_2"])["PRESUPUESTO DEFINITIVO"].sum().reset_index()

            # Convertir a formato de pesos colombianos
            df_agrupado2["PRESUPUESTO DEFINITIVO Agrupado"] = df_agrupado2["PRESUPUESTO DEFINITIVO"].apply(
                lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            # Eliminar la columna duplicada si no es necesaria
            df_agrupado2.drop(columns=["PRESUPUESTO DEFINITIVO"], inplace=True)

            # Mostrar el DataFrame agrupado
            st.write("suma de presupuesto defintivo por fuente de financiacion en ejecucion de ingresos:")
            st.dataframe(df_agrupado2)
        except Exception as e:
            st.error(f"Error al procesar 'PRESUPUESTO DEFINITIVO': {e}")
    else:
        st.warning("No se encontraron las columnas 'Parte_1', 'Parte_2' o 'PRESUPUESTO DEFINITIVO' en el DataFrame.")
else:
    st.warning("No se ha cargado el archivo CSV (Ejecución Presupuestal Ingresos).")
    
if df2 is not None:  # Verifica que df2 haya sido cargado correctamente
    if "FUEN FINA." in df2.columns and "PAGOS" in df2.columns:  # Verifica que existan las columnas necesarias
        try:
            # Convertir los valores de 'PAGOS' a un formato numérico (eliminando puntos y reemplazando comas por puntos)
            df2['PAGOS'] = df2['PAGOS'].replace({r'\.': '', r',': '.'}, regex=True).astype(float)
            
            # Agrupar por 'FUEN FINA.' y sumar los valores de 'PAGOS'
            df2_agrupado = df2.groupby("FUEN FINA.")["PAGOS"].sum().reset_index()

            # Mostrar el DataFrame agrupado
            st.write("suma de pagos en ejecucion de egresos:")
            st.dataframe(df2_agrupado)
        except Exception as e:
            st.error(f"Error al agrupar los datos: {e}")
    else:
        st.warning("Las columnas 'FUEN FINA.' o 'PAGOS' no existen en el archivo cargado.")
else:
    st.warning("No se ha cargado el archivo CSV (Ejecución Presupuestal Egresos).")

if df2 is not None:  # Verifica que df2 haya sido cargado correctamente
    if "FUEN FINA." in df2.columns and "PTTO DEFI." in df2.columns:  # Verifica que existan las columnas necesarias
        try:
            # Limpiar los valores de 'PTTO DEFI.': eliminar '$', puntos de miles y convertir comas a puntos
            df2['PTTO DEFI.'] = df2['PTTO DEFI.'].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)
            
            # Agrupar por 'FUEN FINA.' y sumar los valores de 'PTTO DEFI.'
            df2_agrupado2 = df2.groupby("FUEN FINA.")["PTTO DEFI."].sum().reset_index()

            # Mostrar el DataFrame agrupado
            st.write("Suma de presupuesto definitivo en ejecución de egresos:")
            st.dataframe(df2_agrupado2)




        except Exception as e:
            st.error(f"Error al agrupar los datos: {e}")
    else:
        st.warning("Las columnas 'FUEN FINA.' o 'PTTO DEFI.' no existen en el archivo cargado.")
else:
    st.warning("No se ha cargado el archivo CSV (Ejecución Presupuestal Egresos).")

# Verificar si los DataFrames necesarios están creados
if 'df_agrupado2' in locals() and 'df2_agrupado2' in locals():
    # Asegurémonos de que las columnas a comparar sean del mismo tipo
    df_agrupado2["Parte_1"] = df_agrupado2["Parte_1"].astype(str)
    df2_agrupado2["FUEN FINA."] = df2_agrupado2["FUEN FINA."].astype(str)

    # Realizamos el merge entre ambos DataFrames por la columna de fuente de financiación
    df_comparado = pd.merge(df_agrupado2, df2_agrupado2, left_on="Parte_1", right_on="FUEN FINA.", how="inner")

    # Renombrar las columnas
    df_comparado.rename(columns={
        "Parte_1": "FUENTE DE FINANCIACION",
        "Parte_2": "NOMBRE DE LA FUENTE",
        "PRESUPUESTO DEFINITIVO Agrupado": "PRESUPUESTO EN INGRESOS",
        "PTTO DEFI.": "PRESUPUESTO EN GASTOS"
    }, inplace=True)

    # Convertimos las columnas numéricas a tipo flotante para hacer la comparación
    df_comparado["PRESUPUESTO EN INGRESOS"] = df_comparado["PRESUPUESTO EN INGRESOS"].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)
    df_comparado["PRESUPUESTO EN GASTOS"] = df_comparado["PRESUPUESTO EN GASTOS"].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)

    # Calculamos la diferencia entre ambos valores
    df_comparado["Diferencia"] = df_comparado["PRESUPUESTO EN INGRESOS"] - df_comparado["PRESUPUESTO EN GASTOS"]

    # Convertimos los resultados a formato de pesos colombianos
    df_comparado["PRESUPUESTO EN INGRESOS"] = df_comparado["PRESUPUESTO EN INGRESOS"].apply(
        lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    df_comparado["PRESUPUESTO EN GASTOS"] = df_comparado["PRESUPUESTO EN GASTOS"].apply(
        lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    df_comparado["Diferencia"] = df_comparado["Diferencia"].apply(
        lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    # Eliminar la columna 'FUEN FINA.'
    df_comparado = df_comparado.drop(columns=["FUEN FINA."])

    # Mostrar el DataFrame con las diferencias
    st.write("Comparación entre el presupuesto en ingresos y el presupuesto en gastos:")
    st.dataframe(df_comparado)
else:
    st.error("Error: Los DataFrames 'df_agrupado2' y 'df2_agrupado2' no están creados o definidos.")

# Verificar si los DataFrames necesarios están creados para la segunda comparación
if 'df_agrupado' in locals() and 'df2_agrupado' in locals():
    # Asegurémonos de que las columnas 'Total Recaudo Agrupado' y 'PAGOS' sean numéricas
    df_agrupado["Total Recaudo Agrupado"] = df_agrupado["Total Recaudo Agrupado"].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)
    df2_agrupado["PAGOS"] = df2_agrupado["PAGOS"].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)

    # Realizamos el merge entre df_agrupado y df2_agrupado por la columna de fuente de financiación
    df_comparado_recaudo_pagos = pd.merge(df_agrupado, df2_agrupado, left_on="Parte_1", right_on="FUEN FINA.", how="inner")

    # Calcular la diferencia entre 'Total Recaudo Agrupado' y 'PAGOS'
    df_comparado_recaudo_pagos["Recaudo - Pagos (ECB)"] = df_comparado_recaudo_pagos["Total Recaudo Agrupado"] - df_comparado_recaudo_pagos["PAGOS"]

    # Convertir los resultados a formato de pesos colombianos
    df_comparado_recaudo_pagos["Total Recaudo Agrupado"] = df_comparado_recaudo_pagos["Total Recaudo Agrupado"].apply(
        lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    df_comparado_recaudo_pagos["PAGOS"] = df_comparado_recaudo_pagos["PAGOS"].apply(
        lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    df_comparado_recaudo_pagos["Recaudo - Pagos (ECB)"] = df_comparado_recaudo_pagos["Recaudo - Pagos (ECB)"].apply(
        lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    # Eliminar la columna 'FUEN FINA.'
    df_comparado_recaudo_pagos = df_comparado_recaudo_pagos.drop(columns=["FUEN FINA."])

    # Mostrar el DataFrame con la diferencia (Recaudo - Pagos (ECB))
    st.write("Diferencia entre Recaudo y Pagos por fuente de financiación:")
    st.dataframe(df_comparado_recaudo_pagos)
else:
    st.error("Error: Los DataFrames 'df_agrupado' y 'df2_agrupado' no están creados o definidos.")
