import os
from dotenv import load_dotenv
import gdown
from setup_dir import setup_diretorio
from carrega_dados import carrega_base_dados
from filtra_dados import filtra_dados_pe, filtra_escola_específica, filtra_escola_cod, filtra_esfera_estadual
from processa_dados import processa_dados_agua
from processa_dados_elementar import calcula_todas_elementar
from processa_dados_basico import calcula_todas_basico
from processa_dados_adequado import calcula_todas_adequado
from etl_dados import pivota_matriz
import pandas as pd
import math

def main():
    
    #  #Carrega as variáveis de ambiente do arquivo .env
    # load_dotenv()

    # Obtém o ID do arquivo do Google Drive a partir do .env
    # file_id = os.getenv("FILE_ID")

    # Configura o diretório e obtém o caminho do arquivo
    lista_arquivos = setup_diretorio()

    tabela_escola_final = pd.DataFrame()
    df_resultados_elementar_final = pd.DataFrame()
    df_resultados_basico_final = pd.DataFrame()
    df_resultados_adequado_final = pd.DataFrame()
    df_resultado_nivel_final = pd.DataFrame()
    df_resultado_geral_final = pd.DataFrame()

    for local_file_path in lista_arquivos:
        # local_file_path = setup_diretorio()
        if not local_file_path:
            print("Arquivo não está na pasta.")

        print(local_file_path)
        # Dividir o caminho pelo separador '\'
        partes = local_file_path.split(os.sep)
        ano = ""
        # Encontrar a parte que contém o padrão 'microdados_ed_basica_'
        for parte in partes:
            if 'microdados_ed_basica_' in parte:
                # Extrair o ano a partir da string
                ano = parte.split('_')[-1].split('.')[0]
                break

        
            
        
        # if local_file_path:  # Somente faz o download se o caminho for válido
        #     # ID do arquivo no Google Drive
        #     drive_url = f"https://drive.google.com/uc?id={file_id}"

        #     # Baixa o arquivo usando gdown
        #     print("Baixando o arquivo do Google Drive...")
        #     gdown.download(drive_url, local_file_path, quiet=False)
        # else:
        #     print("Pulando o download. Continuando com o arquivo existente...")

        # Define o caminho correto do arquivo (mesmo se o download for ignorado)
        # local_file_path = os.path.join("arquivos", "microdados_ed_basica_2023.csv")

        # Carrega base de dados
        df_base = carrega_base_dados(local_file_path)
        
        # Filtra dados
        df_basePE = filtra_dados_pe(df_base)
        df_basePE = filtra_esfera_estadual(df_basePE)

        
        num_escolas = 0
        resultados_elementar = []
        resultados_basico = []
        resultados_adequado = []
        resultado_geral = []
        resultado_nivel = []
        for codigo in df_basePE['CO_ENTIDADE']:
        
                # Processa dados
                df_basePE_amostra = filtra_escola_cod(df_basePE, codigo)
                # Pivota matriz
                df_basePE_amostra = pivota_matriz(df_basePE_amostra)
                # Calcula Elementar
                ranking_elementar, elementar_notas = calcula_todas_elementar(df_basePE_amostra)
                ranking_elementar = round(ranking_elementar, 3)

                for indicador, nota in elementar_notas.items():
                    resultados_elementar.append({
                        "CO_ENTIDADE": codigo,
                        "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],  # Assumindo que a coluna NU_ANO_CENSO está presente
                        "INDICADOR": indicador,
                        "NOTA": round(nota, 3)
                    })
                resultado_nivel.append({
                    "CO_ENTIDADE": codigo,
                    "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],
                    "NIVEL": "ELEMENTAR",
                    "NOTA": ranking_elementar
                })

                # Calcula Básico
                ranking_basico, basico_notas = calcula_todas_basico(df_basePE_amostra)
                ranking_basico = round(ranking_basico, 3)

                for indicador, nota in basico_notas.items():
                    resultados_basico.append({
                        "CO_ENTIDADE": codigo,
                        "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],  # Assumindo que a coluna NU_ANO_CENSO está presente
                        "INDICADOR": indicador,
                        "NOTA": round(nota, 3)
                    })

                resultado_nivel.append({
                    "CO_ENTIDADE": codigo,
                    "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],
                    "NIVEL": "BASICO",
                    "NOTA": ranking_basico
                })
                # Calcula Adequado
                ranking_adequado, adequado_notas = calcula_todas_adequado(df_basePE_amostra)
                ranking_adequado = round(ranking_adequado, 3)

                for indicador, nota in adequado_notas.items():
                    resultados_adequado.append({
                        "CO_ENTIDADE": codigo,
                        "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],  # Assumindo que a coluna NU_ANO_CENSO está presente
                        "INDICADOR": indicador,
                        "NOTA": round(nota, 3)
                    })
                resultado_nivel.append({
                    "CO_ENTIDADE": codigo,
                    "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],
                    "NIVEL": "ADEQUADO",
                    "NOTA": ranking_adequado
                })
                
                nota_geral = (ranking_elementar*0.2) + (ranking_basico*0.3) + (ranking_adequado*0.5)

                resultado_geral.append({
                    "CO_ENTIDADE": codigo,
                    "NU_ANO_CENSO": df_basePE_amostra["NU_ANO_CENSO"].iloc[0],
                    "NOTA_GERAL": round(nota_geral,3)
                })


        tabela_escola = df_basePE[[
            'NU_ANO_CENSO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'NO_UF', 
            'SG_UF', 'CO_UF', 'NO_MUNICIPIO', 'CO_MUNICIPIO', 
            'TP_DEPENDENCIA', 'TP_LOCALIZACAO','QT_MAT_FUND_AF', 'QT_MAT_MED'
        ]]

        df_resultados_elementar = pd.DataFrame(resultados_elementar)
        df_resultados_basico = pd.DataFrame(resultados_basico)
        df_resultados_adequado = pd.DataFrame(resultados_adequado)
        df_resultado_nivel = pd.DataFrame(resultado_nivel)
        df_resultado_geral = pd.DataFrame(resultado_geral)
        

        # # Mostra o DataFrame final
        # print(df_resultados_elementar)
        # print(df_resultados_basico)
        # print(df_resultados_adequado)
        # print(df_resultado_nivel)
        
        # tabela_escola.to_csv(f'arquivos/tabela_escola_{ano}.csv', sep=';', encoding='utf-8', index=False)
        tabela_escola_final = pd.concat([tabela_escola_final, tabela_escola], ignore_index=True)
        df_resultados_elementar_final = pd.concat([df_resultados_elementar_final, df_resultados_elementar], ignore_index=True)
        df_resultados_basico_final = pd.concat([df_resultados_basico_final, df_resultados_basico], ignore_index=True)
        df_resultados_adequado_final = pd.concat([df_resultados_adequado_final, df_resultados_adequado], ignore_index=True)
        df_resultado_nivel_final = pd.concat([df_resultado_nivel_final, df_resultado_nivel], ignore_index=True)
        df_resultado_geral_final = pd.concat([df_resultado_geral_final, df_resultado_geral], ignore_index=True)


        # df_resultados_elementar.to_csv(f'arquivos/resultados_elementar_{ano}.csv', sep=';', encoding='utf-8', index=False)
        # df_resultados_basico.to_csv(f'arquivos/resultados_basico_{ano}.csv', sep=';', encoding='utf-8', index=False)
        # df_resultados_adequado.to_csv(f'arquivos/resultados_adequado_{ano}.csv', sep=';', encoding='utf-8', index=False)
        # df_resultado_nivel.to_csv(f'arquivos/resultados_nivel_{ano}.csv', sep=';', encoding='utf-8', index=False)
        # df_resultado_geral.to_csv(f'arquivos/resultados_geral_{ano}.csv', sep=';', encoding='utf-8', index=False)
    tabela_escola_final.to_csv(f'arquivos/tabela_escola_final.csv', sep=';', encoding='utf-8', index=False)
    df_resultados_elementar_final.to_csv(f'arquivos/resultados_elementar_final.csv', sep=';', encoding='utf-8', index=False)
    df_resultados_basico_final.to_csv(f'arquivos/resultados_basico_final.csv', sep=';', encoding='utf-8', index=False)
    df_resultados_adequado_final.to_csv(f'arquivos/resultados_adequado_final.csv', sep=';', encoding='utf-8', index=False)
    df_resultado_nivel_final.to_csv(f'arquivos/resultados_nivel_final.csv', sep=';', encoding='utf-8', index=False)
    df_resultado_geral_final.to_csv(f'arquivos/resultados_geral_final.csv', sep=';', encoding='utf-8', index=False)
if __name__ == "__main__":
    main()
