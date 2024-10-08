import pandas as pd
import re
import pickle
import numpy as np
import os


os.chdir(os.path.dirname(__file__))  # Cambia al directorio donde está el script


def scopus_refs(dataframe):
    df = dataframe.copy()

    resultados = pd.DataFrame(columns=['SR','CR_ref', 'ID'])

    # Iterar por cada celda en la columna específica
    for idx, fila in df.iterrows():

        datos = str(fila['CR']).split(';')  # Separar los datos por punto y coma
        # Crear un DataFrame temporal con los datos separados
        temp_df = pd.DataFrame({'CR_ref': [dato.strip() for dato in datos], 'ID': idx + 1, 'SR': fila['SR']})
        # Concatenar los resultados con el DataFrame original
        resultados = pd.concat([resultados, temp_df], ignore_index=True)

    resultados['CR_ref'] = resultados['CR_ref'].replace(['', ' ', 'NaN', 'nan'], np.nan)

    # Verifica si hay valores que pandas no ha reconocido como NaN y los convierte
    resultados['CR_ref'] = resultados['CR_ref'].apply(lambda x: np.nan if pd.isnull(x) or str(x).strip() == '' else x)

    # Eliminar filas con NaN en la columna 'CR_ref'
    resultados = resultados.dropna()


    df = resultados.copy()
    df.dropna()

    # Función para identificar el tipo de referencia y extraer los datos correspondientes
    def extraer_datos(referencia):
        if pd.isna(referencia):  # Verifica si la celda está vacía
            return pd.Series([None, None, None, None, None, None, None])  # Retorna valores nulos si está vacía

        # SR (Referencia completa)
        cr_ref = referencia

        # Detectar el tipo de referencia
        tipo = "Unknown"
        autores, year, titulo, journal = None, None, None, None

        # Verificar si es Tipo 2 (Año justo después de los autores)
        if re.search(r'^(?!.*doi\.org).*https:\/\/.*$', referencia, re.IGNORECASE):
              tipo = 5
        elif re.search(r",\s*\(\d{4}\)", referencia):
            if re.search(r'proceedings of.*conference|international conference', referencia, re.IGNORECASE):
              tipo = 4
            elif 'PP.' not in referencia:
              tipo = 2
            else:
              tipo = 3

            # AU (Autores) - Todo antes del año entre paréntesis
            autores = re.findall(r'^(.*?),\s*\(\d{4}\)', referencia)
            autores = autores[0].strip() if autores else None

            # PY (Año) - Año entre paréntesis
            year = re.findall(r"\(\d{4}\)", referencia)[0][1:-1] if re.findall(r"\(\d{4}\)", referencia) else None

            # JI (Journal) - Se extrae despué de la ultima coma
            journal = referencia.rsplit(',', 1)[-1].strip() if referencia.count(",") > 1 else None

            # TI (titulo) - Después del año
            titulo_info = referencia.split(")", 1)[1].strip() if ")" in referencia else None
            titulo = titulo_info.split(",")[0].strip() if titulo_info else None

        # Verificar si es Tipo 1 (Referencia de revista con año entre paréntesis después del título)
        else:
            tipo = 1

            # AU (Autores) - Todo antes del primer punto y coma
            autores = re.findall(r'^(.*?),', referencia)
            autores = autores[0].strip() if autores else None

            # PY (Año) - Año entre paréntesis
            year = re.findall(r"\((\d{4})\)", referencia)[0] if re.findall(r"\((\d{4})\)", referencia) else None

            # TI (Título) - Parte después del primer autor y antes del año
            titulo = re.split(r"\(\d{4}\)", referencia)[0].split(",")[-1].strip() if re.split(r"\(\d{4}\)", referencia) else None

            # JI (Journal) - Después del año
            journal_info = referencia.split(")", 1)[1].strip() if ")" in referencia else None
            journal = journal_info.split(",")[0].strip() if journal_info else None

        # SR_ref (Autor principal, PY, JI)
        autor_principal = autores.split(",")[0].strip() if autores else None  # Extraer solo el primer autor
        sr_ref = f"{autor_principal}, {year}, {journal}" if autor_principal and year and journal else None

        # Devolver los datos con el tipo de referencia incluido
        return pd.Series([sr_ref, titulo, autores, journal, year, cr_ref, tipo])
        
    # Aplicar la función a la columna relevante del DataFrame
    df_nuevo = df['CR_ref'].apply(extraer_datos)

    # Asignar nombres a las columnas extraídas
    df_nuevo.columns = ['SR_ref', 'TI', 'AU', 'JI', 'PY', 'CR_ref', 'ref_type']

    df_nuevo.insert(0, 'SR', df['SR'])
    # Guardar el resultado en un nuevo archivo si es necesario
    df_nuevo.to_excel('datos_extraidos_con_tipos.xlsx', index=False)
    return df_nuevo


# Cargar el archivo Excel
file_path = 'dataframe\\all_data_EM_bibx.xlsx'

sheet_name = 'scopus'

# Cargar solo la hoja especificada
df = pd.read_excel(file_path, sheet_name=sheet_name)

df_ref = scopus_refs(df)
print(df_ref)