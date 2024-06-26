import os

from utils import reserved_words_and_symbols_table, token_table, generate_report_files
from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable
from lexical_table import LexicalTable


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

    file_content = read_code_file(file_path, filename)

    start_lexical_analyser(file_content, filename, file_path)


def start_lexical_analyser(file_content, filename, file_path):
    if file_content is not None:
        lexical_analyser = LexicalAnalyzer(
            reserved_words_and_symbols_table(),
            token_table(),
            SymbolTable(),
            LexicalTable(),
        )
        lexical_analyser.analyze(file_content)
        
        filled_symbol_table = lexical_analyser.symbol_table.table
        filled_lexical_table = lexical_analyser.lexical_table.table
        
        generate_report_files(filename, filled_symbol_table, filled_lexical_table, file_path)


def read_code_file(filename, report_filename):
    try:
        with open(filename, "r") as input_file:
            content = input_file.read()
    except FileNotFoundError:
        print(f"O arquivo {filename} não foi encontrado.")
        return

    return content


if __name__ == "__main__":
    main()
