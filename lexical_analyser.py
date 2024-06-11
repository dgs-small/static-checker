from utils import reserved_words_and_symbols
from symbol_table import SymbolTable

import re

class LexicalAnalyser:
    def __init__(self):
        self.reserved_words_and_symbols = reserved_words_and_symbols()
        self.symbol_table = SymbolTable()
        self.identifier_patterns = {
            "consCadeia": r"\".*?\"",
            "consCaracter": r"'.'",
            "consInteiro": r"\d+",
            "consReal": r"\d+\.\d+([eE][-+]?\d+)?",
            "nomFuncao": r"[a-zA-Z][a-zA-Z0-9]*",
            "nomPrograma": r"[a-zA-Z][a-zA-Z0-9]*",
            "variavel": r"[a-zA-Z_][a-zA-Z0-9_]*"
        }
    
    def lexical_scan(self, character, position):
        pass
    
    def lexical_analysis(self, character, symbol_table):
        pass