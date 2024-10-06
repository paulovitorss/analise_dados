import pymongo
import logging
from datetime import datetime

# Configurando o logger
logging.basicConfig(level=logging.INFO)


class CollectionFilters:
    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection
        self.collection_name_out = None

    def check_or_create_collection(self, pipeline, collection_name_out):
        self.collection_name_out = collection_name_out
        # Acessa o banco de dados diretamente a partir da coleção
        db = self.collection.database

        # Verificando se a coleção de saída já existe
        if self.collection_name_out in db.list_collection_names():
            logging.info(f'A coleção já existe: {self.collection_name_out}')
        else:
            # Executa o pipeline na coleção atual e cria a nova coleção
            logging.info(f'Criando a coleção: {self.collection_name_out}')
            self.collection.aggregate(pipeline)

        # Atualiza a coleção atual para a nova coleção criada ou existente
        self.collection = db[self.collection_name_out]

        return self.collection

    def apply_pipeline1(self, collection_name_out: str):
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
                '$out': collection_name_out
            }
        ]

        self.check_or_create_collection(pipeline1, collection_name_out)

    def apply_pipeline2(self, time1: int, time2: int, collection_name_out: str):
        time1_millis = time1 * 365.25 * 24 * 60 * 60 * 1000
        time2_millis = time2 * 365.25 * 24 * 60 * 60 * 1000

        pipeline2 = [
            {
                '$addFields': {
                    'firstPostDate': {
                        '$toLong': {
                            '$arrayElemAt': [
                                '$posts.created_time', -1
                            ]
                        }
                    },
                    'lastPostDate': {
                        '$toLong': {
                            '$arrayElemAt': [
                                '$posts.created_time', 0
                            ]
                        }
                    }
                }
            },
            {
                '$addFields': {
                    'diff': {
                        '$subtract': [
                            '$lastPostDate', '$firstPostDate'
                        ]
                    }
                }
            },
            {
                '$match': {
                    '$and': [
                        {'diff': {'$gte': time2_millis}},
                        {'diff': {'$lte': time1_millis}}
                    ]
                }
            },
            {
                '$out': collection_name_out
            }
        ]

        self.check_or_create_collection(pipeline2, collection_name_out)

    def apply_pipeline3(self, collection_name_out: str):
        pipeline3 = [
            {
                '$unwind': '$posts'
            }, {
                '$project': {
                    '_id': '$posts._id',
                    'idade': 1,
                    'sexo': 1,
                    'id_usuario': 1,
                    'pessimismo': {
                        '$arrayElemAt': [
                            '$respostas.pessimismo', 0
                        ]
                    },
                    'tristeza': {
                        '$arrayElemAt': [
                            '$respostas.tristeza', 0
                        ]
                    },
                    'fracasso': {
                        '$arrayElemAt': [
                            '$respostas.fracasso', 0
                        ]
                    },
                    'prazer': {
                        '$arrayElemAt': [
                            '$respostas.prazer', 0
                        ]
                    },
                    'culpa': {
                        '$arrayElemAt': [
                            '$respostas.culpa', 0
                        ]
                    },
                    'punicao': {
                        '$arrayElemAt': [
                            '$respostas.punicao', 0
                        ]
                    },
                    'estima': {
                        '$arrayElemAt': [
                            '$respostas.estima', 0
                        ]
                    },
                    'critica': {
                        '$arrayElemAt': [
                            '$respostas.critica', 0
                        ]
                    },
                    'suicida': {
                        '$arrayElemAt': [
                            '$respostas.suicida', 0
                        ]
                    },
                    'choro': {
                        '$arrayElemAt': [
                            '$respostas.choro', 0
                        ]
                    },
                    'agitacao': {
                        '$arrayElemAt': [
                            '$respostas.agitacao', 0
                        ]
                    },
                    'interesse': {
                        '$arrayElemAt': [
                            '$respostas.interesse', 0
                        ]
                    },
                    'indecisao': {
                        '$arrayElemAt': [
                            '$respostas.indecisao', 0
                        ]
                    },
                    'desvalorizacao': {
                        '$arrayElemAt': [
                            '$respostas.desvalorizacao', 0
                        ]
                    },
                    'energia': {
                        '$arrayElemAt': [
                            '$respostas.energia', 0
                        ]
                    },
                    'sono': {
                        '$arrayElemAt': [
                            '$respostas.sono', 0
                        ]
                    },
                    'irritabilidade': {
                        '$arrayElemAt': [
                            '$respostas.irritabilidade', 0
                        ]
                    },
                    'apetite': {
                        '$arrayElemAt': [
                            '$respostas.apetite', 0
                        ]
                    },
                    'concentracao': {
                        '$arrayElemAt': [
                            '$respostas.concentracao', 0
                        ]
                    },
                    'fadiga': {
                        '$arrayElemAt': [
                            '$respostas.fadiga', 0
                        ]
                    },
                    'int_sexo': {
                        '$arrayElemAt': [
                            '$respostas.int_sexo', 0
                        ]
                    },
                    'quantAmigos': '$friends.summary.total_count',
                    'postMessage': '$posts.message',
                    'postStory': '$posts.story',
                    'postCreatedTime': '$posts.created_time',
                    'diaDaSemana': {
                        '$switch': {
                            'branches': [
                                {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 1
                                        ]
                                    },
                                    'then': 'Domingo'
                                }, {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 2
                                        ]
                                    },
                                    'then': 'Segunda-feira'
                                }, {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 3
                                        ]
                                    },
                                    'then': 'Terça-feira'
                                }, {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 4
                                        ]
                                    },
                                    'then': 'Quarta-feira'
                                }, {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 5
                                        ]
                                    },
                                    'then': 'Quinta-feira'
                                }, {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 6
                                        ]
                                    },
                                    'then': 'Sexta-feira'
                                }, {
                                    'case': {
                                        '$eq': [
                                            {
                                                '$dayOfWeek': '$posts.created_time'
                                            }, 7
                                        ]
                                    },
                                    'then': 'Sábado'
                                }
                            ],
                            'default': 'Desconhecido'
                        }
                    }
                }
            },
            {
                '$out': collection_name_out
            }
        ]

        self.check_or_create_collection(pipeline3, collection_name_out)

    def apply_pipeline4(self, collection_name_out: str):
        pipeline4 = [
            {
                '$match': {
                    'diaDaSemana': {'$ne': 'Desconhecido'}
                }
            },
            {
                '$out': collection_name_out
            }
        ]
        self.check_or_create_collection(pipeline4, collection_name_out)

    def apply_pipeline5(self, collection_name_out: str, data_inicio: datetime, data_fim: datetime):
        pipeline5 = [
            {
                '$match': {
                    'postCreatedTime': {
                        '$gte': data_fim,
                        '$lt': data_inicio
                    }
                }
            },
            {
                '$out': collection_name_out
            }
        ]

        # Verifica se a nova coleção será criada ou já existe
        self.check_or_create_collection(pipeline5, collection_name_out)

    def apply_pipeline6(self, collection_name_out: str):
        pipeline6 = [
            {
                '$unwind': '$likes'
            }, {
                '$project': {
                    '_id': '$likes._id',
                    'id_usuario': 1,
                    'likeCreatedTime': '$likes.created_time'
                },
            },
            {
                '$out': collection_name_out
            }
        ]
        self.check_or_create_collection(pipeline6, collection_name_out)

    def quant_users_cat(self, field: str, operator: str, level: int | str):
        pipeline = [
            {
                '$match': {
                    f"{field}": {
                        f"{operator}": level
                    }
                }
            },
            {
                '$group': {
                    '_id': '$id_usuario'
                }
            },
            {
                '$count': 'numero_de_usuarios_unicos'
            }
        ]

        # Executando a agregação
        resultado = list(self.collection.aggregate(pipeline))

        return resultado[0]['numero_de_usuarios_unicos'] if resultado else 0

    def count_users_by_gender(self, field: str, operator: str, level: int | str, gender: str):

        pipeline = [
            {
                '$match': {
                    f"{field}": {
                        f"{operator}": level
                    },
                    'sexo': gender
                }
            },
            {
                '$group': {
                    '_id': '$id_usuario'  # Agrupa por id_usuario
                }
            },
            {
                '$count': f'numero_de_usuarios_{gender.lower()}'
            }
        ]

        # Executando a agregação
        resultado = list(self.collection.aggregate(pipeline))

        return resultado[0][f'numero_de_usuarios_{gender.lower()}'] if resultado else 0
