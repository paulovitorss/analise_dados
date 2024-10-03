from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


class NuvemPalavras:
    def __init__(self):
        """Construtor"""
        pass

    @staticmethod
    def plot_nuvem_palavras(palavras):
        """
        Plota a nuvem de palavras com base nas frequências fornecidas.

        Args:
            palavras (dict): Dicionário com as palavras e suas frequências.
        """
        stop_words = stopwords.words('portuguese')

        # Criar o objeto WordCloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            stopwords=stop_words,
            background_color='white',
            max_font_size=150,
            max_words=800,
            min_font_size=1,
            collocation_threshold=2,
            collocations=False).generate_from_frequencies(palavras)

        # Exibir o objeto WordCloud
        plt.figure(figsize=(20, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
