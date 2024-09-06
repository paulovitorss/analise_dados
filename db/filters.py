import pymongo


class CollectionFilters:
    def __init__(self, db: pymongo.database.Database, collection_name: str, collection_name_out: str):
        """
        Inicializa o nome da coleção e a conexão com o banco de dados.

        Args:
            db (pymongo.database.Database): Conexão com o banco de dados.
            collection_name (str): Nome da coleção de verificação.
            collection_name_out (str): Nome da coleção de saída.
        """
        self.db = db
        self.collection_name = collection_name
        self.collection_name_out = collection_name_out

    def apply_pipeline1(self):
        """
        Aplica o pipeline à coleção e cria/seleciona a coleção de saida.

        Returns:
            pymongo.collection.Collection: A coleção com os dados filtrados.
        """

        # Seleciona a coleção de dados
        collection = self.db[self.collection_name]

        # Verificando se a coleção já existe
        if self.collection_name_out in self.db.list_collection_names():
            print('A coleção já existe')
            collection = self.db[self.collection_name_out]
        else:
            # Define o pipeline para filtrar os dados e criar a nova coleção
            pipeline1 = [
                {
                    '$match': {
                        'posts': {
                            '$exists': True,
                            '$ne': []
                        }
                    }
                },
                {
                    '$match': {
                        'autoriza': 'S'
                    }
                },
                {
                    '$match': {
                        'public_profile.locale': 'pt_BR'
                    }
                },
                {
                    '$out': self.collection_name_out  # Saída dos dados na coleção 'collection_name_out'
                }
            ]
            # Executa o pipeline e cria a coleção filtrada
            collection.aggregate(pipeline1)
            collection = self.db[self.collection_name_out]

        return collection
