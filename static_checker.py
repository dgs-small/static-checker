import os

def check_file(filename):
    # Adiciona a extensão .241 ao nome do arquivo
    filename_with_extension = filename + '.241'

    # Verifica se o arquivo existe
    if os.path.exists(filename_with_extension):
        print(f"O arquivo {filename_with_extension} existe.")
    else:
        print(f"O arquivo {filename_with_extension} não foi encontrado.")

def main():
    # Solicita o nome do arquivo ao usuário
    filename = input("Digite o nome do arquivo ou caminho relativo: ")

    # Verifica se o caminho completo foi fornecido
    if os.path.isabs(filename):
        check_file(filename)
    else:
        # Se apenas o nome do arquivo foi fornecido, verifica no diretório atual
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, filename)
        check_file(file_path)

if __name__ == "__main__":
    main()
