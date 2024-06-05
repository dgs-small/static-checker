import sys
import os
from report_generator import generate_report

def main():
    # Solicita o nome do arquivo ao usuário
    filename = input("Digite o nome do arquivo (sem a extensão .241): ")
    filename_with_extension = filename + '.241'
    
    # Verifica se o caminho completo foi fornecido
    if not os.path.exists(filename_with_extension):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, filename_with_extension)
    else:
        file_path = filename_with_extension

    # Chama a função generate_report passando o nome do arquivo como argumento
    generate_report(file_path, filename)

if __name__ == "__main__":
    main()
