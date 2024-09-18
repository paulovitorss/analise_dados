from prophet import Prophet

class FacebookProphet:

    @staticmethod
    def prophet(df, coluna_data):
        df_grouped = df.groupby(df[coluna_data].dt.date).size().reset_index(name='y')

        # Renomear a coluna de data para 'ds', como o Prophet espera
        df_grouped.rename(columns={coluna_data: 'ds'}, inplace=True)

        # Instanciar o modelo Prophet
        model = Prophet()

        # Ajustar o modelo aos dados
        model.fit(df_grouped)

        # Criar um DataFrame com datas futuras para previsão (30 dias no futuro)
        future = model.make_future_dataframe(periods=30)

        # Fazer as previsões
        forecast = model.predict(future)

        # Plotar as previsões
        model.plot(forecast)

        # Plotar os componentes das previsões (tendência, sazonalidade)
        model.plot_components(forecast)