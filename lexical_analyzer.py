import re

class LexicalAnalyzer:
    def __init__(self, reserved_words_and_symbols, token_table, symbol_table, lexical_table):
        self.reserved_words_and_symbols = reserved_words_and_symbols
        self.reserved_words_and_symbols_lower = {key.lower(): value for key, value in reserved_words_and_symbols.items()}
        self.token_table = token_table
        self.symbol_table = symbol_table
        self.lexical_table = lexical_table
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
        self.valid_characters = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_\"' \n/*.$"
        )

    def first_level_filter(self, char):
        return char if char in self.valid_characters else ""

    def analyze(self, text):
        i = 0
        while i < len(text):
            char = text[i]
            char = self.first_level_filter(char)

            if not char:
                i += 1
                continue

            if isinstance(char, str):
                char = char.upper()

            if char == "\n":
                if self.lexeme:
                    self.finish_token()
                self.current_line += 1
            elif char == "/" and i + 1 < len(text) and text[i + 1] == "*":
                if self.lexeme:
                    self.finish_token()
                i += 2
                while i < len(text) - 1 and not (text[i] == "*" and text[i + 1] == "/"):
                    if text[i] == "\n":
                        self.current_line += 1
                    i += 1
                i += 1  # Skip the closing '/'
            elif char == "/" and i + 1 < len(text) and text[i + 1] == "/":
                if self.lexeme:
                    self.finish_token()
                i += 2
                while i < len(text) and text[i] != "\n":
                    i += 1
                i -= 1  # Let the newline character be processed in the main loop
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
                elif char.lower() in self.reserved_words_and_symbols_lower:
                    self.lexical_table.add_atom(
                        self.reserved_words_and_symbols_lower[char.lower()],
                        char,
                        self.current_line
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
        if code in self.reserved_words_and_symbols.values():
            self.lexical_table.add_atom(code, self.lexeme, self.current_line)
        else:
            symbol_entry = self.symbol_table.add_symbol(code, self.lexeme, token_type, [self.current_line])
            self.lexical_table.add_atom(code, self.lexeme, self.current_line, symbol_entry.get("entry_number"))
        self.state = 0
        self.lexeme = ""

    def determine_code(self, token):
        lower_case_token = token.lower()
        if lower_case_token in self.reserved_words_and_symbols_lower:
            return self.reserved_words_and_symbols_lower[lower_case_token]
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
                    return "CHC"
                elif name == "consInteiro":
                    return "INT"
                elif name == "consReal":
                    return "PFO"
                return name  # Default to the name if no specific type is needed
        return "UNKNOWN"  # Default type for unknown token
