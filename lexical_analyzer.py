import re


class LexicalAnalyzer:
    def __init__(
        self, reserved_words_and_symbols, token_table, symbol_table, lexical_table
    ):
        self.reserved_words_and_symbols = reserved_words_and_symbols
        self.reserved_words_and_symbols_lower = {
            key.lower(): value for key, value in reserved_words_and_symbols.items()
        }
        self.token_table = token_table
        self.symbol_table = symbol_table
        self.lexical_table = lexical_table
        self.state = 0
        self.lexeme = ""
        self.current_line = 1
        self.token_patterns = {
            "consCadeia": re.compile(r'^"[a-zA-Z0-9 $._]*"$'),
            "consCaracter": re.compile(r"^'[a-zA-Z]'$"),
            "consInteiro": re.compile(r"^\d+$"),
            "consReal": re.compile(r"^\d+\.\d+([eE][-+]?\d+)?$"),
            "nomFuncao": re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$"),
            "nomPrograma": re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$"),
            "variavel": re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$"),
        }
        self.valid_characters = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_\"' \n/*.$%():,;?[]{}-*+/!=#<>="
        )

    def first_level_filter(self, char):
        return char if char in self.valid_characters else ""

    """
        This method analyzes each char in the provided text, count the current line and create tokens.
        It also controls the automate's states:
        - State 0 -> Initial state of the automate. Basically verifies all cases for the current char, like if it's a number or a reserved symbol of the lang.
                    Changes the state, finish the token, or continue to next char/line of the text
        - State 1 -> Identifier recognition (nomPrograma, variavel, nomFuncao)
        - State 2 -> Integer recognition (consInteiro)
        - State 3 -> String recognition enclosed in double quotes (consCadeia)
        - State 4 -> Single-quote character recognition (consCaracter)
        - State 5 -> Real Number Recognition (consReal)
        - State 6 -> State to validate exponential notation
    """

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
                elif (
                    i + 1 < len(text)
                    and char + text[i + 1] in self.reserved_words_and_symbols
                ):
                    self.lexical_table.add_atom(
                        self.reserved_words_and_symbols[char + text[i + 1]],
                        char + text[i + 1],
                        self.current_line,
                    )
                    i += 1  # Skip the next character
                elif char in self.reserved_words_and_symbols:
                    self.lexical_table.add_atom(
                        self.reserved_words_and_symbols[char], char, self.current_line
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
            # TODO: Review logis here. It's creating some random tokens on symbol table
            elif self.state == 4:
                self.lexeme += char
                if len(self.lexeme) > 3:
                    print(f"Invalid character constant: {self.lexeme}")
                    self.state = 0
                    self.lexeme = ""
                elif char == "'" and (len(self.lexeme) != 3):
                    print(f"Invalid character constant: {self.lexeme}")
                    self.state = 0
                    self.lexeme = ""
                elif char == "'" and len(self.lexeme) == 3:
                    self.finish_token()
            elif self.state == 5:
                if char.isdigit():
                    self.lexeme += char
                elif char == "E" and self.lexeme[-1] != ".":
                    self.lexeme += char
                    self.state = 6
                else:
                    self.finish_token()
                    if char == "\n":
                        self.current_line += 1
                    i -= 1  # Reprocess this character in initial state
            elif self.state == 6:
                if char.isdigit():
                    self.lexeme += char
                elif char == "+" and char not in self.lexeme and "-" not in self.lexeme:
                    self.lexeme += char
                elif char == "-" and char not in self.lexeme and "+" not in self.lexeme:
                    self.lexeme += char
                else:
                    self.finish_token()
                    if char == "\n":
                        self.current_line += 1

            i += 1

        if self.lexeme:
            self.finish_token()

    def finish_token(self):
        token_type = self.determine_type(self.lexeme)
        code = self.determine_code(self.lexeme)
        if code in self.reserved_words_and_symbols.values():
            self.lexical_table.add_atom(code, self.lexeme, self.current_line)
        elif code != 0:
            truncated_lexeme, code, token_type, original_length = self.perform_token_truncate(self.lexeme, code)
            
            symbol_entry = self.symbol_table.add_symbol(
                code, truncated_lexeme, original_length, token_type, [self.current_line]
            )
            self.lexical_table.add_atom(
                code, truncated_lexeme, self.current_line, symbol_entry.get("entry_number")
            )
        self.state = 0
        self.lexeme = ""

    def determine_code(self, token):
        lower_case_token = token.lower()
        if lower_case_token in self.reserved_words_and_symbols_lower:
            return self.reserved_words_and_symbols_lower[lower_case_token]
        for name, pattern in self.token_patterns.items():
            if pattern.fullmatch(token):
                if name in ["nomPrograma", "nomFuncao", "variavel"]:
                    return self.determine_specific_code(token)
                return self.token_table.get(name, 0)
        return 0  # Default code for unknown token

    def determine_specific_code(self, token):
        if self.is_nom_programa():
            return self.token_table["nomPrograma"]
        elif self.is_nom_funcao():
            return self.token_table["nomFuncao"]
        else:
            return self.token_table["variavel"]

    def is_nom_programa(self):
        last_token = self.get_last_token()
        if last_token and last_token["lexeme"].lower() == "programa":
            return True
        return False

    def is_nom_funcao(self):
        last_three_tokens = self.get_last_n_tokens(3)
        if (
            len(last_three_tokens) == 3
            and last_three_tokens[0]["lexeme"].lower() == "tipofunc"
            and last_three_tokens[1]["lexeme"].lower()
            in [
                "real",
                "inteiro",
                "cadeia",
                "logico",
                "caracter",
                "vazio",
            ]
            and last_three_tokens[2]["lexeme"] == ":"
        ):
            return True
        return False

    def get_last_token(self):
        lines = sorted(self.lexical_table.table.keys(), key=int)
        if not lines:
            return None
        last_line = lines[-1]
        return self.lexical_table.table[last_line][-1]

    def get_last_n_tokens(self, n):
        tokens = []
        lines = sorted(self.lexical_table.table.keys(), key=int, reverse=True)
        for line in lines:
            tokens.extend(reversed(self.lexical_table.table[line]))
            if len(tokens) >= n:
                break
        return list(reversed(tokens[-n:])) if len(tokens) >= n else []

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
                return name
        return "UNKNOWN"


    def perform_token_truncate(self, token, current_token_code):
        original_length = len(token)
        lexeme = token[:30]
        token_code = current_token_code

        if token_code == "C01":  # consCadeia
            if len(lexeme) == 30 and lexeme[-1] != '"':
                lexeme = lexeme[:29] + '"'
        elif token_code == "C04":  # consReal
            if lexeme[-1] == '.' or lexeme[-1] == 'e' or lexeme[-1] == '+' or lexeme[-1] == '-':
                lexeme = lexeme[:-1]
                token_code = self.token_table.get("consInteiro", 0)  # Ajustar para consInteiro

        # Chamar determine_type e determine_code novamente após truncagem
        token_type = self.determine_type(lexeme)
        token_code = self.determine_code(lexeme)

        return [lexeme, token_code, token_type, original_length]
        
        