# wos_module.py

import pandas as pd
import re

def wos_df(ruta_txt):
    """
    Lee un archivo de texto de Web of Science y devuelve un DataFrame con la información.

    :param ruta_txt: str - La ruta del archivo de texto a leer.
    :return: DataFrame - Un DataFrame que contiene los datos extraídos del archivo.
    """
    # Crear listas para almacenar los datos
    columns = ["PT", "AU", "AF", "TI", "SO", "LA", "DT", "DE", "ID", "AB", 
               "C1", "RP", "EM", "RI", "OI", "NR", "TC", "Z9", "U1", "U2", 
               "PU", "PI", "PA", "SN", "EI", "J9", "JI", "PD", "PY", "VL", 
               "IS", "SI", "BP", "EP", "DI", "PG", "WC", "WE", "SC", "GA", 
               "UT", "OA", "DA"]
    data = {col: [] for col in columns}

    # Leer el archivo de texto
    with open(ruta_txt, 'r', encoding='utf-8') as file:
        content = file.read()

    # Separar los registros por el marcador 'ER'
    records = content.split('ER\n')

    # Procesar cada registro
    for record in records:
        if record.strip():
            for col in columns:
                pattern = rf"{col}\s(.*)"
                match = re.search(pattern, record, re.MULTILINE)
                data[col].append(match.group(1) if match else "")

    # Crear y devolver un DataFrame
    df = pd.DataFrame(data)
    return df
