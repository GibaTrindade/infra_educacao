def filtra_dados_pe(df_base):
    return df_base.query('NU_ANO_CENSO == 2023 and SG_UF == "PE"')

def filtra_esfera_estadual(df_base):
    return df_base.query('TP_DEPENDENCIA == 2')

def filtra_escola_específica(df_basePE, school_name):
    return df_basePE.query(f'NO_ENTIDADE == "{school_name}" and NO_MUNICIPIO == "Carpina"')

def filtra_escola_cod(df_basePE, cod):
    return df_basePE.query(f'CO_ENTIDADE == {cod}')
