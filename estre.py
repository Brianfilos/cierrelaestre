import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CIERRE PRESUPUESTAL ESTRELLA", layout="wide")

st.title("Cargue Archivos para Cruce")

# Función para cargar y limpiar un archivo CSV
def cargar_csv(label, sep_char=",", skip_rows=5):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file is not None:
        try:
            df = pd.read_csv(file, encoding="latin1", sep=sep_char, skiprows=skip_rows)
            df.columns = df.columns.str.strip()  # Elimina espacios en los nombres de las columnas
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None

# Función para cargar archivos Excel
def cargar_excel(label):
    file = st.file_uploader(label, type=["xlsx"], key=label)
    if file is not None:
        try:
            df = pd.read_excel(file, engine="openpyxl")
            df.columns = df.columns.str.strip()  # Elimina espacios en los nombres de las columnas
            return df
        except Exception as e:
            st.error(f"No se pudo leer el archivo {label}: {e}")
    return None

# Diccionario para almacenar los DataFrames
dataframes = {}

# Lista de configuraciones de archivos
archivos = [
    {"titulo": "Ejecución Presupuestal - Egresos", "color": "green", "funcion_carga": cargar_csv, "parametro": "Cargar CSV (Egresos)", "nombre_df": "df_egresos", "sep_char": ";"},
    {"titulo": "Ejecución Presupuestal - Ingresos", "color": "red", "funcion_carga": cargar_csv, "parametro": "Cargar CSV (Ingresos)", "nombre_df": "df_ingresos", "sep_char": ";"},
    {"titulo": "Reporte De Cuentas Por Pagar", "color": "blue", "funcion_carga": cargar_csv, "parametro": "Cargar CSV (Cuentas por pagar)", "nombre_df": "df_cuentas_pagar", "sep_char": ";"},
    {"titulo": "Boletín de Caja", "color": "blue", "funcion_carga": cargar_excel, "parametro": "Cargar Excel (Boletín de Caja)", "nombre_df": "df_boletin_caja"},
    {"titulo": "Comprobante de Egreso por Rubro", "color": "violet", "funcion_carga": cargar_excel, "parametro": "Cargar Excel (Egreso por Rubro)", "nombre_df": "df_egreso_rubro"},
    {"titulo": "Conciliaciones Bancarias", "color": "gray", "funcion_carga": cargar_excel, "parametro": "Cargar Excel (Conciliaciones)", "nombre_df": "df_conciliaciones"},
    {"titulo": "Reservas La Estrella", "color": "blue", "funcion_carga": cargar_excel, "parametro": "Cargar Excel (Reservas)", "nombre_df": "df_reservas"},
    {"titulo": "Boletin de Tesoreria", "color": "green", "funcion_carga": cargar_excel, "parametro": "Cargar Excel (tesoreria)", "nombre_df": "df_tesoreria"}
]

# Iterar sobre los archivos para cargarlos
for archivo in archivos:
    st.header(archivo["titulo"], divider=archivo["color"])

    if "sep_char" in archivo:
        dataframes[archivo["nombre_df"]] = archivo["funcion_carga"](archivo["parametro"], sep_char=archivo["sep_char"])
    else:
        dataframes[archivo["nombre_df"]] = archivo["funcion_carga"](archivo["parametro"])

    # Mostrar vista previa si el usuario lo solicita
    if dataframes[archivo["nombre_df"]] is not None:
        if st.checkbox(f"Mostrar vista previa de {archivo['titulo']}"):
            st.write(f"Vista previa de {archivo['nombre_df']}:")
            st.dataframe(dataframes[archivo["nombre_df"]])
    else:
        st.warning(f"No se ha cargado el archivo {archivo['titulo']}.")

# Verificación de carga de archivos
def archivos_cargados():
    return all(df is not None and not df.empty for df in dataframes.values())


# MATRIZ GENERAL

# Definir las columnas
columnas = ['FUENTE','CONCEPTO', 'NOMBRE']

# Definir las filas (puedes personalizarlas según lo necesites)
filas = [
    ['0-101','LIBRE DESTINACIÓN','INGRESOS CORRIENTES DE LIBRE DESTINACION'],
    ['0-103','PRIMERA INFANCIA','SGP PRIMERA INFANCIA'],
    ['0-104','FONDO EMPLEADOS','RECUPERACION DE CARTERA - PRESTAMOS'],
    ['0-105','SOBRETASA AMBIENTAL (DEPOSITOS PROVISIONALES)','DEPOSITOS PROVISIONALES'],
    ['0-108','FONDO OBREROS','RECUPERACION DE CARTERA - PRESTAMOS'],
    ['0-111','EDUCACION MATRICULA OFICIAL','SGP-EDUCACION-CALIDAD  POR GRATUIDAD'],
    ['0-114','PRO CULTURA','ESTAMPILLAS'],
    ['0-115','SGP - LIBRE INVERSION','SGP-PROPOSITO GENERAL-PROPOSITO GENERAL LIBRE INVERSION'],
    ['0-116','SGP DEPORTE','SGP-PROPOSITO GENERAL-DEPORTE Y RECREACION'],
    ['0-117','SGP CULTURA','SGP-PROPOSITO GENERAL-CULTURA'],
    ['0-118','APSB','SGP-AGUA POTABLE Y SANEAMIENTO BASICO'],
    ['0-119','PAE','SGP-ASIGNACION ESPECIAL-PROGRAMAS DE ALIMENTACION ESCOLAR'],
    ['0-120','COLJUEGOS','DERECHOS POR LA EXPLOTACION JUEGOS DE SUERTE Y AZAR'],
    ['0-124','CONTRIBUCION OBRAS PUBLICAS','CONTRIBUCION SOBRE CONTRATOS DE OBRA PUBLICA'],
    ['0-126','SECTOR ELECTRICO','CONTRIBUCION DEL SECTOR ELECTRICO'],
    ['0-129','SGP SUBSIDIO A LA OFERTA','SGP-SALUD-SUBSIDIO A LA OFERTA'],
    ['0-131','SALUD PUBLICA','SGP-SALUD-SALUD PUBLICA'],
    ['0-136','ACUEDUCTO','PARTICIPACIÓN SUPERÁVIT DE LAS CONTRIBUCIONES DE SOLIDARIDAD DE SERVICIOS PÚBLICOS (ASEO)'],
    ['0-137','MULTAS','OTRAS MULTAS, SANCIONES E INTERESES DE MORA CON DESTINACION ESPECIFICA LEGAL'],
    ['0-159','OTROS BANCOS','CONVENIOS'],
    ['0-163','RESIDUOS SOLIDOS','OTRAS TASAS Y DERECHOS ADMINISTRATIVOS CON DESTINACION ESPECIFICA LEGAL'],
    ['0-168','OTROS BANCOS','CONVENIOS'],
    ['0-216','OTROS BANCOS','CONVENIOS'],
    ['0-219','SOBRETASA BOMBERIL','SOBRETASA BOMBERIL'],
    ['0-251','ADULTO MAYOR','ESTAMPILLAS'],
    ['0-273','OTROS BANCOS','CONVENIOS'],
    ['0-283','OTROS BANCOS','REGALIAS'],
    ['0-302','OTROS BANCOS','CONVENIOS'],
    ['0-315','ALUMBRADO PUBLICO','IMPUESTO - SOBRETASA POR EL ALUMBRADO PUBLICO'],
    ['0-327','FONDO CONCEJO','RECUPERACION DE CARTERA - PRESTAMOS'],
    ['0-337','CUOTAS PARTES PENSIONALES','SISTEMA GENERAL DE PENSIONES - CUOTAS PARTES PENSIONALES'],
    ['0-338','RECURSOS DEL CREDITO','RECURSOS DE CREDITO INTERNO'],
    ['0-356','MULTAS POLICIA','MULTAS CODIGO NACIONAL DE POLICIA Y CONVIVENCIA'],
    ['0-365','FONPET','RETIROS FONPET'],
    ['0-404','CONVENIOS','CONVENIOS'],
    ['0-429','RESIDUOS SOLIDOS','OTRAS TASAS Y DERECHOS ADMINISTRATIVOS CON DESTINACION ESPECIFICA LEGAL'],
    ['0-431','OTRAS FUENTES','RETIROS FONPET'],
    ['0-501','SOBRETASA AMBIENTAL CCAA','SOBRETASA - PARTICIPACION AMBIENTAL - CORPORACIONES AUTONOMAS REGIONALES'],
    ['0-502','SOBRETASA AMBIENTAL AAMM','SOBRETASA AMBIENTAL AREAS METROPOLITANAS'],
    ['0-504','JUSTICIA FAMILIAR','ESTAMPILLAS'],
    ['0-505','ALCANTARILLADO','PARTICIPACIÓN SUPERÁVIT DE LAS CONTRIBUCIONES DE SOLIDARIDAD DE SERVICIOS PÚBLICOS (ASEO)'],
    ['0-506','ASEO','PARTICIPACIÓN SUPERÁVIT DE LAS CONTRIBUCIONES DE SOLIDARIDAD DE SERVICIOS PÚBLICOS (ASEO)'],
    ['0-507','COLJUEGOS','DERECHOS POR LA EXPLOTACION JUEGOS DE SUERTE Y AZAR'],
    ['0-509','LEY 99','ICLD LEY 99 - DESTINO AMBIENTAL'],
    ['0-510','GESTIÓN DEL RIESGO','INGRESOS CORRIENTES DE DESTINACION ESPECIFICA POR ACTO ADMINISTRATIVO'],
    ['0-511','PAE','PARTICIPACIONES DISTINTAS DEL SGP CON DESTINACION ESPECIFICA LEGAL'],
    ['0-512','OBLIGACIONES URBANISTICAS','OTRAS CONTRIBUCIONES CON DESTINACION ESPECIFICA LEGAL'],
    ['0-601','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-602','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-603','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-604','OTROS BANCOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-605','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-606','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-607','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-608','CONVENIOS','COFINANCIACION-AMVA PAR VIAL'],
    ['0-609','EDUCACION PRESTACION DE SERVICIOS','SGP-EDUCACION-PRESTACION DE SERVICIOS'],
    ['0-610','CONVENIOS','CONVENIOS'],
    ['0-611','CONVENIOS','CONVENIOS'],
    ['0-612','CONVENIOS','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-613','CONVENIOS','CONVENIOS'],
    ['0-615','RESIDUOS SOLIDOS','OTRAS TASAS Y DERECHOS ADMINISTRATIVOS CON DESTINACION ESPECIFICA LEGAL'],
    ['0-616','LEY 1493 ESPECTACULOS PP','PARTICIPACIONES DISTINTAS DEL SGP CON DESTINACION ESPECIFICA LEGAL'],
    ['0-618','CONVENIOS','CONVENIOS'],
    ['0-619','CONVENIOS','CONVENIOS'],
    ['0-623','ALUMBRADO PUBLICO','CONVENIOS'],
    ['0-625','CONVENIOS','CONVENIOS'],
    ['0-626','SALUD PUBLICA','TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['0-627','SALUD PUBLICA','VIGILANCIA EN SALUD-CONCURRENCIA'],
    ['0-628','CONVENIOS','PLAN BÁSICO DEL ORDAMIENTO TERRITORIAL'],
    ['0-630','CONVENIOS','COFINANCIACION CORANTIOQUIA 040-COV2409-43'],
    ['1-110','ADRES','SISTEMA GENERAL DE SEGURIDAD SOCIAL EN SALUD - OTROS RECURSOS ADMINISTRADOS POR ADRES'],
    ['1-112','SGP EDUCACIÓN GRATUIDAD','IMPLEMENTACIÓN DE ESTRATEGIAS DE COBERTURA PERMANENCIA Y APRENDIZAJE PARA LOS ESTUDIANTES DE LAS DIFERENTES INSTITUCIONES EDUCATIVAS OFICIALES'],
    ['1-120','COJUEGOS','COLJUEGOS 75% SSF'],
    ['1-130','SALUD REGIMEN SUBSIDIADO','SGP-SALUD-REGIMEN SUBSIDIADO'],
    ['1-143','IMPUESTO AL TELÉFONO','DESARROLLO DE ENCUENTROS DEPORTIVOS Y RECREATIVOS PARA LOS HABITANTES'],
    ['1-212','ADRES','RECURSOS DE INSPECCIÓN, VIGILANCIA Y CONTROL'],
    ['1-379','ADRES','RECURSOS DE INSPECCIÓN, VIGILANCIA Y CONTROL'],
    ['1-503','SF-SOBRETASA A LA GASOLINA ','FORTALECIMIENTO LA CAPACIDAD FINANCIERA EN LA OPERACIÓN DEL METRO DE MEDELLÍN POR PARTE DEL MUNICIPIO DE LA ESTRELLA'],
    ['1-609','EDUCACION PRESTACION DE SERVICIOS','SGP-EDUCACION-PRESTACION DE SERVICIOS'],
    ['2-101','LIBRE DESTINACIÓN','RECURSOS DEL BALANCE DE LIBRE DESTINACION'],
    ['2-103','PRIMERA INFANCIA','RB SGP PRIMERA INFANCIA'],
    ['2-104','FONDO EMPLEADOS','RB FONDO VIVIENDA EMPLEADOS'],
    ['2-108','FONDO OBREROS','R.B. RECUPERACION DE CARTERA - PRESTAMOS'],
    ['2-109','FOVIS','RB FOVIS'],
    ['2-111','EDUCACION MATRICULA OFICIAL','R.B. SGP-EDUCACION-CALIDAD  POR MATRICULA OFICIAL'],
    ['2-114','PRO CULTURA','R.B. ESTAMPILLAS'],
    ['2-115','SGP - LIBRE INVERSION','RB SGP PROPOSITOS GENERAL LIBRE INVERSION'],
    ['2-116','SGP DEPORTE','RB SGP OTROS SECTORES DEPORTE'],
    ['2-117','SGP CULTURA','R.B. SGP-PROPOSITO GENERAL-CULTURA'],
    ['2-118','APSB','R.B. SGP-AGUA POTABLE Y SANEAMIENTO BASICO'],
    ['2-119','PAE','R.B. SGP-ASIGNACION ESPECIAL-PROGRAMAS DE ALIMENTACION ESCOLAR'],
    ['2-120','COLJUEGOS','R.B. DERECHOS POR LA EXPLOTACION JUEGOS DE SUERTE Y AZAR'],
    ['2-124','CONTRIBUCION OBRAS PUBLICAS','R.B. CONTRIBUCION SOBRE CONTRATOS DE OBRA PUBLICA'],
    ['2-126','SECTOR ELECTRICO','R.B.CONTRIBUCION DEL SECTOR ELECTRICO'],
    ['2-129','SGP SUBSIDIO A LA OFERTA','R.B. SGP-SALUD-PRESTACION DEL SERVICIO DE SALUD'],
    ['2-130','SALUD REGIMEN SUBSIDIADO','R.B. SGP-SALUD-REGIMEN SUBSIDIADO'],
    ['2-131','SALUD PUBLICA','R.B. SGP-SALUD-SALUD PUBLICA'],
    ['2-136','ACUEDUCTO','RB FONDO DE SOLIDARIDAD Y REDISTRIBUCION DEL INGRESO -ACUEDUCTO'],
    ['2-137','MULTAS','RB TRANSITO Y TRANSPORTE'],
    ['2-138','DONACIONES','R.B. DONACIONES'],
    ['2-163','RESIDUOS SOLIDOS','R.B APROVECHAMIENTO Y TRATAMIENTO DE RESIDUOS SOLIDOS'],
    ['2-219','SOBRETASA BOMBERIL','R.B. SOBRETASA BOMBERIL'],
    ['2-251','ADULTO MAYOR','R.B. ESTAMPILLAS'],
    ['2-315','ALUMBRADO PUBLICO','R.B. IMPUESTO DE ALUMBRADO PUBLICO'],
    ['2-327','FONDO CONCEJO','RB FONDO VIVIENDA CONCEJO'],
    ['2-337','CUOTAS PARTES PENSIONALES','R.B. RECURSOS DEL SISTEMA DE SEGURIDAD SOCIAL INTEGRAL - PENSIONES'],
    ['2-341','ESTRATIFICACION ECONOMICA','R.B. OTRAS CONTRIBUCIONES'],
    ['2-356','MULTAS POLICIA','RB SANCIONES IMPUESTAS POR GOBIERNO, CODIGO DE POLICIA Y CONVIVENCIA'],
    ['2-365','FONPET','RB DESAHORRO FONPET'],
    ['2-431','OTRAS FUENTES','RB RETIRO FONPET'],
    ['2-501','SOBRETASA AMBIENTAL CCAA','R.B TRASLADO DE RECURSOS A LAS AUTORIDADES AMBIENTALES PARA LA PROTECCIÓN DE ECOSISTEMAS CON APORTES DEL MUNICIPIO DE LA ESTRELLA'],
    ['2-502','SOBRETASA AMBIENTAL AAMM','R.B TRASLADO DE RECURSOS A LAS AUTORIDADES AMBIENTALES PARA LA PROTECCIÓN DE ECOSISTEMAS CON APORTES DEL MUNICIPIO DE LA ESTRELLA'],
    ['2-504','JUSTICIA FAMILIAR','RB ESTAMPILLA PARA LA JUSTICIA FAMILIAR'],
    ['2-505','ALCANTARILLADO','RB FONDO DE SOLIDARIDAD Y REDISTRIBUCION DEL INGRESO-ALCANTARILLADO'],
    ['2-506','ASEO','RB FONDO DE SOLIDARIDAD Y REDISTRIBUCION DEL INGRESO-ASEO'],
    ['2-509','LEY 99','RB LEY 99/93'],
    ['2-510','GESTIÓN DEL RIESGO','RB ACUERDO 002/2014'],
    ['2-511','PAE','RB APORTES NACION ALIMENTACION ESCOLAR'],
    ['2-512','OBLIGACIONES URBANISTICAS','RB OBLIGACIONES URBANISTICAS COMPENSADAS EN DINERO'],
    ['2-601','CONVENIOS','RB COFINANCIACION CONVENIO 592 AMVA'],
    ['2-605','CONVENIOS','RB COFINANCIACION PARQUE DEL MOVIMIENTO'],
    ['2-609','EDUCACION PRESTACION DE SERVICIOS','RB SGP EDUCACION PRESTACION DE SERVICIOS'],
    ['2-610','CONVENIOS','R.B. TRANSFERENCIAS DE CAPITAL DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['2-612','CONVENIOS','RB COFINANCIACION CONVENIO 040 CONV2110-135'],
    ['2-614','TRANSFERENCIAS DE OTRAS ENTIDADES','R.B. OTRAS TRANSFERENCIAS CORRIENTES DE OTRAS ENTIDADES DEL GOBIERNO GENERAL'],
    ['2-615','RESIDUOS SOLIDOS','R.B. OTRAS CONTRIBUCIONES'],
    ['2-616','LEY 1493 ESPECTACULOS PP','RB LEY 1493 ESPECTACULOS PUBLICOS'],
    ['2-627','SALUD PUBLICA','RB RECURSOS CONCURRENCIA DEPARTAMENTO'],
    ['3-101','LIBRE DESTINACIÓN','R.F. OTROS RENDIMIENTOS FINANCIEROS'],
    ['3-103','PRIMERA INFANCIA','R.F. SGP - ASIGNACION-ATENCION INTEGRAL DE LA PRIMERA INFANCIA'],
    ['3-104','FONDO EMPLEADOS','R.F FONDO VIVIENDA EMPLEADOS'],
    ['3-108','FONDO OBREROS','R.F FONDO DE VIVIENDA OBREROS'],
    ['3-109','FOVIS','R.B FOVIS'],
    ['3-110','ADRES','R.F. DE SISTEMA GENERAL DE SEGURIDAD SOCIAL EN SALUD - OTROS RECURSOS ADMINISTRADOS POR ADRES'],
    ['3-111','EDUCACION MATRICULA OFICIAL','R.F. SGP - EDUCACION-CALIDAD  POR MATRICULA OFICIAL'],
    ['3-115','SGP - LIBRE INVERSION','R.F. SGP - PROPOSITO GENERAL -LIBRE INVERSION'],
    ['3-116','SGP DEPORTE','R.F - PROPOSITO GENERAL  DEPORTES'],
    ['3-117','SGP CULTURA','R.F - PROPOSITO GENERAL CULTURA'],
    ['3-118','APSB','R.F. SGP - AGUA POTABLE Y SANEAMIENTO BASICO'],
    ['3-119','PAE','R.F. SGP - ASIGNACION ESPECIAL-PROGRAMAS DE ALIMENTACION ESCOLAR'],
    ['3-120','COLJUEGOS','R.F COLJUEGOS-ETESA-LOCALIZADOS'],
    ['3-124','CONTRIBUCION OBRAS PUBLICAS','R.F FONDO DE SEGURIDAD 5% CONTRATOS'],
    ['3-126','SECTOR ELECTRICO','R.F. CONTRIBUCION DEL SECTOR ELECTRICO'],
    ['3-129','SGP SUBSIDIO A LA OFERTA','R.F. SGP - SALUD-PRESTACION DEL SERVICIO DE SALUD'],
    ['3-130','SALUD REGIMEN SUBSIDIADO','R.F. SGP - SALUD-REGIMEN SUBSIDIADO'],
    ['3-131','SALUD PUBLICA','R.F. SGP - SALUD-SALUD PUBLICA'],
    ['3-136','ACUEDUCTO','R.F. FSRI ACUEDUCTO'],
    ['3-137','MULTAS','R.F. DERECHOS DE TRANSITO'],
    ['3-219','SOBRETASA BOMBERIL','R.F SOBRETASA BOMBERIL'],
    ['3-251','ADULTO MAYOR','R.F ADULTO MAYOR'],
    ['3-283','OTROS BANCOS','R.F REGALIAS'],
    ['3-315','ALUMBRADO PUBLICO','R.F ALUMBRADO PUBLICO'],
    ['3-327','FONDO CONCEJO','R.F FONDO VIVIENDA CONCEJO'],
    ['3-337','CUOTAS PARTES PENSIONALES','R.F. DE SISTEMA GENERAL DE PENSIONES'],
    ['3-341','ESTRATIFICACION ECONOMICA','R.F ESTRATIFICACION SOCIOECONOMICA MUNICIPIO DE LA ESTRELLA'],
    ['3-352','OTROS BANCOS','R.F SUBSIDIOS COMFAMA'],
    ['3-356','MULTAS POLICIA','R.F CODIGO POLICIA'],
    ['3-365','FONPET','R.F DESAHORRO-FONPET'],
    ['3-431','OTRAS FUENTES','R.F DESAHORRO FONPET P.G OTRAS FTES'],
    ['3-504','JUSTICIA FAMILIAR','R.F ESTAMPILLA PARA LA JUSTICIA FAMILIAR'],
    ['3-505','ALCANTARILLADO','R.F. FSRI ALCANTARILLADO'],
    ['3-506','ASEO','R.F. FSRI ASEO'],
    ['3-509','LEY 99','R.F LEY 99/93'],
    ['3-510','GESTIÓN DEL RIESGO','R.F ACUERDO 002/2014'],
    ['3-511','PAE','APORTES NACIONR.F ALIMENTACION ESCOLAR'],
    ['3-512','OBLIGACIONES URBANISTICAS','R.F OBLIGACIONES URBANISTICAS COMPENSADAS EN DINERO'],
    ['3-609','EDUCACION PRESTACION DE SERVICIOS','R.F. SGP - EDUCACION-PRESTACION DE SERVICIO EDUCATIVO'],
    ['3-614','TRANSFERENCIAS DE OTRAS ENTIDADES','R.F OTROS GTOS SALUD INVERSION'],
    ['3-615','RESIDUOS SOLIDOS','R.F. OTROS RENDIMIENTOS FINANCIEROS'],
    ['3-616','LEY 1493 ESPECTACULOS PP','R.F LEY 1493 ESPECTACULOS PUBLICOS'],
    ['3-623','ALUMBRADO PUBLICO','R.F  C.I 10032022021 DE 2021 EMGEA S.A E.S.P GEN + S.A E.S.P. (ANTIOQUIA LED)'],
    ['3-628','PLAN BÁSICO DEL ORDAMIENTO TERRITORIAL','R.F PLAN BÁSICO DEL ORDAMIENTO TERRITORIAL']
]

# Crear el DataFrame con las columnas y filas definidas
df_Matriz = pd.DataFrame(filas, columns=columnas)

# Mostrar el DataFrame en Streamlit
#st.dataframe(df_Matriz)

# Procesamiento de la Ejecución Presupuestal de Ingresos
if "df_ingresos" in dataframes and dataframes["df_ingresos"] is not None:
    df_ingresos = dataframes["df_ingresos"]

    # Verificar si la columna 'FUENTE FINANCIACION' existe
    if "FUENTE FINANCIACION" in df_ingresos.columns:
        df_ingresos["FUENTE FINANCIACION"] = df_ingresos["FUENTE FINANCIACION"].astype(str)

        # Separar la columna 'FUENTE FINANCIACION'
        def split_by_first_two_hyphens(text):
            parts = text.split("-", 2)
            return (parts[0] + "-" + parts[1], parts[2]) if len(parts) > 2 else (parts[0], "")

        columnas_separadas = df_ingresos["FUENTE FINANCIACION"].apply(split_by_first_two_hyphens)
        columnas_separadas = pd.DataFrame(columnas_separadas.tolist(), columns=["Parte_1", "Parte_2"])

        df_ingresos["Parte_1"], df_ingresos["Parte_2"] = columnas_separadas["Parte_1"], columnas_separadas["Parte_2"]

        # --- 🔹 Procesar 'TOTAL RECAUDO' ---
        if "TOTAL RECAUDO" in df_ingresos.columns:
            try:
                df_ingresos["TOTAL RECAUDO"] = df_ingresos["TOTAL RECAUDO"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
                df_ingresos["TOTAL RECAUDO"] = pd.to_numeric(df_ingresos["TOTAL RECAUDO"], errors="coerce")
                df_ingresos["TOTAL RECAUDO"].fillna(0, inplace=True)

                # Agrupar y mostrar resultados
                df_agrupado_recaudo = df_ingresos.groupby(["Parte_1", "Parte_2"])["TOTAL RECAUDO"].sum().reset_index()
                df_agrupado_recaudo["Total Recaudo Agrupado"] = df_agrupado_recaudo["TOTAL RECAUDO"].apply(
                    lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
                df_agrupado_recaudo["Parte_1"].fillna(0, inplace=True)  # 🔥 Eliminar valores NaN
                #st.header("Total Recaudo por fuente de financiación en ejecución de ingresos:", divider="blue")
                #st.dataframe(df_agrupado_recaudo[["Parte_1", "Parte_2", "Total Recaudo Agrupado"]])
            except Exception as e:
                st.error(f"Error al procesar 'TOTAL RECAUDO': {e}")
        else:
            st.warning("No se ha encontrado la columna 'TOTAL RECAUDO' en el archivo cargado.")

        # --- 🔹 Procesar 'PRESUPUESTO DEFINITIVO' ---
        if "PRESUPUESTO DEFINITIVO" in df_ingresos.columns:
            try:
                df_ingresos["PRESUPUESTO DEFINITIVO"] = df_ingresos["PRESUPUESTO DEFINITIVO"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
                df_ingresos["PRESUPUESTO DEFINITIVO"] = pd.to_numeric(df_ingresos["PRESUPUESTO DEFINITIVO"], errors="coerce")
                df_ingresos["PRESUPUESTO DEFINITIVO"].fillna(0, inplace=True)

                # Agrupar y mostrar resultados
                df_agrupado_presupuesto = df_ingresos.groupby(["Parte_1", "Parte_2"])["PRESUPUESTO DEFINITIVO"].sum().reset_index()
                df_agrupado_presupuesto["PRESUPUESTO DEFINITIVO Agrupado"] = df_agrupado_presupuesto["PRESUPUESTO DEFINITIVO"].apply(
                    lambda x: f"${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
                df_agrupado_presupuesto["Parte_1"].fillna(0, inplace=True) # 🔥 Eliminar valores NaN
                #st.header("Suma de presupuesto definitivo por fuente de financiación en ejecución de ingresos:", divider="blue")
                #st.dataframe(df_agrupado_presupuesto[["Parte_1", "Parte_2", "PRESUPUESTO DEFINITIVO Agrupado"]])
            except Exception as e:
                st.error(f"Error al procesar 'PRESUPUESTO DEFINITIVO': {e}")
        else:
            st.warning("No se ha encontrado la columna 'PRESUPUESTO DEFINITIVO' en el archivo cargado.")

    else:
        st.error("La columna 'FUENTE FINANCIACION' no existe en el archivo cargado.")
else:
    st.warning("El DataFrame 'df_ingresos' no está cargado.")

#Procesamiento de la Ejecución Presupuestal de Egresos
if "df_egresos" in dataframes and dataframes["df_egresos"] is not None:
        df_egresos = dataframes["df_egresos"]
        
        # --- 🔹 Procesar 'COMPROBACION DE EJECUCION DE EGRESOS' ---
        if df_egresos is not None:  
            # Procesar los pagos
            if "FUEN FINA." in df_egresos.columns and "PAGOS" in df_egresos.columns and "COMP." in df_egresos.columns and "OBLI." in df_egresos.columns:
                try:
                    # Convertir los valores de 'PAGOS', 'COMP.', y 'OBLI.' a formato numérico (eliminando puntos y reemplazando comas por puntos)
                    
                    df_egresos[['PAGOS', 'COMP.', 'OBLI.']] = df_egresos[['PAGOS', 'COMP.', 'OBLI.']].replace({r'\.': '', r',': '.'}, regex=True).astype(float)
                    
                    # Agrupar por 'FUEN FINA.' y sumar los valores de 'PAGOS', 'COMP.', y 'OBLI.'
                    df2_agrupado = df_egresos.groupby("FUEN FINA.")[['PAGOS', 'COMP.', 'OBLI.']].sum().reset_index()
                    
                    # Crear una nueva columna 'CXP' que sea la resta de 'OBLI.' menos 'PAGOS'
                    df2_agrupado['CXP'] = df2_agrupado['OBLI.'] - df2_agrupado['PAGOS']
                    
                    #st.write("COMPROBACION DE EJECUCION DE EGRESOS (CXP (OBLIGACIONES-PAGOS)):")
                    #st.write(df2_agrupado)
                    
                except Exception as e:
                    st.error(f"Error al agrupar los datos: {e}")
            else:
                st.warning("Las columnas 'FUEN FINA.', 'PAGOS', 'COMP.' o 'OBLI.' no existen en el archivo cargado.")
            
            
            # Procesar los pagos
            if "FUEN FINA." in df_egresos.columns and "PAGOS" in df_egresos.columns and "CCPET" in df_egresos.columns:
                try:
                    # Extraer los primeros 3 dígitos de 'CCPET' y colocarlos en 'CLASIFICACION GASTO'
                    df_egresos["CLASIFICACION GASTO"] = df_egresos["CCPET"].astype(str).str[:3]

                    # Convertir los valores de 'PAGOS' a formato numérico (eliminando puntos y reemplazando comas por puntos)
                    df_egresos['PAGOS'] = df_egresos['PAGOS'].replace({r'\.': '', r',': '.'}, regex=True).astype(float)
                    
                    # Agrupar por 'FUEN FINA.' y 'CLASIFICACION GASTO' y sumar los valores de 'PAGOS'
                    df2_agrupado_CLASI = df_egresos.groupby(["FUEN FINA.", "CLASIFICACION GASTO"])["PAGOS"].sum().reset_index()

                    #st.write("COMPROBACION DE EJECUCION DE EGRESOS (PAGOS POR CLASIFICACION DE GASTO):")
                    #st.write(df2_agrupado_CLASI)
                    
                except Exception as e:
                    st.error(f"Error al agrupar los datos: {e}")
            else:
                    st.warning("Las columnas 'FUEN FINA.', 'PAGOS' o 'CCPET' no existen en el archivo cargado.")
            
            # Procesar el presupuesto definitivo
            if "FUEN FINA." in df_egresos.columns and "PTTO DEFI." in df_egresos.columns:
                try:
                    # Limpiar los valores de 'PTTO DEFI.': eliminar '$', puntos de miles y convertir comas a puntos
                    df_egresos['PTTO DEFI.'] = df_egresos['PTTO DEFI.'].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)
                    
                    # Agrupar por 'FUEN FINA.' y sumar los valores de 'PTTO DEFI.'
                    df2_agrupado2 = df_egresos.groupby("FUEN FINA.")["PTTO DEFI."].sum().reset_index()

                    # Mostrar el DataFrame agrupado
                    #st.header("Suma de presupuesto definitivo en ejecución de egresos:",divider="red")
                    #st.dataframe(df2_agrupado2)

                except Exception as e:
                    st.error(f"Error al agrupar los datos: {e}")
            else:
                st.warning("Las columnas 'FUEN FINA.' o 'PTTO DEFI.' no existen en el archivo cargado.")
            

        else:
            st.error("La columna  no existe en el archivo cargado.")
else:
    st.warning("El DataFrame 'df_' no está cargado.")

# Comparación entre recaudo y pagos
if 'df_agrupado_recaudo' in locals() and 'df2_agrupado' in locals():
        # Asegurémonos de que las columnas 'Total Recaudo Agrupado' y 'PAGOS' sean numéricas
        df_agrupado_recaudo["Total Recaudo Agrupado"] = df_agrupado_recaudo["Total Recaudo Agrupado"].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)
        df2_agrupado['PAGOS'] = df2_agrupado['PAGOS'].replace({r'\$': '', r'\.': '', r',': '.'}, regex=True).astype(float)

        # Realizamos el merge entre df_agrupado y df2_agrupado por la columna de fuente de financiación
        df_comparado_recaudo_pagos = pd.merge(df_agrupado_recaudo, df2_agrupado, left_on="Parte_1", right_on="FUEN FINA.", how="inner")

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
        #st.header("Diferencia entre Recaudo y Pagos por fuente de financiación:", divider="gray")
        #st.dataframe(df_comparado_recaudo_pagos)
else:
        st.error("Error: Los DataFrames 'df_agrupado' y 'df2_agrupado' no están creados o definidos.")

#CONVERTIR EL BOLETIN DE CAJA

# Procesar el archivo de Boletín de Caja
def procesar_boletin_caja():
    # Obtener el DataFrame cargado
    df_boletin_caja = dataframes.get("df_boletin_caja")
    
    if df_boletin_caja is None:
        st.error("El archivo de Boletín de Caja no se ha cargado correctamente.")
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
    columnas_ordenadas = ['fuente', 'CODIGO', 'DESCRIPCION']
    df_boletin_caja = df_boletin_caja[columnas_ordenadas]
    
    return df_boletin_caja

# Procesar el Boletín de Caja
df_boletin_caja_procesado = procesar_boletin_caja()

# Agregar la columna SALDO EXTRACTO del df_tesoreria
if df_boletin_caja_procesado is not None and "df_tesoreria" in dataframes:
    df_tesoreria = dataframes["df_tesoreria"]
    if df_tesoreria is not None:
        df_tesoreria.columns = df_tesoreria.columns.str.replace(' ', '')
        
        # Convertir las columnas CODIGO a tipo str
        df_boletin_caja_procesado['CODIGO'] = df_boletin_caja_procesado['CODIGO'].astype(str)
        df_tesoreria['CODIGO'] = df_tesoreria['CODIGO'].astype(str)
        
        df_boletin_caja_procesado = df_boletin_caja_procesado.merge(df_tesoreria[['CODIGO', 'SALDOEXTRACTO']], on='CODIGO', how='left')
        st.header("MATRIZ DE TESORERIA", divider="green")
        st.dataframe(df_boletin_caja_procesado)
    else:
        st.error("El archivo de Tesorería no se ha cargado correctamente.")
else:
    st.error("El archivo de Boletín de Caja no se ha cargado correctamente o el DataFrame 'df_tesoreria' no está disponible.")

# Extraer los últimos 5 caracteres de la columna 'RUBRO' en df_reservas y crear la columna 'FUENTE'
if "df_reservas" in dataframes and dataframes["df_reservas"] is not None:
    df_reservas = dataframes["df_reservas"]
    df_reservas['FUENTE'] = df_reservas['RUBRO'].astype(str).str[-5:]
        
    # Reordenar las columnas para que 'FUENTE' esté al inicio
    columnas_ordenadas = ['FUENTE'] + [col for col in df_reservas.columns if col != 'FUENTE']
    df_reservas = df_reservas[columnas_ordenadas]
    
    #st.header("Reservas con columna FUENTE extraída", divider="blue")
    #st.dataframe(df_reservas)
    
    # Seleccionar solo la columna 'SALDO' para la operación de suma
    if 'SALDO' in df_reservas.columns:
        df_reservas_acumuladas = df_reservas.groupby('FUENTE')['SALDO'].sum().reset_index()
        
        #st.header("Reservas Acumuladas por FUENTE", divider="blue")
        #st.dataframe(df_reservas_acumuladas)
    else:
        st.error("La columna 'SALDO' no existe en el DataFrame 'df_reservas'.")
else:
    st.error("El DataFrame 'df_reservas' no está cargado o no existe.")

#TRAER LA INFORMACION DE BOLETIN DE TESORERIA

# UNIR MATRIZ CON DF_COMPARADO_RECAUDO_PAGOS:
df_Matriz_1 = pd.merge(df_Matriz, df_comparado_recaudo_pagos, left_on="FUENTE", right_on="Parte_1", how="left")

# Reemplazar NaN con 0 en las columnas numéricas
df_Matriz_1.fillna(0, inplace=True)

# Definir el orden de columnas deseado
columnas_deseadas = ["FUENTE", "CONCEPTO", "NOMBRE", "Total Recaudo Agrupado", "PAGOS", "COMP.", "OBLI.", "CXP"]

# Filtrar y reordenar las columnas en df_Matriz_1
df_Matriz_1 = df_Matriz_1[columnas_deseadas]

# Cruzar también el df_reservas_acumuladas y llevar la columna SALDO a df_Matriz_1 cruzando por FUENTE
if 'df_reservas_acumuladas' in locals():
    df_Matriz_1 = pd.merge(df_Matriz_1, df_reservas_acumuladas[['FUENTE', 'SALDO']], on='FUENTE', how='left')
    df_Matriz_1['SALDO'].fillna(0, inplace=True)
    df_Matriz_1.rename(columns={'SALDO': 'RESERVAS'}, inplace=True)

st.header("MATRIZ FINAL PRESUPUESTO:", divider="green")
st.write(df_Matriz_1)
