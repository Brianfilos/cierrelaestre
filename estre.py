import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CIERRE PRESUPUESTAL ESTRELLA", layout="wide")

st.title("Cargue Archivos para Cruce")

# Función para cargar y mostrar un archivo CSV
def cargar_csv(label, sep_char=","):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file is not None:
        try:
            # Leer el archivo CSV con delimitador especificado
            df = pd.read_csv(file, encoding="latin1", sep=sep_char, skiprows=5)
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None

# Función para cargar y mostrar un archivo CSV
def cargar_csv2(label, sep_char=","):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file is not None:
        try:
            # Leer el archivo CSV con delimitador especificado
            df = pd.read_csv(file, encoding="latin1", sep=sep_char, skiprows=4)
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
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None

# Lista de configuraciones de archivos
archivos = [
    {
        "titulo": "Archivo CSV (Ejecución Presupuestal - Egresos):",
        "color": "green",
        "funcion_carga": cargar_csv,
        "parametro": "Cargar archivo CSV (Ejecución Presupuestal Egresos)",
        "nombre_df": "df_egresos",
        "sep_char": ";"
    },
    {
        "titulo": "Archivo CSV (Ejecución Presupuestal - Ingresos):",
        "color": "red",
        "funcion_carga": cargar_csv,
        "parametro": "Cargar archivo CSV (Ejecución Presupuestal Ingresos)",
        "nombre_df": "df_ingresos",
        "sep_char": ";"
    },
    {
        "titulo": "Archivo CSV (EJECUCION CONSOLIDADA DE INGRESOS Y GASTOS):",
        "color": "orange",
        "funcion_carga": cargar_csv2,
        "parametro": "Cargar archivo CSV (EJECUCION CONSOLIDADA DE INGRESOS Y GASTOS)",
        "nombre_df": "df_consolidado_i_e",
        "sep_char": ";"
    },
    {
        "titulo": "Archivo CSV (Reporte De Cuentas Por Pagar):",
        "color": "blue",
        "funcion_carga": cargar_csv,
        "parametro": "Cargar archivo CSV (Reporte De Cuentas Por Pagar)",
        "nombre_df": "df_cuentas_pagar",
        "sep_char": ";"
    },
     {
        "titulo": "Archivo CSV (Boletin de caja):",
        "color": "blue",
        "funcion_carga": cargar_excel,
        "parametro": "Cargar archivo XLSX (Boletin de caja)",
        "nombre_df": "df_boletin_caja",
    },
    {
        "titulo": "Archivo EXCEL (Comprobante De Egreso Consolidado Por Rubro):",
        "color": "violet",
        "funcion_carga": cargar_excel,
        "parametro": "Cargar archivo XLSX (Comprobante De Egreso Consolidado Por Rubro)",
        "nombre_df": "df_egreso_rubro",
    },
    {
        "titulo": "Archivo EXCEL (Archivo Conciliaciones Bancarias Consolidadas):",
        "color": "gray",
        "funcion_carga": cargar_excel,
        "parametro": "Cargar archivo XLSX (Archivo Conciliaciones Bancarias Consolidadas)",
        "nombre_df": "df_conciliaciones",
    },
]

# Iterar sobre los archivos para cargarlos con nombres específicos
for archivo in archivos:
    st.header(archivo["titulo"], divider=archivo["color"])

    # Cargar el archivo usando la función correspondiente
    if archivo.get("sep_char"):
        globals()[archivo["nombre_df"]] = archivo["funcion_carga"](archivo["parametro"], sep_char=archivo["sep_char"])
    else:
        globals()[archivo["nombre_df"]] = archivo["funcion_carga"](archivo["parametro"])

    # Mostrar la tabla solo si el usuario selecciona la opción
    if globals()[archivo["nombre_df"]] is not None:
        if st.checkbox(f"Mostrar vista previa de {archivo['titulo']}"):
            st.write(f"Vista previa de {archivo['nombre_df']}:")
            st.dataframe(globals()[archivo["nombre_df"]])
    else:
        st.write(f"El archivo {archivo['titulo']} se ha cargado correctamente. Marca la casilla para ver la vista previa.")

# Verificar si los archivos fueron cargados correctamente
def archivos_cargados():
    return all(df is not None and not df.empty for df in [
        globals().get("df_egresos"),
        globals().get("df_ingresos"),
        globals().get("df_consolidado_i_e"),
        globals().get("df_cuentas_pagar"),
        globals().get("df_egreso_rubro"),
        globals().get("df_conciliaciones"),
        globals().get("df_boletin_caja")
    ])

if not archivos_cargados():
    st.warning("Por favor, carga al menos un archivo CSV para continuar.")

#st.title("PROCESAMIENTO EJECUCION DE INGRESOS:")

# Ensure 'FUENTE FINANCIACION' column is of type string
globals()["df_ingresos"][' FUENTE FINANCIACION'] = globals()["df_ingresos"][' FUENTE FINANCIACION'].astype(str)

# Custom function to split by the first two hyphens
def split_by_first_two_hyphens(text):
    parts = text.split("-", 2)
    if len(parts) > 2:
        return parts[0] + "-" + parts[1], parts[2]
    elif len(parts) > 1:
        return parts[0] + "-" + parts[1], ""
    else:
        return parts[0], ""

# Apply the custom function to split the column
columnas_separadas = globals()["df_ingresos"][" FUENTE FINANCIACION"].apply(split_by_first_two_hyphens)
columnas_separadas = pd.DataFrame(columnas_separadas.tolist(), columns=["Parte_1", "Parte_2"])

# Asignar los valores a las nuevas columnas
globals()["df_ingresos"]["Parte_1"] = columnas_separadas["Parte_1"]
globals()["df_ingresos"]["Parte_2"] = columnas_separadas["Parte_2"]

# Reordenar las columnas según el orden deseado
columnas_ordenadas = ["CCPET","Parte_1", "Parte_2","CCP","CONS.","C. RES"," NOMBRE","INICIAL","ADICIONES","REDUCCIONES","PRESUPUESTO DEFINITIVO","RECAUDO ANTERIOR","TOTAL RECAUDO","SALDO POR EJECUTAR","SALDO POR EXCESO"]
globals()["df_ingresos"] = globals()["df_ingresos"][columnas_ordenadas]

# Mostrar las columnas 'Parte_1', 'Parte_2' 
st.header("DF INGRESOS CON COLUMNAS SEPARADAS", divider="blue")
st.dataframe(globals()["df_ingresos"][columnas_ordenadas])


if globals().get("df_ingresos") is not None and "TOTAL RECAUDO" in globals()["df_ingresos"].columns:
    try:
        # Convertir 'TOTAL RECAUDO' a numérico
        globals()["df_ingresos"]["TOTAL RECAUDO"] = globals()["df_ingresos"]["TOTAL RECAUDO"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        globals()["df_ingresos"]["TOTAL RECAUDO"] = pd.to_numeric(globals()["df_ingresos"]["TOTAL RECAUDO"], errors="coerce")
        globals()["df_ingresos"]["TOTAL RECAUDO"].fillna(0, inplace=True)

        # Agrupar por 'Parte_1' y 'Parte_2' y sumar 'TOTAL RECAUDO'
        df_agrupado = globals()["df_ingresos"].groupby(["Parte_1", "Parte_2"])["TOTAL RECAUDO"].sum().reset_index()

        # Convertir a formato de pesos colombianos
        df_agrupado["Total Recaudo Agrupado"] = df_agrupado["TOTAL RECAUDO"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Mostrar las columnas 'Parte_1', 'Parte_2' y 'Total Recaudo Agrupado'
        st.header("Total Recaudo por fuente de financiación en ejecución de ingresos:", divider="blue")
        st.dataframe(df_agrupado[["Parte_1", "Parte_2", "Total Recaudo Agrupado"]])
    except Exception as e:
        st.error(f"Error al procesar 'TOTAL RECAUDO': {e}")
else:
    st.warning("No se ha encontrado la columna 'TOTAL RECAUDO' en el archivo cargado.")



if globals().get("df_ingresos") is not None:  # Verifica que el DataFrame df_ingresos esté cargado
    if "Parte_1" in globals().get("df_ingresos").columns and "Parte_2" in globals().get("df_ingresos").columns and "PRESUPUESTO DEFINITIVO" in globals().get("df_ingresos").columns:  # Verifica que existan las columnas necesarias
        try:
            # Eliminar puntos como separadores de miles y reemplazar coma por punto como separador decimal
            globals().get("df_ingresos")["PRESUPUESTO DEFINITIVO"] = globals().get("df_ingresos")["PRESUPUESTO DEFINITIVO"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

            # Convertir la columna 'PRESUPUESTO DEFINITIVO' a numérico
            globals().get("df_ingresos")["PRESUPUESTO DEFINITIVO"] = pd.to_numeric(globals().get("df_ingresos")["PRESUPUESTO DEFINITIVO"], errors="coerce")

            # Reemplazar valores NaN con 0 en caso de errores
            globals().get("df_ingresos")["PRESUPUESTO DEFINITIVO"].fillna(0, inplace=True)

            # Agrupar por 'Parte_1' y 'Parte_2' y sumar 'PRESUPUESTO DEFINITIVO'
            df_agrupado2 = globals().get("df_ingresos").groupby(["Parte_1", "Parte_2"])["PRESUPUESTO DEFINITIVO"].sum().reset_index()

            # Convertir a formato de pesos colombianos
            df_agrupado2["PRESUPUESTO DEFINITIVO Agrupado"] = df_agrupado2["PRESUPUESTO DEFINITIVO"].apply(
                lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            # Eliminar la columna duplicada si no es necesaria
            df_agrupado2.drop(columns=["PRESUPUESTO DEFINITIVO"], inplace=True)

            # Mostrar el DataFrame agrupado
            st.header("Suma de presupuesto definitivo por fuente de financiación en ejecución de ingresos:",divider="blue")
            st.dataframe(df_agrupado2)
        except Exception as e:
            st.error(f"Error al procesar 'PRESUPUESTO DEFINITIVO': {e}")
    else:
        st.warning("No se encontraron las columnas 'Parte_1', 'Parte_2' o 'PRESUPUESTO DEFINITIVO' en el DataFrame.")
else:
    st.warning("No se ha cargado el archivo CSV (Ejecución Presupuestal Ingresos).")


st.title("PROCESAMIENTO EJECUCION DE EGRESOS:")

if globals().get("df_egresos") is not None:  
    # Procesar los pagos
    if "FUEN FINA." in globals().get("df_egresos").columns and "PAGOS" in globals().get("df_egresos").columns and "CCPET" in globals().get("df_egresos").columns:
        try:
            
            # Convertir los valores de 'PAGOS' a formato numérico (eliminando puntos y reemplazando comas por puntos)
            globals().get("df_egresos")['PAGOS'] = globals().get("df_egresos")['PAGOS'].replace({r'\.': '', r',': '.'}, regex=True).astype(float)
            
            # Agrupar por 'FUEN FINA.' y 'CLASIFICACION GASTO' y sumar los valores de 'PAGOS'
            df2_agrupado = globals().get("df_egresos").groupby("FUEN FINA.")["PAGOS"].sum().reset_index()
            
            
        except Exception as e:
            st.error(f"Error al agrupar los datos: {e}")
    else:
        st.warning("Las columnas 'FUEN FINA.', 'PAGOS' o 'CCPET' no existen en el archivo cargado.")

if globals().get("df_egresos") is not None:  
    # Procesar los pagos
    if "FUEN FINA." in globals().get("df_egresos").columns and "PAGOS" in globals().get("df_egresos").columns and "CCPET" in globals().get("df_egresos").columns:
        try:
            # Extraer los primeros 3 dígitos de 'CCPET' y colocarlos en 'CLASIFICACION GASTO'
            globals().get("df_egresos")["CLASIFICACION GASTO"] = globals().get("df_egresos")["CCPET"].astype(str).str[:3]

            # Convertir los valores de 'PAGOS' a formato numérico (eliminando puntos y reemplazando comas por puntos)
            globals().get("df_egresos")['PAGOS'] = globals().get("df_egresos")['PAGOS'].replace({r'\.': '', r',': '.'}, regex=True).astype(float)
            
            # Agrupar por 'FUEN FINA.' y 'CLASIFICACION GASTO' y sumar los valores de 'PAGOS'
            df2_agrupado_CLASI = globals().get("df_egresos").groupby(["FUEN FINA.", "CLASIFICACION GASTO"])["PAGOS"].sum().reset_index()

            
        except Exception as e:
            st.error(f"Error al agrupar los datos: {e}")
    else:
        st.warning("Las columnas 'FUEN FINA.', 'PAGOS' o 'CCPET' no existen en el archivo cargado.")

    # Procesar el presupuesto definitivo
    if "FUEN FINA." in globals().get("df_egresos").columns and "PTTO DEFI." in globals().get("df_egresos").columns:
        try:
            # Limpiar los valores de 'PTTO DEFI.': eliminar '$', puntos de miles y convertir comas a puntos
            globals().get("df_egresos")['PTTO DEFI.'] = globals().get("df_egresos")['PTTO DEFI.'].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)
            
            # Agrupar por 'FUEN FINA.' y sumar los valores de 'PTTO DEFI.'
            df2_agrupado2 = globals().get("df_egresos").groupby("FUEN FINA.")["PTTO DEFI."].sum().reset_index()

            # Mostrar el DataFrame agrupado
            st.header("Suma de presupuesto definitivo en ejecución de egresos:",divider="red")
            st.dataframe(df2_agrupado2)

        except Exception as e:
            st.error(f"Error al agrupar los datos: {e}")
    else:
        st.warning("Las columnas 'FUEN FINA.' o 'PTTO DEFI.' no existen en el archivo cargado.")

# Comparación entre ingresos y egresos
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
        st.header("VALIDADOR DE INGRESOS Y GASTOS :", divider="gray")
        st.dataframe(df_comparado)
    else:
        st.error("Error: Los DataFrames 'df_agrupado2' y 'df2_agrupado2' no están creados o definidos.")

# Comparación entre recaudo y pagos
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
        st.header("Diferencia entre Recaudo y Pagos por fuente de financiación:", divider="gray")
        st.dataframe(df_comparado_recaudo_pagos)
    else:
        st.error("Error: Los DataFrames 'df_agrupado' y 'df2_agrupado' no están creados o definidos.")

# Función para extraer la fuente de los rubros y la clasificación del gasto
def extraer_fuente_y_clasificacion(rubro):
    fuente = None
    clasificacion = None
    if isinstance(rubro, str):  # Verifica si el valor es una cadena
        if "." in rubro:  # Verifica si hay al menos un punto en el valor
            partes = rubro.split(".")  # Divide por puntos
            fuente = partes[-1][-5:]  # Toma los últimos 5 caracteres de la última parte
        clasificacion = rubro[:3]  # Toma los primeros 3 caracteres
    return fuente, clasificacion  # Devuelve la fuente y la clasificación

   
# Función para extraer la fuente de los rubros
def extraer_fuente(rubro):
    if isinstance(rubro, str):  # Verifica si el valor es una cadena
        if "." in rubro:  # Verifica si hay al menos un punto en el valor
            partes = rubro.split(".")  # Divide por puntos
            return partes[-1][-5:]  # Toma los últimos 5 caracteres de la última parte
    return None  # Devuelve None si el valor no es válido

# Aseguramos que los valores de 'RUBRO' sean cadenas y aplicamos la función
if globals().get("df_cuentas_pagar") is not None:
    globals().get("df_cuentas_pagar")["FUENTE"] = globals().get("df_cuentas_pagar")["RUBRO"].astype(str).apply(extraer_fuente)

    # Reemplazamos los valores 'None' con un valor vacío o por defecto si es necesario
    globals().get("df_cuentas_pagar")["FUENTE"].fillna("", inplace=True)

    # Eliminar símbolos y convertir 'PAGO' a numérico
    globals().get("df_cuentas_pagar")["PAGO"] = globals().get("df_cuentas_pagar")["PAGO"].str.replace("[^\d,.-]", "", regex=True)
    globals().get("df_cuentas_pagar")["PAGO"] = globals().get("df_cuentas_pagar")["PAGO"].str.replace(r"\.(?=\d{3})", "", regex=True).str.replace(",", ".").astype(float)

    # Agrupar por 'FUENTE' y sumar los valores de 'PAGO'
    df_cuentas_pagar_agrupado = globals().get("df_cuentas_pagar").groupby("FUENTE")["PAGO"].sum().reset_index(name="Total Pagos")

    # Convertir a formato de pesos colombianos
    df_cuentas_pagar_agrupado["Total Pagos"] = df_cuentas_pagar_agrupado["Total Pagos"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.header("TOTAL DE PAGOS POR FUENTE EN CUENTAS POR PAGAR:", divider="green")
    st.dataframe(df_cuentas_pagar_agrupado)

# Función para extraer la fuente de los rubros
def extraer_fuente(rubro):
    if isinstance(rubro, str):  # Verifica si el valor es una cadena
        if "." in rubro:  # Verifica si hay al menos un punto en el valor
            partes = rubro.split(".")  # Divide por puntos
            return partes[-1][-5:]  # Toma los últimos 5 caracteres de la última parte
    return None  # Devuelve None si el valor no es válido

# Aseguramos que los valores de 'RUBRO' sean cadenas y aplicamos la función
if globals().get("df_cuentas_pagar") is not None:
    globals().get("df_cuentas_pagar")["FUENTE"] = globals().get("df_cuentas_pagar")["RUBRO"].astype(str).apply(extraer_fuente)
    globals().get("df_cuentas_pagar")["FUENTE"].fillna("", inplace=True)

    # Convertir todos los valores de 'PAGO' a cadenas
    globals().get("df_cuentas_pagar")["PAGO"] = globals().get("df_cuentas_pagar")["PAGO"].astype(str)

    # Eliminar símbolos y convertir 'PAGO' a numérico
    globals().get("df_cuentas_pagar")["PAGO"] = globals().get("df_cuentas_pagar")["PAGO"].str.replace("[^\d,.-]", "", regex=True)
    globals().get("df_cuentas_pagar")["PAGO"] = globals().get("df_cuentas_pagar")["PAGO"].str.replace(r"\.(?=\d{3})", "", regex=True).str.replace(",", ".").astype(float)
    df_cuentas_pagar_agrupado = globals().get("df_cuentas_pagar").groupby("FUENTE")["PAGO"].sum().reset_index(name="Total Pagos")
    df_cuentas_pagar_agrupado["Total Pagos"] = df_cuentas_pagar_agrupado["Total Pagos"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ","))

if globals().get("df_egreso_rubro") is not None:
    globals().get("df_egreso_rubro")["FUENTE"] = globals().get("df_egreso_rubro")["RUBRO"].astype(str).apply(extraer_fuente)
    globals().get("df_egreso_rubro")["FUENTE"].fillna("", inplace=True)
    df_egreso_agrupado2 = globals().get("df_egreso_rubro").groupby("FUENTE")["VALOR"].sum().reset_index(name="Total Egresos")
    df_egreso_agrupado2["Total Egresos"] = df_egreso_agrupado2["Total Egresos"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ","))

# Cruzar los DataFrames
if globals().get("df_comparado_recaudo_pagos") is not None:
    df_comparado_recaudo_pagos = globals().get("df_comparado_recaudo_pagos")
    df_comparado_recaudo_pagos = df_comparado_recaudo_pagos.merge(df_cuentas_pagar_agrupado, left_on="Parte_1", right_on="FUENTE", how="left")
    df_comparado_recaudo_pagos = df_comparado_recaudo_pagos.merge(df_egreso_agrupado2, left_on="Parte_1", right_on="FUENTE", how="left")

    # Renombrar columnas
    df_comparado_recaudo_pagos.rename(columns={
        "Parte_1": "FUENTE",
        "Parte_2": "NOMBRE DE LA FUENTE",
        "Total Pagos": "TOTAL PAGOS EN CXP"
    }, inplace=True)

    # Seleccionar solo las columnas necesarias
    columnas_seleccionadas = ["FUENTE", "NOMBRE DE LA FUENTE", "Total Recaudo Agrupado", "PAGOS", "Recaudo - Pagos (ECB)", "TOTAL PAGOS EN CXP", "Total Egresos"]
    df_comparado_recaudo_pagos = df_comparado_recaudo_pagos[columnas_seleccionadas]

    #st.header("MATRIZ POR FUENTE DE FINANCIACION:", divider="green")
    st.dataframe(df_comparado_recaudo_pagos)
    
    
    # Aseguramos que los valores de 'RUBRO' sean cadenas y aplicamos la función
if globals().get("df_egreso_rubro") is not None:
    df_egreso_rubro = globals().get("df_egreso_rubro")
    df_egreso_rubro[["FUENTE", "CLASIFICACION DEL GASTO"]] = df_egreso_rubro["RUBRO"].astype(str).apply(lambda x: pd.Series(extraer_fuente_y_clasificacion(x)))

    # Reemplazamos los valores 'None' con un valor vacío o por defecto si es necesario
    df_egreso_rubro["FUENTE"].fillna("", inplace=True)
    df_egreso_rubro["CLASIFICACION DEL GASTO"].fillna("", inplace=True)

    # Agrupar por 'FUENTE' y 'CLASIFICACION DEL GASTO' y sumar los valores de 'VALOR'
    df_egreso_agrupado = df_egreso_rubro.groupby(["FUENTE", "CLASIFICACION DEL GASTO"])["VALOR"].sum().reset_index()
    df_egreso_agrupado.rename(columns={"VALOR": "Total Egresos"}, inplace=True)

    # Convertir a formato de pesos colombianos
    df_egreso_agrupado["Total Egresos"] = df_egreso_agrupado["Total Egresos"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.header("TOTAL DE EGRESOS POR FUENTE Y CLASIFICACION DEL GASTO EN COMPROBANTE DE EGRESOS:", divider="green")
    st.dataframe(df_egreso_agrupado)
    
    st.header("EJECUCION DE EGRESOS POR CLASIFICADOR DEL GASTO", divider="red")
    st.dataframe(df2_agrupado_CLASI)
    
    # Realizar el merge
    df_cruzado = df_egreso_agrupado.merge(df2_agrupado_CLASI, left_on="FUENTE", right_on="FUEN FINA.", how="inner")

# Mostrar el DataFrame cruzado
#st.header("Tabla cruzada de egresos y pagos por fuente:", divider="blue")
#st.dataframe(df_cruzado)

    # Función para convertir los valores de 'PAGOS' a formato numérico correcto
    def convertir_pagos(valor):
        partes = valor.split('.')
        if len(partes) > 2:
            # Combina todas las partes excepto la última como parte entera
            parte_entera = ''.join(partes[:-1])
            # La última parte es la parte decimal
            parte_decimal = partes[-1]
            return float(parte_entera + '.' + parte_decimal)
        return float(valor)

    # Función para convertir los valores de 'Total Egresos' a formato numérico correcto
    def convertir_total_egresos(valor):
        valor = valor.replace("$", "").replace(".", "").replace(",", ".")
        return float(valor)

    # Realizar el merge
    df_cruzado = df_egreso_agrupado.merge(df2_agrupado_CLASI, left_on=["FUENTE", "CLASIFICACION DEL GASTO"], right_on=["FUEN FINA.", "CLASIFICACION GASTO"], how="inner")

    # Seleccionar solo las columnas necesarias
    df_cruzado = df_cruzado[["FUENTE", "CLASIFICACION DEL GASTO", "Total Egresos", "PAGOS"]]

    # Convertir todos los valores de 'Total Egresos' a formato numérico correcto
    df_cruzado["Total Egresos"] = df_cruzado["Total Egresos"].apply(convertir_total_egresos)

    # Convertir todos los valores de 'PAGOS' a formato numérico correcto
    df_cruzado["PAGOS"] = df_cruzado["PAGOS"].astype(str).apply(convertir_pagos)

    # Calcular la diferencia entre 'Total Egresos' y 'PAGOS'
    df_cruzado["Total EGRESOS-PAGOS"] = df_cruzado["Total Egresos"] - df_cruzado["PAGOS"]

    # Convertir 'Total Egresos', 'PAGOS' y 'Total EGRESOS-PAGOS' a formato de pesos colombianos
    df_cruzado["Total Egresos"] = df_cruzado["Total Egresos"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_cruzado["PAGOS"] = df_cruzado["PAGOS"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_cruzado["Total EGRESOS-PAGOS"] = df_cruzado["Total EGRESOS-PAGOS"].apply(lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Mostrar el DataFrame cruzado
    st.header("EJECUCION POR TIPO DE GASTO:", divider="blue")
    st.dataframe(df_cruzado)

        # Hacer una copia del DataFrame
    df_comparado_recaudo_pagos_copia = df_comparado_recaudo_pagos.copy()

# Función para convertir los valores a formato numérico correcto
def convertir_a_numero(valor):
    if isinstance(valor, str):
        valor = valor.replace("$", "").replace(".", "").replace(",", "")
        valor = valor[:-2] + "." + valor[-2:]
    return float(valor)

def procesar_dataframe(df):
    # Convertir las columnas 'TOTAL PAGOS EN CXP', 'Total Egresos', 'PAGOS' y 'Recaudo - Pagos (ECB)' a formato numérico
    df["TOTAL PAGOS EN CXP"] = df["TOTAL PAGOS EN CXP"].apply(convertir_a_numero)
    df["Total Egresos"] = df["Total Egresos"].apply(convertir_a_numero)
    df["PAGOS"] = df["PAGOS"].apply(convertir_a_numero)
    df["Recaudo - Pagos (ECB)"] = df["Recaudo - Pagos (ECB)"].apply(convertir_a_numero)

    # Calcular 'SALDO CXP'
    df["SALDO CXP"] = df["TOTAL PAGOS EN CXP"] - df["PAGOS"]

    # Calcular 'Recaudo - Pagos - SALDO CXP (ECB)'
    df["Recaudo - Pagos - SALDO CXP (ECB)"] = df["Recaudo - Pagos (ECB)"] - df["SALDO CXP"]

    # Mostrar el DataFrame copiado con el nuevo cálculo
    st.header("MATRIZ POR FUENTE DE FINANCIACION CON SALDO CXP:", divider="green")
    st.dataframe(df)

    return df

# Uso de la función
df_comparado_recaudo_pagos_copia = procesar_dataframe(df_comparado_recaudo_pagos_copia)
    # Mostrar el DataFrame copiado con el nuevo cálculo
#st.header("MATRIZ POR FUENTE DE FINANCIACION CON SALDO CXP:", divider="green")
#st.dataframe(df_comparado_recaudo_pagos_copia)

def procesar_excel():
    # Obtener el DataFrame cargado
    df_boletin_caja = globals().get("df_boletin_caja")
    
    if df_boletin_caja is None:
        st.error("El archivo de Boletin de caja no se ha cargado correctamente.")
        return None
    
    
    # Eliminar espacios en blanco de los nombres de las columnas
    df_boletin_caja.columns = df_boletin_caja.columns.str.replace(' ', '')
    
    # Crear la columna 'fuente' y 'categoria'
    df_boletin_caja['fuente'] = None
    df_boletin_caja['categoria'] = None
    
    # Variables para almacenar los valores actuales de 'fuente' y 'categoria'
    fuente_actual = None
    categoria_actual = None
    
    indices_a_eliminar = []

    for index, row in df_boletin_caja.iterrows():
        # Asignar el valor de 'fuente' cuando se encuentra 'FUENTE:'
        if 'FUENTE:' in str(row['CODIGO']):
            fuente_actual = row['DESCRIPCION']
            indices_a_eliminar.append(index)
        
        # Asignar el valor de 'categoria' cuando se encuentra 'BANCOS' o 'CAJAS'
        if row['CODIGO'] == 'BANCOS':
            categoria_actual = 'BANCOS'
        elif row['CODIGO'] == 'CAJAS':
            categoria_actual = 'CAJAS'
        
        # Asignar los valores actuales de 'fuente' y 'categoria' a las filas correspondientes
        df_boletin_caja.at[index, 'fuente'] = fuente_actual
        df_boletin_caja.at[index, 'categoria'] = categoria_actual
    
        # Eliminar las filas que contienen 'FUENTE:'
        df_boletin_caja = df_boletin_caja.drop(indices_a_eliminar)
    
        # Eliminar filas que contienen 'SUBTOTAL', 'TOTAL' o 'Modulo de Tesoreria v6'
        df_boletin_caja = df_boletin_caja[~df_boletin_caja['CODIGO'].str.contains('SUBTOTAL|TOTAL|Modulo de Tesoreria v6', na=False)]
        
        # Eliminar filas vacías
        df_boletin_caja = df_boletin_caja.dropna(how='all')
        
        # Eliminar filas donde 'CODIGO' esté vacío o contenga 'CODIGO'
        df_boletin_caja = df_boletin_caja[~df_boletin_caja['CODIGO'].isnull() & (df_boletin_caja['CODIGO'] != 'CODIGO')]

        # Reorganizar las columnas
        columnas_ordenadas = ['CODIGO','fuente', 'BANCOS', 'DESCRIPCION', 'V.ANTERIOR', 'V.DEBITO', 'V.CREDITO', 'V.SIGUIENTE']
        df_boletin_caja = df_boletin_caja[columnas_ordenadas]
        
        # Renombrar el DataFrame combinado
        df_combinado_bancos = df_boletin_caja

    
    return df_combinado_bancos

# Procesar el archivo Excel de Boletin de caja
#df_combinado_bancos = procesar_excel()

#if df_combinado_bancos is not None:
            #st.write("Vista previa de df_combinado_bancos:")
            #st.dataframe(df_combinado_bancos)

def cruzar_conciliaciones():
    # Obtener los DataFrames cargados
    df_conciliaciones = globals().get("df_conciliaciones")
    df_combinado_bancos = globals().get("df_combinado_bancos")
    
    if df_conciliaciones is None:
        st.error("El archivo de Conciliaciones no se ha cargado correctamente.")
        return None
    
    if df_combinado_bancos is None:
        st.error("El archivo combinado de bancos no se ha procesado correctamente.")
        return None
    
    # Eliminar espacios en blanco de los nombres de las columnas
    df_conciliaciones.columns = df_conciliaciones.columns.str.replace(' ', '')
    df_combinado_bancos.columns = df_combinado_bancos.columns.str.replace(' ', '')
    
    # Convertir las columnas a tipo string para realizar el merge
    df_conciliaciones['CUENTASINAP'] = df_conciliaciones['CUENTASINAP'].astype(str)
    df_combinado_bancos['CODIGO'] = df_combinado_bancos['CODIGO'].astype(str)
    
    # Realizar el cruce de datos
    df_conciliaciones = df_conciliaciones.merge(df_combinado_bancos[['CODIGO', 'fuente']], left_on='CUENTASINAP', right_on='CODIGO', how='left')
    
    # Eliminar la columna 'CODIGO' duplicada después del merge
    df_conciliaciones = df_conciliaciones.drop(columns=['CODIGO'])

    # Reorganizar las columnas para que 'fuente' quede al principio
    columnas = ['fuente'] + [col for col in df_conciliaciones.columns if col != 'fuente']
    df_conciliaciones = df_conciliaciones[columnas]
    
    return df_conciliaciones

# Procesar el cruce de conciliaciones
df_conciliaciones_cruzado = cruzar_conciliaciones()
#if df_conciliaciones_cruzado is not None:
    #st.write("Vista previa de df_conciliaciones_cruzado:")
    #st.dataframe(df_conciliaciones_cruzado)

def sumar_saldo_por_fuente():
    # Obtener el DataFrame cruzado
    df_conciliaciones_cruzado = globals().get("df_conciliaciones_cruzado")
    
    if df_conciliaciones_cruzado is None:
        st.error("El DataFrame de conciliaciones cruzado no se ha generado correctamente.")
        return None
    
    # Asegurarse de que la columna 'SALDOEXTRACTOBANCARIO' sea numérica
    df_conciliaciones_cruzado['SALDOEXTRACTOBANCARIO'] = pd.to_numeric(df_conciliaciones_cruzado['SALDOEXTRACTOBANCARIO'], errors='coerce')
    
    # Sumar 'SALDOEXTRACTOBANCARIO' acumulado por la columna 'fuente'
    df_suma_saldo = df_conciliaciones_cruzado.groupby('fuente')['SALDOEXTRACTOBANCARIO'].sum().reset_index()
    
    # Convertir los valores sumados a formato de pesos
    df_suma_saldo['SALDOEXTRACTOBANCARIO'] = df_suma_saldo['SALDOEXTRACTOBANCARIO'].apply(lambda x: f"${x:,.2f}")
    
    return df_suma_saldo

# Procesar la suma de saldos por fuente
df_suma_saldo = sumar_saldo_por_fuente()
#if df_suma_saldo is not None:
    #st.write("Suma de SALDOEXTRACTOBANCARIO por fuente:")
    #st.dataframe(df_suma_saldo)

def cruzar_saldo_con_recaudo():
    # Obtener los DataFrames cargados
    df_comparado_recaudo_pagos_copia = globals().get("df_comparado_recaudo_pagos_copia")
    df_suma_saldo = globals().get("df_suma_saldo")
    
    if df_comparado_recaudo_pagos_copia is None:
        st.error("El DataFrame de comparado recaudo pagos copia no se ha generado correctamente.")
        return None
    
    if df_suma_saldo is None:
        st.error("El DataFrame de suma de saldo no se ha generado correctamente.")
        return None
    
    # Convertir las columnas a tipo string para realizar el merge
    df_comparado_recaudo_pagos_copia['FUENTE'] = df_comparado_recaudo_pagos_copia['FUENTE'].astype(str)
    df_suma_saldo['fuente'] = df_suma_saldo['fuente'].astype(str)
    
    # Realizar el cruce de datos
    df_resultado = df_comparado_recaudo_pagos_copia.merge(df_suma_saldo[['fuente', 'SALDOEXTRACTOBANCARIO']], left_on='FUENTE', right_on='fuente', how='left')
    
    # Eliminar la columna 'fuente' duplicada después del merge
    df_resultado = df_resultado.drop(columns=['fuente'])
    
    return df_resultado

# Procesar el cruce de saldo con recaudo
df_resultado = cruzar_saldo_con_recaudo()
if df_resultado is not None:
    st.header("MATRIZ POR FUENTE DE FINANCIACION:", divider="green")
    st.dataframe(df_resultado)
