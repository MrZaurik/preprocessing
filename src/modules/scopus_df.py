import pandas as pd
import bibtexparser
import re

def bib_to_df(file_path):
    column_mapping = {
        'source': 'SRC',
        'document_type': 'DT',
        'abbrev_source_title': 'ABR_SRC_TITLE',
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
        'pages': 'PG',
        'number': 'NUM',
        'volume': 'VL',
        'year': 'PR',
        'journal': 'JNL',
        'title': 'TI',
        'author': 'AU',
        'ENTRYTYPE': 'ENTRY_TYPE',
        'ID': 'USERS',
        'publisher': 'PU',
        'funding_text_1': 'FUNDING',
        'funding_details': 'F_DETAILS',
        'keywords': 'ID',
        'art_number': 'ART NUMBER',
        'isbn': 'BN',
        'coden': 'CODEN',
        'editor': 'PU',
        'pubmed_id': 'PMID',
        'sponsors': 'SP',
        'page_count': 'PG',
        'chemicals_cas': 'CHEMICAL_CAS'
        }
    
    column_order = [
    'AU', 'DE', 'ID', 'C1',
    'CR', 'PG', 'AB', 'SN',
    'TI', 'ART NUMBER', 'SP', 'CODEN',
    'PU', 'FUNDING', 'ENTRY_TYPE', 'PMID',
    'CHEMICAL_CAS', 'USERS', 'JNL', 'BN',
    'VL', 'DOI', 'LA', 'URL',
    'PR', 'NUM', 'ABR_SRC_TITLE', 'AFF',
    'COUNTRY_AFILIATION',
    'NOTE', 'CHEMICAL_CAS', 'SRC',	
    'F_DETAILS'
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
                    if i == 'author':
                        entry_data[i] = entry_data[i].replace(' AND ', ';')
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

    except Exception as e:
        print(f"Ha ocurrido el error: {e}")

    return None