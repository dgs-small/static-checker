def generate_report(filename):
    report_filename = filename + '.lex'

    try:
        with open(filename, 'r') as input_file:
            content = input_file.read()
    except FileNotFoundError:
        print(f"O arquivo {filename} não foi encontrado.")
        return
    
    with open(report_filename, 'w') as report_file:
        report_file.write("Titulo: Relatorio de Informacoes:\n")
        report_file.write("Conteudo:\n")
        report_file.write(content)

    print(f"Relatório gerado com sucesso: {report_filename}")
