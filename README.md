# Preprocessing Package

Este paquete contiene funciones para procesar datos bibliográficos desde diferentes fuentes.

## Funciones

-   **`wos_df()`**: Transforma archivos .txt de Web of Science a DataFrames de pandas.
-   **`scopus_df()`**: Convierte archivos .bib de Scopus a DataFrames de pandas.
-   **`doi_crossref()`**: Realiza una consulta a la API de Crossref y extrae información de un DOI.
-   **`scopus_ref()`**: Gestiona referencias de artículos, encontrando conexiones entre ellas.

## Instalación

Usa el siguiente comando para instalar las dependencias necesarias:

```
$ pip install -r requirements.txt
```

## Uso

Ejemplo de cómo usar el paquete:

```python
from preprocessing import wos_df, scopus_df

df_wos = wos_df()
df_scopus = scopus_df()
```
