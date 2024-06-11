class SymbolTable:
    def __init__(self):
        self.table = []
        self.indices = {}
    
    def add_symbol(self, code, lexeme, symbol_type, lines):
        if lexeme in self.indices:
            idx = self.indices[lexeme]
            self.table[idx]["lines"] += lines[:5 - len(self.table[idx]["lines"])]
        else:
            entry = {
                "entry_number": len(self.table) + 1,
                "atom_code": code, #Ex: C07
                "lexeme": lexeme[:30],  # Truncagem de lexeme para 30 caracteres
                "original_length": len(lexeme),
                "truncated_length": min(len(lexeme), 30),
                "symbol_type": symbol_type,
                "lines": lines[:5]  # Armazena apenas as 5 primeiras linhas onde o simbolo aparece
            }
            self.indices[lexeme] = len(self.table)
            self.table.append(entry)
    
    def __str__(self):
        return str(self.table)
