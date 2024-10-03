import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


class PlotGraphs:

    @staticmethod
    def plot_posts_per_user(posts_grouped: pd.DataFrame, output_dir: str):
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

    @staticmethod
    def plot_posts_per_weekday(posts_grouped: pd.DataFrame, output_dir: str):

        # para a função funcionar:
        # # Adicionar uma coluna mes/ano no formato "mm/yyyy"
        # df['mes_ano'] = df['mes'].astype(str).str.zfill(2) + '/' + df['ano'].astype(str)
        #
        # # Agrupar os dados por id_usuario, mes_ano, diaDaSemana e contar a quantidade de posts
        # posts_grouped_weekday = df.groupby(['id_usuario', 'mes_ano', 'diaDaSemana']).size().reset_index(name='quantidade')
        # plot_graphs.plot_posts_per_weekday(posts_grouped_weekday, 'dados/com_filtros_datas/2meses/graficos/semana')

        # Criar o gráfico de barras para cada usuário e mês/ano
        for usuario in posts_grouped['id_usuario'].unique():
            df_usuario = posts_grouped[posts_grouped['id_usuario'] == usuario]

            for mes_ano in df_usuario['mes_ano'].unique():
                df_mes = df_usuario[df_usuario['mes_ano'] == mes_ano]

                # Ordenar os dias da semana na ordem correta
                ordem_dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado',
                              'Domingo']
                df_mes['diaDaSemana'] = pd.Categorical(df_mes['diaDaSemana'], categories=ordem_dias, ordered=True)
                df_mes = df_mes.sort_values('diaDaSemana')

                # Configurar o gráfico de barras
                plt.figure(figsize=(10, 6))
                plt.bar(df_mes['diaDaSemana'], df_mes['quantidade'], color='skyblue')

                # Adicionar título e rótulos
                plt.title(f'Quantidade de Posts por Dia da Semana - Usuário: {usuario} - {mes_ano}')
                plt.xlabel('Dia da Semana')
                plt.ylabel('Quantidade de Posts')

                # Ajustar rótulos no eixo X
                plt.xticks(rotation=45, ha='right', fontsize=10)

                # Adicionar grid
                plt.grid(True, axis='y')

                # Ajustar layout
                plt.tight_layout()

                # Salvando o gráfico no diretório especificado
                plt.savefig(f'{output_dir}/quantidade_posts_semana_{usuario}_{mes_ano.replace("/", "-")}.png')

                # Mostrar o gráfico
                plt.show()

                # Fechar a figura explicitamente para liberar memória
                plt.close()

    @staticmethod
    def plot_total_posts_per_weekday(df: pd.DataFrame):
        # Ordenar os dias da semana na ordem correta
        ordem_dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado',
                      'Domingo']

        # Contar a quantidade de postagens por dia da semana
        posts_por_dia = df['diaDaSemana'].value_counts().reindex(ordem_dias)

        # Configurar o gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(posts_por_dia.index, posts_por_dia.values, color='skyblue')

        # Adicionar título e rótulos
        plt.title('Quantidade Total de Posts por Dia da Semana (Todos os Usuários)')
        plt.xlabel('Dia da Semana')
        plt.ylabel('Quantidade de Posts')

        # Ajustar rótulos no eixo X
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Adicionar grid
        plt.grid(True, axis='y')

        # Ajustar layout
        plt.tight_layout()

        # Mostrar o gráfico
        plt.show()

        # Fechar a figura explicitamente para liberar memória
        plt.close()

    @staticmethod
    def plot_posts_and_user_percentage_per_weekday(df: pd.DataFrame):
        """
        Plota a quantidade de posts por dia da semana e a porcentagem de usuários que postam naquele dia.

        Args:
            df (pd.DataFrame): DataFrame contendo as colunas 'diaDaSemana' e 'id_usuario' com as postagens de todos os usuários.
        """
        # Ordenar os dias da semana na ordem correta
        ordem_dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado',
                      'Domingo']

        # Contar a quantidade de postagens por dia da semana
        posts_por_dia = df['diaDaSemana'].value_counts().reindex(ordem_dias, fill_value=0)

        # Contar a quantidade de usuários únicos que postaram por dia da semana
        usuarios_por_dia = df.groupby('diaDaSemana')['id_usuario'].nunique().reindex(ordem_dias, fill_value=0)

        # Total de usuários no DataFrame
        total_usuarios = df['id_usuario'].nunique()

        # Calcular a porcentagem de usuários que postam em cada dia da semana
        porcentagem_usuarios = (usuarios_por_dia / total_usuarios) * 100

        # Plotando o gráfico
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Configurar o gráfico de barras para a quantidade de postagens
        ax1.bar(posts_por_dia.index, posts_por_dia.values, color='skyblue', label='Quantidade de Posts')
        ax1.set_xlabel('Dia da Semana')
        ax1.set_ylabel('Quantidade de Posts', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')

        # Configurar o segundo eixo para a porcentagem de usuários
        ax2 = ax1.twinx()
        ax2.plot(posts_por_dia.index, porcentagem_usuarios.values, color='red', marker='o', label='% de Usuários')
        ax2.set_ylabel('Porcentagem de Usuários (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Título e ajustes de layout
        plt.title('Quantidade de Posts por Dia da Semana e Porcentagem de Usuários que Postam')
        fig.tight_layout()

        # Exibir o gráfico
        plt.show()

        # Fechar a figura explicitamente para liberar memória
        plt.close()

    @staticmethod
    def plot_posts_per_hour_per_user(df: pd.DataFrame, output_dir: str):
        # Lista de horas do dia (0 a 23)
        horas_dia = list(range(24))

        # Criar o gráfico para cada usuário
        for usuario in df['id_usuario'].unique():
            df_usuario = df[df['id_usuario'] == usuario].copy()

            # Contar a quantidade de postagens por hora
            posts_por_hora = df_usuario['hora'].value_counts().reindex(horas_dia, fill_value=0)

            # Configurar o gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(posts_por_hora.index, posts_por_hora.values, color='skyblue')

            # Adicionar título e rótulos
            plt.title(f'Quantidade de Posts por Hora - Usuário: {usuario}')
            plt.xlabel('Hora do Dia')
            plt.ylabel('Quantidade de Posts')

            # Melhorar a legibilidade dos rótulos do eixo X
            plt.xticks(horas_dia, rotation=0)

            # Adicionar grid
            plt.grid(True, axis='y')

            # Ajustar o layout para evitar sobreposição
            plt.tight_layout()

            # Salvando o gráfico no diretório especificado
            plt.savefig(f'{output_dir}/quantidade_posts_hora_{usuario}.png')

            # Mostrar o gráfico
            plt.show()

            # Fechar a figura explicitamente para liberar memória
            plt.close()

    @staticmethod
    def plot_posts_per_hour_all_users(df: pd.DataFrame, output_dir: str):
        # Lista de horas do dia (0 a 23)
        horas_dia = list(range(24))

        # Contar a quantidade de postagens por hora considerando todos os usuários
        posts_por_hora = df['hora'].value_counts().reindex(horas_dia, fill_value=0)

        # Configurar o gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(posts_por_hora.index, posts_por_hora.values, color='skyblue')

        # Adicionar título e rótulos
        plt.title(f'Quantidade Total de Posts por Hora (Todos os Usuários)')
        plt.xlabel('Hora do Dia')
        plt.ylabel('Quantidade de Posts')

        # Melhorar a legibilidade dos rótulos do eixo X
        plt.xticks(horas_dia, rotation=0)

        # Adicionar grid
        plt.grid(True, axis='y')

        # Ajustar o layout para evitar sobreposição
        plt.tight_layout()

        # Salvando o gráfico no diretório especificado
        plt.savefig(f'{output_dir}/quantidade_posts_por_hora_todos_usuarios.png')

        # Mostrar o gráfico
        plt.show()

        # Fechar a figura explicitamente para liberar memória
        plt.close()

    @staticmethod
    def plot_posts_per_hour_by_month(df: pd.DataFrame, output_dir: str):
        # Verificar se as colunas 'ano' e 'mes' existem
        if 'ano' not in df.columns or 'mes' not in df.columns:
            raise ValueError("O DataFrame deve conter as colunas 'ano' e 'mes'.")

        # Criar a coluna 'mes_ano' combinando o mês e ano usando pd.Period
        df['mes_ano'] = df['ano'].astype(str) + '-' + df['mes'].astype(str)
        df['mes_ano'] = pd.to_datetime(df['mes_ano'], format='%Y-%m').dt.to_period('M')

        # Lista de horas do dia (0 a 23)
        horas_dia = list(range(24))

        # Agrupar os dados por mês/ano
        for mes_ano, df_mes in df.groupby('mes_ano'):
            # Contar a quantidade de postagens por hora para o mês/ano específico
            posts_por_hora = df_mes['hora'].value_counts().reindex(horas_dia, fill_value=0)

            # Configurar o gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(posts_por_hora.index, posts_por_hora.values, color='skyblue')

            # Adicionar título e rótulos
            plt.title(f'Quantidade de Posts por Hora - Mês/Ano: {mes_ano}')
            plt.xlabel('Hora do Dia')
            plt.ylabel('Quantidade de Posts')

            # Melhorar a legibilidade dos rótulos do eixo X
            plt.xticks(horas_dia, rotation=0)

            # Adicionar grid
            plt.grid(True, axis='y')

            # Ajustar o layout para evitar sobreposição
            plt.tight_layout()

            # Salvando o gráfico no diretório especificado
            plt.savefig(f'{output_dir}/quantidade_posts_por_hora_{mes_ano}.png')

            # Mostrar o gráfico
            plt.show()

            # Fechar a figura explicitamente para liberar memória
            plt.close()

    @staticmethod
    def plot_posts_per_hour_per_user_by_month(df: pd.DataFrame, output_dir: str):
        """
        Plota a quantidade de posts por hora para cada usuário divididos por mês/ano e salva os gráficos no diretório especificado.

        Args:
            df (pd.DataFrame): DataFrame contendo as colunas 'id_usuario', 'hora', 'mes', 'ano'.
            output_dir (str): Diretório onde os gráficos serão salvos.
        """
        # Verificar se as colunas 'ano' e 'mes' existem
        if 'ano' not in df.columns or 'mes' not in df.columns:
            raise ValueError("O DataFrame deve conter as colunas 'ano' e 'mes'.")

        # Criar a coluna 'mes_ano' combinando o mês e ano
        df['mes_ano'] = df['ano'].astype(str) + '-' + df['mes'].astype(str)
        df['mes_ano'] = pd.to_datetime(df['mes_ano'], format='%Y-%m').dt.to_period('M')

        # Lista de horas do dia (0 a 23)
        horas_dia = list(range(24))

        # Iterar sobre cada usuário
        for usuario in df['id_usuario'].unique():
            df_usuario = df[df['id_usuario'] == usuario].copy()

            # Iterar sobre cada mês/ano
            for mes_ano, df_mes in df_usuario.groupby('mes_ano'):
                # Contar a quantidade de postagens por hora para o usuário específico e mês/ano
                posts_por_hora = df_mes['hora'].value_counts().reindex(horas_dia, fill_value=0)

                # Configurar o gráfico de barras
                plt.figure(figsize=(10, 6))
                plt.bar(posts_por_hora.index, posts_por_hora.values, color='skyblue')

                # Adicionar título e rótulos
                plt.title(f'Quantidade de Posts por Hora - Usuário: {usuario} - Mês/Ano: {mes_ano}')
                plt.xlabel('Hora do Dia')
                plt.ylabel('Quantidade de Posts')

                # Melhorar a legibilidade dos rótulos do eixo X
                plt.xticks(horas_dia, rotation=0)

                # Adicionar grid
                plt.grid(True, axis='y')

                # Ajustar o layout para evitar sobreposição
                plt.tight_layout()

                # Salvando o gráfico no diretório especificado
                plt.savefig(f'{output_dir}/quantidade_posts_hora_{usuario}_{mes_ano}.png')

                # Mostrar o gráfico
                plt.show()

                # Fechar a figura explicitamente para liberar memória
                plt.close()
