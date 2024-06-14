class LexicalTable:
    def __init__(self):
        self.table = {}

    def add_atom(self, code, lexeme, line, symbol_table_index=None):
        line_str = str(line)
        
        entry = {
            "lexeme": lexeme,
            "code": code,
            "symbol_table_index": (symbol_table_index if symbol_table_index else "-"),
            "line": line_str,
        }
        if self.table.get(line_str) or self.table.get(line_str) == []:
            self.table[line_str].append(entry)
        else:
            self.table[line_str] = [entry]

    def __str__(self):
        return str(self.table)
