from symbol_table import SymbolTable
import re


class LexicalAnalyser:
    def __init__(self, reserved_words_and_symbols_table, token_table):
        self.reserved_words_and_symbols = reserved_words_and_symbols_table  # Pair of reserved words and symbols with their codes
        self.token_table = token_table  # Pair of token types with their codes
        self.symbol_table = SymbolTable()
        self.state = 0
        self.lexeme = ""
        self.current_line = 1
        self.token_patterns = {
            "consCadeia": re.compile(r'^".*"$'),
            "consCaracter": re.compile(r"^'.'$"),
            "consInteiro": re.compile(r"^\d+$"),
            "consReal": re.compile(r"^\d+\.\d+([eE][-+]?\d+)?$"),
            "nomFuncao": re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$"),
            "nomPrograma": re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$"),
            "variavel": re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$"),
        }

    def analyze(self, text):
        i = 0
        while i < len(text):
            char = text[i]

            # Convert to uppercase to make analysis case insensitive and save lexeme in uppercase
            if isinstance(char, str):
                char = char.upper()

            # In case of line break, always finish the token before incrementing the current line
            if char == "\n":
                if self.lexeme:
                    self.finish_token()
                self.current_line += 1
            elif self.state == 0:
                if char.isalpha():
                    self.state = 1
                    self.lexeme += char
                elif char.isdigit():
                    self.state = 2
                    self.lexeme += char
                elif char == '"':
                    self.state = 3
                    self.lexeme += char
                elif char == "'":
                    self.state = 4
                    self.lexeme += char
                elif char in self.reserved_words_and_symbols:
                    self.symbol_table.add_symbol(
                        self.reserved_words_and_symbols[char],
                        char,
                        "SYMBOL",
                        [self.current_line],
                    )
                elif char.isspace():
                    if char == "\n":
                        if self.lexeme:
                            self.finish_token()
                        self.current_line += 1
                else:
                    print(f"Unexpected character: {char}")
            elif self.state == 1:
                if char.isalnum() or char == "_":
                    self.lexeme += char
                else:
                    self.finish_token()
                    if char == "\n":
                        self.current_line += 1
                    i -= 1  # Reprocess this character in initial state
            elif self.state == 2:
                if char.isdigit():
                    self.lexeme += char
                elif char == ".":
                    self.state = 5
                    self.lexeme += char
                else:
                    self.finish_token()
                    if char == "\n":
                        self.current_line += 1
                    i -= 1  # Reprocess this character in initial state
            elif self.state == 3:
                self.lexeme += char
                if char == '"':
                    self.finish_token()
            elif self.state == 4:
                self.lexeme += char
                if char == "'":
                    self.finish_token()
            elif self.state == 5:
                if char.isdigit():
                    self.lexeme += char
                else:
                    self.finish_token()
                    if char == "\n":
                        self.current_line += 1
                    i -= 1  # Reprocess this character in initial state

            i += 1

        # Finalize last token if necessary
        if self.lexeme:
            self.finish_token()

    def finish_token(self):
        token_type = self.determine_type(self.lexeme)
        code = self.determine_code(self.lexeme)
        self.symbol_table.add_symbol(code, self.lexeme, token_type, [self.current_line])
        self.state = 0
        self.lexeme = ""

    def determine_code(self, token):
        for name, pattern in self.token_patterns.items():
            if pattern.fullmatch(token):
                return self.token_table.get(name, 0)
        return 0  # Default code for unknown token

    def determine_type(self, token):
        for name, pattern in self.token_patterns.items():
            if pattern.fullmatch(token):
                if name in ["variavel", "nomPrograma", "nomFuncao"]:
                    return "VOI"
                elif name == "consCadeia":
                    return "STR"
                elif name == "consCaracter":
                    return "CHR"
                elif name == "consInteiro":
                    return "INT"
                elif name == "consReal":
                    return "PFO"
                return name  # Default to the name if no specific type is needed
        return "UNKNOWN"  # Default type for unknown token

    # def determine_type(self, token):
    #     for name, pattern in self.token_patterns.items():
    #         if pattern.fullmatch(token):
    #             return name  # Return the name as the type for simplicity
    #     return "UNKNOWN"  # Default type for unknown token
