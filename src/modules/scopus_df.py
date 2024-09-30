import pandas as pd
import bibtexparser

def bib_to_df(file_path, fields=None):
    
    try:
        with open(file_path, 'r', encoding='utf-8') as bibfile:
            bibtex_str = bibfile.read()
        
        library = bibtexparser.loads(bibtex_str)

        entries_data = []

        for entry in library.entries:
            if fields is not None:
                entry = {k: entry.get(k, '') for k in fields}
            entry_data = {}
            for i in entry:
                entry_data[i] = entry.get(i, '')
            entries_data.append(entry_data)

        return pd.DataFrame(entries_data)
    
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encuentra.")

    except Exception as e:
        print(f"Ha ocurrido el error: {e}")

    return None