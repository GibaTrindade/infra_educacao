import os

def setup_diretorio():
    # Define o caminho para salvar o arquivo baixado no Windows
    current_dir = os.getcwd()  # Obtém o diretório atual
    local_dir = os.path.join(current_dir, "arquivos")
    local_file_path = os.path.join(local_dir, "microdados_ed_basica_2023.csv")
    
    # Cria o diretório se ele não existir
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Verifica se o arquivo já existe
    if os.path.exists(local_file_path):
        user_input = input(f"O arquivo '{local_file_path}' já existe. Deseja sobrescrevê-lo? (s/n): ").strip().lower()
        if user_input != 's':
            print("Usando o arquivo existente.")
            return None  # Retorna None se o usuário não quiser sobrescrever
    
    return local_file_path
