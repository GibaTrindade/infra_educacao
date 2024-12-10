import pandas as pd

lab_info_notas = {
  'IN_LABORATORIO_INFORMATICA': 1,
 }
internet_notas = {
  'IN_INTERNET_ALUNOS': 1,
  'IN_INTERNET_ADMINISTRATIVO': 1,
  'IN_INTERNET_APRENDIZAGEM': 1,
  'IN_ACESSO_INTERNET_COMPUTADOR': 1,
  'IN_ACES_INTERNET_DISP_PESSOAIS': 1,
 }
biblioteca_notas = {
  'IN_BIBLIOTECA': 1,
 }
quadra_notas = {
  'IN_QUADRA_ESPORTES_COBERTA': 1,
  'IN_QUADRA_ESPORTES_DESCOBERTA': 0.5,
 }
alimentacao_notas = {
  'IN_ALIMENTACAO': 1,
 }
auditorio_notas = {
  'IN_AUDITORIO': 1,
 }
area_verde_notas = {
  'IN_AREA_VERDE': 1,
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
  
def calcula_todas_adequado(df):
    lab_info_final = calcula_notas(df, lab_info_notas, 'soma dos valores')*0.200
    internet_final = calcula_notas(df, internet_notas, 'soma dos valores')*0.185
    biblioteca_final = calcula_notas(df, biblioteca_notas, 'soma dos valores')*0.185
    quadra_final = calcula_notas(df, quadra_notas, 'maior valor')*0.125
    auditorio_final = calcula_notas(df, auditorio_notas, 'soma dos valores')*0.100
    area_verde_final = calcula_notas(df, area_verde_notas, 'soma dos valores')*0.09
    alimentacao_final = calcula_notas(df, alimentacao_notas, 'maior valor')*0.115
    
    ranking_adequado = {
      'LAB_INFO': lab_info_final,
      'INTERNET': internet_final,
      'BIBLIOTECA': biblioteca_final,
      'QUADRA': quadra_final,
      'AUDITORIO': auditorio_final,
      'AREA_VERDE': area_verde_final,
      'ALIMENTACAO': alimentacao_final,
    }
    total_adequado_score = sum(ranking_adequado.values())

    return total_adequado_score, ranking_adequado