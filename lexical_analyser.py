from utils import reserved_words_and_symbols_table, token_table
from symbol_table import SymbolTable

import re

class LexicalAnalyser:
    def __init__(self):
        self.reserved_words_and_symbols = reserved_words_and_symbols_table() # Par chave e valor com atomo e codigo de palavras e simbolos reservados
        self.token_table = token_table() # Par chave e valor com atomo e codigo de cada tipo de identificador
        self.symbol_table = SymbolTable()
        self.token_patterns = {
            "consCadeia": r"\".*?\"",
            "consCaracter": r"'.'",
            "consInteiro": r"\d+",
            "consReal": r"\d+\.\d+([eE][-+]?\d+)?",
            "nomFuncao": r"[a-zA-Z][a-zA-Z0-9]*",
            "nomPrograma": r"[a-zA-Z][a-zA-Z0-9]*",
            "variavel": r"[a-zA-Z_][a-zA-Z0-9_]*"
        }
