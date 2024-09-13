from dbm import error

import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import string
import unidecode
from wordcloud import STOPWORDS
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS
import stanza
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class TextTreatment:
    def __init__(self):
        """Constructor
        """
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt', quiet=True)
        stanza.download('pt')

    @staticmethod
    def get_stopwords() -> list:
        portuguese_ingles_stopwords = []

        # Stopwords em português
        portugues = [unidecode.unidecode(palavra.lower().replace(" ", "")) for palavra in
                     nltk.corpus.stopwords.words('portuguese')]
        portuguese_ingles_stopwords.extend(portugues)

        # Stopwords em inglês
        ingles = [unidecode.unidecode(palavra.lower().replace(" ", "")) for palavra in
                  nltk.corpus.stopwords.words('english')]
        portuguese_ingles_stopwords.extend(ingles)

        # Stopwords de diferentes fontes
        stopwords_wordcloud = [unidecode.unidecode(palavra.lower().replace(" ", "")) for palavra in STOPWORDS]
        portuguese_ingles_stopwords.extend(stopwords_wordcloud)

        stopwords_sklearn = [unidecode.unidecode(word.lower().replace(" ", "")) for word in STOP_WORDS]
        portuguese_ingles_stopwords.extend(stopwords_sklearn)

        # Adicionar stopwords do arquivo customizado
        try:
            with open('dados/datasets/stopwords-pt.txt', 'r', encoding='utf-8') as words:
                custom_stopwords = [unidecode.unidecode(word.lower().strip()) for word in words if word.strip()]
            portuguese_ingles_stopwords.extend(custom_stopwords)
        except FileNotFoundError:
            print("Arquivo de stopwords customizadas não encontrado.")

        try:
            with open('dados/datasets/girias.txt', 'r', encoding='utf-8') as words:
                girias = [unidecode.unidecode(word.lower().strip()) for word in words if word.strip()]
            portuguese_ingles_stopwords.extend(girias)
        except FileNotFoundError:
            print("Arquivo de girias não encontrado.")

        # Adicionar nomes
        try:
            with open('dados/datasets/nomes.txt', 'r', encoding='utf-8') as words:
                nomes_stopwords = [unidecode.unidecode(word.lower().strip()) for word in words if word.strip()]
            portuguese_ingles_stopwords.extend(nomes_stopwords)
        except FileNotFoundError:
            print("Arquivo de nomes não encontrado.")

        # Remover duplicatas e ordenar a lista
        portuguese_ingles_stopwords = list(set(portuguese_ingles_stopwords))
        portuguese_ingles_stopwords.sort()

        return portuguese_ingles_stopwords

    @staticmethod
    def remocao_stopword(palavra, lista_stopwords) -> str:
        return ' '.join([i for i in palavra.split() if i not in lista_stopwords])

    @staticmethod
    def remove_caracteres(text) -> str:
        # Converter para minúsculas e remover espaços em branco no início e fim
        text = text.lower().strip()

        # Remover tags HTML
        text = re.sub(r'<.*?>', '', text)

        # Remover pontuação
        text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)

        # Remover múltiplos espaços em branco
        text = re.sub(r'\s+', ' ', text)

        # Remover referências numéricas em colchetes [123]
        text = re.sub(r'\[[0-9]*]', ' ', text)

        # Remover caracteres que não são letras ou espaços
        text = re.sub(r'[^\w\s]', '', text)

        # Remover números
        text = re.sub(r'\d', ' ', text)

        # Remover símbolo de dólar
        text = re.sub(r"\$", "", text)

        # Remover URLs
        text = re.sub(r"https?://\S+|www\.\S+", '', text)

        # Remover hashtags
        text = re.sub(r"#", "", text)

        # Remover trechos com "<a href"
        text = re.sub(r'<a href.*?>', ' ', text)

        # Remover entidades HTML como &amp;
        text = re.sub(r'&amp;', '', text)

        # Remover caracteres especiais adicionais
        text = re.sub(r'[_"\-;%()|+&=*.,!?:#$@\[\]/]', ' ', text)

        # Remover quebras de linha no formato HTML
        text = re.sub(r'<br />', ' ', text)

        # Remover caracteres que não são letras (em português)
        text = re.sub(r'[^a-zà-ù ]', ' ', text)

        # Remover repetições de 'k' ou 'j' (ex.: "kkkk", "jjjj")
        text = re.sub(r'k{2,}', '', text, flags=re.IGNORECASE)
        text = re.sub(r'j{2,}', '', text, flags=re.IGNORECASE)

        # Remover emojis e caracteres unicode especiais
        text = re.sub(r"["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese characters
                      u"\U00002702-\U000027B0"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", '', text)

        return text

    @staticmethod
    def obter_pos_tag(token) -> str:
        if token.startswith('J'):
            return wordnet.ADJ
        elif token.startswith('V'):
            return wordnet.VERB
        elif token.startswith('N'):
            return wordnet.NOUN
        elif token.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    @staticmethod
    def lematizacao(palavra, op_lemmatizer=None) -> str:
        if op_lemmatizer is None:
            print("Usando o lemmatizer do spaCy")
            nlp = spacy.load("pt_core_news_sm")
            doc = nlp(palavra)
            return " ".join([token.lemma_ for token in doc])

        elif op_lemmatizer == 1:
            print("Usando o lemmatizer do NLTK")
            lemmatizer = WordNetLemmatizer()
            token = word_tokenize(palavra)
            word_pos_tags = nltk.pos_tag(token)
            return " ".join(
                [lemmatizer.lemmatize(tag[0], TextTreatment.obter_pos_tag(tag[1])) for tag in word_pos_tags])

        elif op_lemmatizer == 2:
            print("Usando o lemmatizer do Stanza")
            stanza.download('pt')  # Baixar o modelo se necessário
            nlp = stanza.Pipeline('pt')
            doc = nlp(palavra)
            return " ".join([word.lemma for sent in doc.sentences for word in sent.words])

        else:
            print("Erro: Opção inválida para lematização.")
            raise ValueError("Opção de lematização inválida")

    @staticmethod
    def preprocessamento_texto(texto_limpo) -> str:
        lista_stopwords = TextTreatment.get_stopwords()
        texto_limpo = TextTreatment.remove_caracteres(texto_limpo)
        texto_limpo = TextTreatment.remocao_stopword(texto_limpo, lista_stopwords)
        texto_limpo = TextTreatment.lematizacao(texto_limpo)
        return texto_limpo

    @staticmethod
    def finds_pandas_words(df_text):
        try:
            with open('dados/datasets/nomes_medicamentos_antidepressivos.txt', 'r', encoding='utf-8') as file:
                text_lists = [row.strip() for row in file.readlines()]
        except FileNotFoundError:
            print("Arquivo de nomes não encontrado.")

        return df_text.isin(text_lists)

    @staticmethod
    def finds_fuzzy_words(df_text):
        texts_found = []
        try:
            with open('dados/datasets/nomes_medicamentos_antidepressivos.txt', 'r', encoding='utf-8') as file:
                text_lists = [row.strip() for row in file.readlines()]
        except FileNotFoundError:
            print("Arquivo de nomes não encontrado.")

        for word in text_lists:
            results = process.extract(word, df_text, limit=2, scorer=fuzz.ratio)
            for result, similarity in results:
                if similarity >= 80:
                    texts_found.append((word, result, similarity))

        return texts_found