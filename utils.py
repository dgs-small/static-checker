def reserved_words_and_symbols_table():
    reserved_words_and_symbols = {
        "cadeia": "A01",
        "caracter": "A02",
        "declaracoes": "A03",
        "enquanto": "A04",
        "false": "A05",
        "fimDeclaracoes": "A06",
        "fimEnquanto": "A07",
        "fimFunc": "A08",
        "fimFuncoes": "A09",
        "fimPrograma": "A10",
        "fimSe": "A11",
        "funcoes": "A12",
        "imprime": "A13",
        "inteiro": "A14",
        "logico": "A15",
        "pausa": "A16",
        "programa": "A17",
        "real": "A18",
        "retorna": "A19",
        "se": "A20",
        "senao": "A21",
        "tipoFunc": "A22",
        "tipoParam": "A23",
        "tipoVar": "A24",
        "true": "A25",
        "vazio": "A26",
        "%": "B01",
        "(": "B02",
        ")": "B03",
        ",": "B04",
        ":": "B05",
        ":=": "B06",
        ";": "B07",
        "?": "B08",
        "[": "B09",
        "]": "B10",
        "{": "B11",
        "}": "B12",
        "-": "B13",
        "*": "B14",
        "/": "B15",
        "+": "B16",
        "!=": "B17",
        "#": "B17",
        "<": "B18",
        "<=": "B19",
        "==": "B20",
        ">": "B21",
        ">=": "B22",
    }

    return reserved_words_and_symbols


def token_table():
    token_table = {
        "consCadeia": "C01",
        "consCaracter": "C02",
        "consInteiro": "C03",
        "consReal": "C04",
        "nomFuncao": "C05",
        "nomPrograma": "C06",
        "variavel": "C07",
    }

    return token_table


def generate_report_files(report_filename, content, code_filename):
    report_file_header = """Codigo da Equipe: EQ01\nComponentes:
    Tiago Galvão Pinho; tiagog.pinho@ucsal.edu.br; (71)98366-3017
    João Marcos Gatis Araújo Silva; joaomg.silva@ucsal.edu.br; (71)99900-9154
    Gabriel Pinheiro Pedreira; gabriel.pedreira@ucsal.edu.br; (71)98125-6355
    Lucas Moreno Dantas Santos; lucasmoreno.santos@ucsal.edu.br; (71)99670-7576\n"""

    # Cria o arquivo de relatório .LEX
    lex_reportfile_name = report_filename + ".LEX"
    with open(lex_reportfile_name, "w") as report_file_lex:
        report_file_lex.write(f"{report_file_header}\n")
        report_file_lex.write(
            f"RELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {code_filename}\n"
        )
        report_file_lex.write(
            "---------------------------------------------------------\n"
        )
        report_file_lex.write("A fazer")
        # for entry in content:
        #     report_file_tab.write(
        #         f"----------------------------------------------------------------------------\nLexeme: {entry.get('lexeme')}, Código: {entry.get('atom_code')}, IndiceTabSimb: {entry.get('entry_number')}, Linha: {str(entry.get('lines'))}\n"
        #     )
        

    print(f"Relatório gerado com sucesso: {lex_reportfile_name}")

    # Cria o arquivo de relatório .TAB
    tab_reportfile_name = report_filename + ".TAB"
    with open(tab_reportfile_name, "w") as report_file_tab:
        report_file_tab.write(f"{report_file_header}\n")
        report_file_tab.write(
            f"RELATÓRIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {code_filename}\n"
        )

        for entry in content:
            report_file_tab.write(
                f"----------------------------------------------------------------------------\nEntrada: {entry.get('entry_number')}, Código: {entry.get('atom_code')}, Lexeme: {entry.get('lexeme')}, QtdCharAntesTrunc: {entry.get('original_length')}, QtdCharDepoisTrunc: {entry.get('truncated_length')}, TipoSimb: {entry.get('symbol_type')}, Linha: {str(entry.get('lines'))}\n"
            )

    print(f"Relatório gerado com sucesso: {tab_reportfile_name}")
