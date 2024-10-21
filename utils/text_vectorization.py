import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import matplotlib.pyplot as plt


class TextVectorization:
    def __init__(self, df, stop_words):
        """
        Inicializa a classe TextVectorization.

        Args:
            df (pd.DataFrame): DataFrame contendo as mensagens e os usuários.
            stop_words (list): Lista de stopwords a serem utilizadas na vetorização.
        """
        self.df = df.reset_index(drop=True)
        self.stop_words = stop_words

    def tfidf_vectorization(self, output_path, max_df_custom: int, min_df_custom: float | int,
                            ngram_range_custom: tuple):
        """
        Realiza a vetorização TF-IDF e salva os resultados em um CSV.

        Args:
            output_path (str): Caminho para salvar o CSV dos resultados.
            max_df_custom (float|int): Valor máximo de frequência de documento personalizado.
            min_df_custom (int): Valor mínimo de frequência de documento personalizado.
            ngram_range_custom (tuple): Intervalo de n-gramas a serem considerados.
        """
        # Criar o vetorizador TF-IDF
        vectorizer = TfidfVectorizer(
            stop_words=self.stop_words,
            max_features=None,
            max_df=max_df_custom,
            min_df=min_df_custom,
            ngram_range=ngram_range_custom,
            sublinear_tf=True
        )

        corpus_tfidf = self.df['postMessageLimpo'].tolist()
        tfidf_matrix = vectorizer.fit_transform(corpus_tfidf)

        # Obter as palavras
        palavras_tfidf = vectorizer.get_feature_names_out()
        resultados_tfidf = []

        # Iterar sobre cada usuário
        for usuario in self.df['id_usuario'].unique():
            indices_usuario = self.df[self.df['id_usuario'] == usuario].index
            if len(indices_usuario) > 0:
                user_tfidf = tfidf_matrix[indices_usuario]
                user_tfidf_mean = np.asarray(user_tfidf.mean(axis=0)).flatten()

                top_10_indices = user_tfidf_mean.argsort()[-10:][::-1]

                for index in top_10_indices:
                    resultados_tfidf.append({
                        'id_usuario': usuario,
                        'palavra': palavras_tfidf[index],
                        'score': user_tfidf_mean[index]
                    })

        # Converter a lista de resultados em DataFrame e salvar
        resultados_df_tfidf = pd.DataFrame(resultados_tfidf)
        resultados_df_tfidf.to_csv(output_path, index=False)
        print(resultados_df_tfidf)
        return resultados_df_tfidf

    def bag_of_words_vectorization(self, output_path, max_df_custom: float | int, min_df_custom: int,
                                   ngram_range_custom: tuple):
        """
        Realiza a vetorização Bag of Words e salva os resultados em um CSV.

        Args:
            output_path (str): Caminho para salvar o CSV dos resultados.
            max_df_custom (float|int): Valor máximo de frequência de documento personalizado.
            min_df_custom (int): Valor mínimo de frequência de documento personalizado.
            ngram_range_custom (tuple): Intervalo de n-gramas a serem considerados.
        """
        vectorizer = CountVectorizer(
            stop_words=self.stop_words,
            max_df=max_df_custom,
            min_df=min_df_custom,
            ngram_range=ngram_range_custom
        )

        corpus_bow = self.df['postMessageLimpo'].tolist()
        bow_matrix = vectorizer.fit_transform(corpus_bow)

        palavras_bow = vectorizer.get_feature_names_out()
        resultados_bow = []

        for usuario in self.df['id_usuario'].unique():
            indices_usuario = self.df[self.df['id_usuario'] == usuario].index
            if len(indices_usuario) > 0:
                user_bow = bow_matrix[indices_usuario]
                user_bow_sum = np.asarray(user_bow.sum(axis=0)).flatten()

                top_10_indices_bow = user_bow_sum.argsort()[-10:][::-1]

                for index in top_10_indices_bow:
                    resultados_bow.append({
                        'id_usuario': usuario,
                        'palavra': palavras_bow[index],
                        'contagem': user_bow_sum[index]
                    })

        # Converter a lista de resultados em DataFrame e salvar
        resultados_df_bow = pd.DataFrame(resultados_bow)
        resultados_df_bow.to_csv(output_path, index=False)
        print(resultados_df_bow)
        return resultados_df_bow

    @staticmethod
    def plot_top_words(df_resultados: pd.DataFrame, column: str, title: str = None):
        """
        Plota as top 10 palavras com base na coluna (score ou contagem) e exibe um gráfico de barras.

        Args:
            df_resultados (pd.DataFrame): DataFrame contendo as palavras e suas contagens ou scores.
            column (str): Nome da coluna a ser usada para plotar (score ou contagem).
            title (str): Título do gráfico.
        """
        top_words = df_resultados.groupby('palavra')[column].sum().sort_values(ascending=False).head(10)
        top_words.plot(kind='bar', title=title)
        plt.ylabel(column)
        plt.show()
