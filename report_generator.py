def generate_report(filename, report_filename):
    # Nome do arquivo de relatório
    report_filename_with_extension = report_filename + '.lex'

    # Tenta abrir o arquivo de entrada
    try:
        with open(filename, 'r') as input_file:
            content = input_file.read()
    except FileNotFoundError:
        print(f"O arquivo {filename} não foi encontrado.")
        return

    # Cria o arquivo de relatório e escreve as informações
    with open(report_filename_with_extension, 'w') as report_file:
        report_file.write("Titulo: Relatorio de Informacoes:\n")
        report_file.write("Conteudo:\n")
        report_file.write(content)

    print(f"Relatório gerado com sucesso: {report_filename_with_extension}")
