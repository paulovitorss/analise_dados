import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


class PlotGraphs:
    def __init__(self):
        pass

    @staticmethod
    def plot_posts_per_user(posts_grouped: pd.DataFrame, output_dir: str):
        """
        Plota a quantidade de posts por usuário ao longo do tempo e salva os gráficos no diretório especificado.

        Args:
            posts_grouped (pd.DataFrame): DataFrame contendo as colunas 'id_usuario', 'periodo' e 'quantidade'.
            output_dir (str): Diretório onde os gráficos serão salvos.
        """
        # Criar o gráfico de linha para cada usuário

        for usuario in posts_grouped['id_usuario'].unique():
            df_usuario = posts_grouped[posts_grouped['id_usuario'] == usuario].copy()

            # Verifique se a conversão foi bem-sucedida
            if df_usuario['periodo'].isnull().any():
                print(f"Erro ao converter 'periodo' para o usuário {usuario}.")
                continue

            # Ordenar os dados por 'periodo'
            df_usuario = df_usuario.sort_values('periodo')

            # Configurar o gráfico de linha
            plt.figure(figsize=(20, 8))

            # Plotando diretamente o eixo x como datetime
            plt.plot(df_usuario['periodo'], df_usuario['quantidade'], marker='o', linestyle='-', color='blue')

            # Definir o formato do eixo x para mostrar datas corretamente
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Mostra uma marcação por mês

            # Adicionar título e rótulos
            plt.title(f'Quantidade de Posts por Mês/Ano - Usuário: {usuario}')
            plt.xlabel('Mês/Ano')
            plt.ylabel('Quantidade de Posts')

            # Melhorar a legibilidade dos rótulos do eixo X
            plt.xticks(rotation=45, ha='right', fontsize=10)

            # Adicionar grid
            plt.grid(True, axis='y')

            # Ajustar o layout para evitar sobreposição
            plt.tight_layout(pad=8.0)

            # Adicionar espaço extra ao layout se necessário
            plt.subplots_adjust(bottom=0.2)

            # Salvando o gráfico no diretório especificado
            plt.savefig(f'{output_dir}/quantidade_posts_{usuario}.png')

            # Mostrar o gráfico
            plt.show()

            # Fechar a figura explicitamente para liberar memória
            plt.close()
