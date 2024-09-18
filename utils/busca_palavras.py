from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import unidecode
import os


class BuscaPalavras:

    @staticmethod
    def string_matching(df_texto, file_path: str):
        if not os.path.exists(file_path):
            print(f"Arquivo '{file_path}' não encontrado.")
            return pd.Series([False] * len(df_texto))

        with open(file_path, 'r', encoding='utf-8') as file:
            text_lists = [unidecode.unidecode(row.strip().lower()) for row in file.readlines()]

        # Comparar os textos do DataFrame normalizados com as palavras do arquivo
        df_text_normalizado = df_texto.apply(lambda x: unidecode.unidecode(x.lower().strip()))

        # Identificar quais palavras foram encontradas
        palavras_encontradas = df_text_normalizado.apply(
            lambda x: ', '.join(filter(lambda palavra: palavra in x, text_lists))
        )

        return palavras_encontradas

    @staticmethod
    def fuzzy_string_matching(df_texto, file_path: str, similarity_threshold: int = 85):
        texts_found = []
        if not os.path.exists(file_path):
            print(f"Arquivo '{file_path}' não encontrado.")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            text_lists = [row.strip() for row in file.readlines()]

        df_text_list = df_texto.tolist()
        for word in text_lists:
            # Realiza a busca fuzzy para encontrar palavras semelhantes no DataFrame
            results = process.extract(word, df_text_list, scorer=fuzz.ratio)
            for result, similarity in results:
                if similarity >= similarity_threshold:
                    texts_found.append((word, result, similarity))

        return texts_found
