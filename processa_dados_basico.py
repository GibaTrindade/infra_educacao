import pandas as pd

salas_notas = {
  'IN_SALA_MULTIUSO': 1,
  'IN_SALA_DIRETORIA': 1,
  'IN_SALA_PROFESSOR': 1,
  'IN_SECRETARIA': 1,
 }
lixo_dest_notas = {
  'IN_LIXO_SERVICO_COLETA': 1,
  'IN_LIXO_QUEIMA': 0.2,
  'IN_LIXO_ENTERRA': 0.2,
  'IN_LIXO_DESTINO_FINAL_PUBLICO': 1,
  'IN_LIXO_DESCARTA_OUTRA_AREA': 0.5,
 }
lixo_trat_notas = {
  'IN_TRATAMENTO_LIXO_SEPARACAO': 1,
  'IN_TRATAMENTO_LIXO_REUTILIZA': 1,
  'IN_TRATAMENTO_LIXO_RECICLAGEM': 1,
  'IN_TRATAMENTO_LIXO_INEXISTENTE': 1,
 }
equipamentos_notas = {
  'IN_COMPUTADOR': 1,
  'IN_EQUIP_COPIADORA': 1,
  'IN_EQUIP_IMPRESSORA': 1,
  'IN_EQUIP_TV': 1,
  'IN_EQUIP_MULTIMIDIA':1,
  'IN_DESKTOP_ALUNO': 1,
  'IN_COMP_PORTATIL_ALUNO': 1,
  'IN_TABLET_ALUNO': 1,
 }
refeitorio_notas = {
  'IN_REFEITORIO': 1,
}
acessibilidade_notas = {
  'IN_ACESSIBILIDADE_CORRIMAO': 1,
  'IN_ACESSIBILIDADE_ELEVADOR': 1,
  'IN_ACESSIBILIDADE_PISOS_TATEIS': 1,
  'IN_ACESSIBILIDADE_VAO_LIVRE': 1,
  'IN_ACESSIBILIDADE_RAMPAS': 1,
  'IN_ACESSIBILIDADE_SINAL_SONORO': 1,
  'IN_ACESSIBILIDADE_SINAL_TATIL': 1,
  'IN_ACESSIBILIDADE_SINAL_VISUAL': 1,
  'IN_ACESSIBILIDADE_INEXISTENTE': 0,
 }
patio_notas = {
  'IN_PATIO_COBERTO': 1,
  'IN_PATIO_DESCOBERTO': 0.5,
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

## Cálculo p/lixo: Maior Valor do Destino + Maior Valor do Tratamento)/2
def calcula_notas_lixo(df):
  lixo_dest_cols = list(lixo_dest_notas.keys())
  lixo_trat_cols = list(lixo_trat_notas.keys())

  nota_destino = df.\
    query('INDICADORES == @lixo_dest_cols'). \
    assign(NOTAS=df['INDICADORES'].map(lixo_dest_notas)). \
    query('VALORES == 1')['NOTAS']
  if nota_destino.empty:
    nota_destino = pd.Series([0.0], name="NOTAS")
  nota_destino = nota_destino.max()

  nota_tratamento = df.\
    query('INDICADORES == @lixo_trat_cols'). \
    assign(NOTAS=df['INDICADORES'].map(lixo_trat_notas)). \
    query('VALORES == 1')['NOTAS']
  if nota_tratamento.empty:
    nota_tratamento = pd.Series([0.0], name="NOTAS")
  nota_tratamento = nota_tratamento.max()

  return (nota_destino + nota_tratamento) / 2


  
def calcula_todas_basico(df):
    salas_final = calcula_notas(df, salas_notas, 'soma dos valores')*0.200
    lixo_final = calcula_notas_lixo(df)*0.195
    equipamentos_final = calcula_notas(df, equipamentos_notas, 'soma dos valores')*0.190
    refeitorio_final = calcula_notas(df, refeitorio_notas, 'maior valor')*0.150
    acessibilidade_final = calcula_notas(df, acessibilidade_notas, 'soma dos valores')*0.145
    patio_final = calcula_notas(df, patio_notas, 'soma dos valores')*0.120

    
    ranking_basico = {
    'SALAS': salas_final,
    'LIXO': lixo_final,
    'EQUIPAMENTOS': equipamentos_final,
    'REFEITORIO': refeitorio_final,
    'ACESSIBILIDADE': acessibilidade_final,
    'PATIO': patio_final,
    }
    total_basico_score = sum(ranking_basico.values()) 

    return total_basico_score, ranking_basico