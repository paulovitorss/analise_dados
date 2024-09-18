import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import string
import unidecode
from wordcloud import STOPWORDS
import spacy
from spacy.cli import download as spacy_download
from spacy.util import is_package
from spacy.lang.pt.stop_words import STOP_WORDS
import stanza
import os
import emoji


class TextTreatment:
    def __init__(self):
        """Constructor
        """
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        if not os.path.exists(os.path.expanduser('~/stanza_resources/pt')):
            stanza.download('pt', verbose=False)
        if not is_package("pt_core_news_sm"):
            spacy_download("pt_core_news_sm")

        # Carregar modelos uma vez durante a inicialização
        self.nlp_spacy = spacy.load("pt_core_news_sm")
        self.nlp_stanza = stanza.Pipeline('pt', processors='tokenize,mwt,pos,lemma', use_gpu=False, verbose=False)
        self.nlp_wl = WordNetLemmatizer()

        # Carregar stopwords uma vez
        self.lista_stopwords = self.get_stopwords()

    @staticmethod
    def get_stopwords() -> list:
        stopwords_total = []

        # Stopwords em português
        portugues = [unidecode.unidecode(palavra.lower().strip()) for palavra in
                     nltk.corpus.stopwords.words('portuguese')]
        stopwords_total.extend(portugues)

        # Stopwords em inglês
        ingles = [unidecode.unidecode(palavra.lower().strip()) for palavra in
                  nltk.corpus.stopwords.words('english')]
        stopwords_total.extend(ingles)

        # Stopwords de diferentes fontes
        stopwords_wordcloud = [unidecode.unidecode(palavra.lower().strip()) for palavra in STOPWORDS]
        stopwords_total.extend(stopwords_wordcloud)

        stopwords_spacy = [unidecode.unidecode(word.lower().strip()) for word in STOP_WORDS]
        stopwords_total.extend(stopwords_spacy)

        # Adicionar stopwords de arquivos customizados
        base_path = 'dados/datasets/'
        arquivos_stopwords = ['stopwords-pt.txt', 'girias.txt', 'nomes.txt']
        for nome_arquivo in arquivos_stopwords:
            caminho_arquivo = os.path.join(base_path, nome_arquivo)
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    palavras_customizadas = [unidecode.unidecode(palavra.lower().strip()) for palavra in arquivo if
                                             palavra.strip()]

                    palavras_customizadas = [re.sub(r'[^\w\s]', '', palavra) for palavra in palavras_customizadas]
                    palavras_customizadas = [re.sub(r'\s+', ' ', palavra).strip() for palavra in palavras_customizadas]
                stopwords_total.extend(palavras_customizadas)
            else:
                print(f"Arquivo '{nome_arquivo}' não encontrado.")

        # Remover duplicatas e ordenar a lista
        stopwords_total = list(set(stopwords_total))
        stopwords_total.sort()

        return stopwords_total

    @staticmethod
    def remocao_stopword(texto, lista_stopwords) -> str:
        return ' '.join([palavra for palavra in texto.split() if
                         unidecode.unidecode(palavra.lower().strip()) not in lista_stopwords])

    @staticmethod
    def remove_caracteres(texto) -> str:
        # Converter para minúsculas e remover espaços em branco no início e fim
        texto = texto.lower().strip()

        # Remover tags HTML
        texto = re.sub(r'<.*?>', '', texto)

        # Remover pontuação
        texto = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', texto)

        # Remover múltiplos espaços em branco
        texto = re.sub(r'\s+', ' ', texto)

        # Remover referências numéricas em colchetes [123]
        texto = re.sub(r'\[[0-9]*]', ' ', texto)

        # Remover caracteres que não são letras ou espaços
        texto = re.sub(r'[^\w\s]', '', texto)

        # Remover números
        texto = re.sub(r'\d', ' ', texto)

        # Remover símbolo de dólar
        texto = re.sub(r"\$", "", texto)

        # Remover URLs
        texto = re.sub(r"https?://\S+|www\.\S+", '', texto)

        # Remover hashtags
        texto = re.sub(r"#", "", texto)

        # Remover trechos com "<a href"
        texto = re.sub(r'<a href.*?>', ' ', texto)

        # Remover entidades HTML como &amp;
        texto = re.sub(r'&amp;', '', texto)

        # Remover caracteres especiais adicionais
        texto = re.sub(r'[_"\-;%()|+&=*.,!?:#$@\[\]/]', ' ', texto)

        # Remover quebras de linha no formato HTML
        texto = re.sub(r'<br />', ' ', texto)

        # Remover caracteres que não são letras (em português)
        texto = re.sub(r'[^a-zà-ù ]', ' ', texto)

        # Remover repetições de 'k' ou 'j' (ex.: "kkkk", "jjjj")
        texto = re.sub(r'k{2,}', '', texto, flags=re.IGNORECASE)
        texto = re.sub(r'j{2,}', '', texto, flags=re.IGNORECASE)
        texto = re.sub(r'ks{2,}', '', texto, flags=re.IGNORECASE)

        # Remover emojis
        texto = emoji.replace_emoji(texto, replace='')

        return texto

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

    def lematizacao(self, texto, op_lemmatizer=None) -> str:
        if op_lemmatizer is None:
            # Usar Spacy para lematização por padrão
            doc = self.nlp_spacy(texto)
            return " ".join([token.lemma_ for token in doc])

        elif op_lemmatizer == 1:
            token = word_tokenize(texto)
            word_pos_tags = nltk.pos_tag(token)
            return " ".join(
                [self.nlp_wl.lemmatize(tag[0], TextTreatment.obter_pos_tag(tag[1])) for tag in word_pos_tags])

        elif op_lemmatizer == 2:
            # Usar Stanza para lematização
            doc = self.nlp_stanza(texto)
            return " ".join([word.lemma for sent in doc.sentences for word in sent.words])

        else:
            print("Erro: Opção inválida para lematização.")
            raise ValueError("Opção de lematização inválida")

    def preprocessamento_texto(self, texto, op_lemmatizer=None) -> str:
        texto = TextTreatment.remove_caracteres(texto)
        texto = unidecode.unidecode(texto)
        texto = TextTreatment.remocao_stopword(texto, self.lista_stopwords)
        texto = self.lematizacao(texto, op_lemmatizer)
        return texto