import os

from utils import generate_report_files


def main():
    # Solicita o nome do arquivo ao usuário
    filename = input("Digite o nome do arquivo (sem a extensão .241): ")
    filename_with_extension = filename + ".241"

    # Verifica se o caminho completo foi fornecido
    if not os.path.exists(filename_with_extension):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, filename_with_extension)
    else:
        file_path = filename_with_extension

    read_code_file(file_path, filename)


def read_code_file(filename, report_filename):
    try:
        with open(filename, "r") as input_file:
            content = input_file.read()
    except FileNotFoundError:
        print(f"O arquivo {filename} não foi encontrado.")
        return

    generate_report_files(report_filename, content, filename)


if __name__ == "__main__":
    main()
