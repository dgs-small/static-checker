class SymbolTable:
    def __init__(self):
        self.table = []
        self.indices = {}
    
    def add_symbol(self, code, lexeme, original_length, symbol_type, lines):
        if lexeme in self.indices:
            idx = self.indices[lexeme]
            self.table[idx]["lines"] += lines[:5 - len(self.table[idx]["lines"])]
        else:
            entry = {
                "entry_number": len(self.table) + 1,
                "atom_code": code, #Ex: C07
                "lexeme": lexeme,
                "original_length": original_length,
                "truncated_length": len(lexeme),
                "symbol_type": symbol_type,
                "lines": lines[:5]  # Armazena apenas as 5 primeiras linhas onde o simbolo aparece
            }
            self.indices[lexeme] = len(self.table)
            self.table.append(entry)
        
        idx = self.indices[lexeme]
        
        return self.table[idx]
    
    def __str__(self):
        return str(self.table)
