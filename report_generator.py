def read_code_file(filename, report_filename):
    try:
        with open(filename, 'r') as input_file:
            content = input_file.read()
    except FileNotFoundError:
        print(f"O arquivo {filename} não foi encontrado.")
        return
    
    generate_report_files(report_filename, content, filename)


def generate_report_files(report_filename, content, code_filename):
    report_file_header = """Codigo da Equipe: EQ01\nComponentes:
    Tiago Galvão Pinho; tiagog.pinho@ucsal.edu.br; (71)98366-3017
    João Marcos Gatis Araújo Silva; joaomg.silva@ucsal.edu.br; (71)99900-9154
    Gabriel Pinheiro Pedreira; gabriel.pedreira@ucsal.edu.br; (71)98125-6355
    Lucas Moreno Dantas Santos; lucasmoreno.santos@ucsal.edu.br; (71)99670-7576\n"""

    # Cria o arquivo de relatório .LEX
    lex_reportfile_name = report_filename + '.LEX'
    with open(lex_reportfile_name, 'w') as report_file_lex:
        report_file_lex.write(f"{report_file_header}\n")
        report_file_lex.write(f"RELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {code_filename}\n")
        report_file_lex.write("Conteudo:\n")
        report_file_lex.write(content)

    print(f"Relatório gerado com sucesso: {lex_reportfile_name}")
    
    # Cria o arquivo de relatório .TAB
    tab_reportfile_name = report_filename + '.TAB'
    with open(tab_reportfile_name, 'w') as report_file_tab:
        report_file_tab.write(f"{report_file_header}\n")
        report_file_tab.write(f"RELATÓRIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {code_filename}\n")
        report_file_tab.write("Conteudo:\n")
        report_file_tab.write(content)
        
    print(f"Relatório gerado com sucesso: {tab_reportfile_name}")