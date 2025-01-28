import os

def setup_diretorio():
    # Define o caminho para salvar o arquivo baixado no Windows
    current_dir = os.getcwd()  # Obtém o diretório atual
    local_dir = os.path.join(current_dir, "arquivos")
    local_file_path = os.path.join(local_dir, "microdados_ed_basica_2023.csv")
    
    # Cria o diretório se ele não existir
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Lista todos os arquivos no diretório que começam com 'microdados_ed_basica_'
    arquivos = [
        os.path.join(local_dir, arquivo)
        for arquivo in os.listdir(local_dir)
        if arquivo.startswith('microdados_ed_basica_')
    ]
    
    return arquivos
