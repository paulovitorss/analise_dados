import pymongo
from pymongo.collection import Collection

class MongoDBConnection:
    """
    Classe para gerenciar a conexão com o MongoDB.

    Atributos:
        uri (str): A URI de conexão com o MongoDB.
        database_name (str): Nome do banco de dados.
        collection_name (str): Nome da coleção.
    """

    def __init__(self, uri: str, database_name: str, collection_name: str):
        """
        Inicializa a conexão com o MongoDB.

        Args:
            uri (str): URI de conexão ao MongoDB.
            database_name (str): Nome do banco de dados.
            collection_name (str): Nome da coleção.
        """
        self.uri = uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self) -> None:
        """
        Conecta ao banco de dados MongoDB e seleciona a coleção.

        Raises:
            Exception: Caso ocorra erro ao conectar com o banco de dados.
        """
        try:
            self.client = pymongo.MongoClient(self.uri)
            # Tenta acessar a lista de coleções para validar a conexão
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            print("Conexão estabelecida com sucesso ao banco de dados.")
        except Exception as e:
            print('Erro ao conectar com o banco de dados. Erro: {}'.format(e))

    def get_collection(self) -> Collection:
        if not self.collection:
            raise Exception("A conexão com o banco de dados não foi estabelecida ou a coleção não está disponível.")
        return self.collection