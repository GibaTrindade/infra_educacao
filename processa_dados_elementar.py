import pandas as pd

abastecimento_agua_notas = {
  'IN_AGUA_REDE_PUBLICA': 1,
  'IN_AGUA_POCO_ARTESIANO': 0.5,
  'IN_AGUA_CACIMBA': 0.3,
  'IN_AGUA_FONTE_RIO': 0.2,
  'IN_AGUA_INEXISTENTE': 0,
}
banheiro_notas = {
  'IN_BANHEIRO': 1,
  'IN_BANHEIRO_EI': 0.5,
  'IN_BANHEIRO_PNE': 0.5,
  'IN_BANHEIRO_FUNCIONARIOS': 0.5,
  'IN_BANHEIRO_CHUVEIRO': 0.5,
}
esgotamento_sanitario_notas = {
  'IN_ESGOTO_REDE_PUBLICA': 1,
  'IN_ESGOTO_FOSSA_SEPTICA': 0.5,
  'IN_ESGOTO_FOSSA_COMUM': 0.3,
  'IN_ESGOTO_FOSSA': 0.2,
  'IN_ESGOTO_INEXISTENTE': 0,
}
energia_eletrica_notas = {
  'IN_ENERGIA_REDE_PUBLICA': 1,
  'IN_ENERGIA_GERADOR_FOSSIL': 0.5,
  'IN_ENERGIA_RENOVAVEL': 1,
  'IN_ENERGIA_INEXISTENTE': 0,
 }
cozinha_notas = {
  'IN_COZINHA': 1,
  'IN_DESPENSA': 1,
 }

def calcula_notas(df, notas, regra):
  cols = list(notas.keys())

  df_notas = df.\
    query('INDICADORES == @cols'). \
    assign(NOTAS=df['INDICADORES'].map(notas)). \
    query('VALORES == 1')['NOTAS']

  if df_notas.empty:
    df_notas = pd.Series([0.0], name="NOTAS")

  if regra == 'maior valor':
    return df_notas.max()
  
  elif regra == 'soma dos valores':
    return df_notas.sum() / sum(notas.values())
  
def calcula_todas_elementar(df):
    agua_final = calcula_notas(df, abastecimento_agua_notas, 'maior valor')*0.255
    energia_final = calcula_notas(df, energia_eletrica_notas, 'maior valor')*0.250
    esgoto_final = calcula_notas(df, esgotamento_sanitario_notas, 'maior valor')*0.190
    banheiro_final = calcula_notas(df, banheiro_notas, 'soma dos valores')*0.160
    cozinha_final = calcula_notas(df, cozinha_notas, 'soma dos valores')*0.145
    
    ranking_elementar = {
    'AGUA': agua_final,
    'BANHEIRO': banheiro_final,
    'COZINHA': cozinha_final,
    'ESGOTO': esgoto_final,
    'ENERGIA': energia_final,
    }
    total_elementar_score = sum(ranking_elementar.values())

    return total_elementar_score, ranking_elementar