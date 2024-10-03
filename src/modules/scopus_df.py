import pandas as pd
import bibtexparser
import re

"""
    Convierte un archivo BibTeX a un DataFrame de pandas.

    Esta función lee un archivo BibTeX, extrae sus entradas y las convierte
    en un DataFrame, organizando las columnas según un mapeo predefinido,
    extrae el país de afiliación de las entradas siempre que esté disponible y
    cambia el formato de los autores de "AND" a ";"

    Parámetros:
    ----------
    file_path : str
        Ruta del archivo BibTeX a leer.

    Retorna:
    -------
    pd.DataFrame
        Un DataFrame de pandas que contiene las entradas del archivo BibTeX.
        Si ocurre un error durante la lectura o el análisis, retorna None.
    
    Excepciones:
    ------------
    - FileNotFoundError: Si el archivo no se encuentra en la ruta especificada.
    - UnicodeDecodeError: Si hay un error de codificación al intentar leer el archivo.
    - bibtexparser.BibTexParserError: Si hay un error al analizar el archivo BibTeX.
    - KeyError: Si se intenta acceder a una clave no existente en un diccionario.
    - ValueError: Si se encuentra un valor no válido.
    - TypeError: Si se pasa un argumento de tipo inapropiado.
"""
def bib_to_df(file_path):
     
    column_mapping = {
        'source': 'SRC',
        'document_type': 'DT',
        'abbrev_source_title': 'ABR',
        'language': 'LA',
        'issn': 'SN',
        'correspondence_address1': 'C1',
        'references': 'CR',
        'author_keywords': 'DE',
        'abstract': 'AB',
        'affiliation': 'AFF',
        'url': 'URL',
        'note': 'NOTE',
        'doi': 'DOI',
        'pages': 'PAGES',
        'number': 'NUM',
        'volume': 'VL',
        'year': 'PR',
        'journal': 'JNL',
        'title': 'TI',
        'author': 'AU',
        'ENTRYTYPE': 'ENTRY_TYPE',
        'ID': 'USERS',
        'publisher': 'PU',
        'funding_text_1': 'FU',
        'funding_details': 'FU_DETAILS',
        'keywords': 'ID',
        'art_number': 'ART NUMBER',
        'isbn': 'BN',
        'coden': 'CODEN',
        'editor': 'PU_EDITOR',
        'pubmed_id': 'PMID',
        'sponsors': 'SP',
        'page_count': 'PG',
        'chemicals_cas': 'CHEMICAL_CAS'
    }
    
    # Solamente para poder previsualizar las columnas en un orden más específico
    column_order = [
    'AU', 'DE', 'ID', 'C1',
    'CR', 'PG', 'PAGES','AB', 'SN',
    'TI', 'ART NUMBER', 'SP', 'CODEN',
    'PU', 'FUNDING', 'DT', 'ENTRY_TYPE', 'PMID',
    'CHEMICAL_CAS', 'USERS', 'NUM', 'BN',
    'VL', 'DOI', 'LA', 'URL',
    'PR', 'JNL', 'ABR', 'AFF',
    'COUNTRY_AFILIATION', 'NOTE', 'CHEMICAL_CAS', 
    'SRC', 'F_DETAILS'
    ]


    try:
        with open(file_path, 'r', encoding='utf-8') as bibfile:
            bibtex_str = bibfile.read()
        
        library = bibtexparser.loads(bibtex_str)

        entries_data = []

        for entry in library.entries:
            entry_data = {}
            for i in entry:
                entry_data[i] = entry.get(i, '').upper()
                for i in list(entry_data):
                    # Cambiar 'AND' por ';' en la lista de autores
                    if i == 'author':
                        entry_data[i] = entry_data[i].replace(' AND ', ';')
                    # Extraer el país de afiliación
                    elif i == 'affiliation':
                        affiliation = entry_data[i]
                        match = re.search(r',\s*([A-Z ]+)$', affiliation)
                        entry_data['COUNTRY_AFILIATION'] = match.group(1) if match else ''
            entries_data.append(entry_data)


        df = pd.DataFrame(entries_data)

        df.rename(columns=column_mapping, inplace=True)
        df = df[column_order]

        return df
    
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encuentra.")
    except UnicodeDecodeError:
        print(f"Error de codificación al intentar leer el archivo {file_path}.")
    except bibtexparser.BibTexParserError as e:
        print(f"Error al analizar el archivo BibTeX: {e}")
    except KeyError as e:
        print(f"Clave no encontrada: {e}")
    except ValueError as e:
        print(f"Valor no válido: {e}")
    except TypeError as e:
        print(f"Error de tipo: {e}")

    return None