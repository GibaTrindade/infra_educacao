def processa_dados_agua(df):
    colunas_agua = ['IN_AGUA_REDE_PUBLICA', 'IN_AGUA_POCO_ARTESIANO', 'IN_AGUA_CACIMBA', 'IN_AGUA_FONTE_RIO', 'IN_AGUA_INEXISTENTE']
    df['Agua_Final'] = df[colunas_agua].apply(lambda row: 0 if row.sum() == 0 else row.max() * 0.255, axis=1)
    return df
