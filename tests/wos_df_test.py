# test_wos_df.py

from ..src.modules import wos_df

# Ruta del archivo de texto
ruta_txt = "./files/wos.txt"

# Llamar a la función y almacenar el DataFrame
df = wos_df(ruta_txt)

# Mostrar el DataFrame
print("DataFrame cargado desde el archivo de texto:")
print(df.head())  # Muestra las primeras filas del DataFrame
