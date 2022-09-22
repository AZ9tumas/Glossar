import string

chars = string.ascii_letters

# Tokens
tok_add = "add"
tok_sub = "sub"
tok_mul = "mul"
tok_div = "div"
tok_num = "num"
tok_str = "str"
tok_idn = "identifier"
tok_assign = "assign"
tok_comma = "comma"
tok_semi= "semi colon"
tok_colon = "colon"
tok_dot = 'dot'
tok_bang = 'bang'

# Braces
tok_rbr = 'round right'
tok_rbl = 'round left'

tok_sbr = 'square right'
tok_sbl = 'square left'

tok_cbr = 'curly right'
tok_cbl = 'curly left'

# Constants

numbers = "0123456789"

class Token:
    def __init__(self, tok, line, val = None):
        self.token = tok
        self.value = val
        self.line = line

    def __repr__(self):
        val = self.value
        if self.token == tok_str: val = f"'{self.value or ''}'"
        return val and f"{self.token} : {val}" or self.token
        

class Scanner:
    def __init__(self, code, fileName, line):
        self.code = code
        self.curr = None
        self.count = -1
        self.tokens = []
        self.file = fileName
        self.line = line

        self.advance()

    def advance(self):
        self.count += 1
        self.curr = self.count >= 0 and self.count < len(self.code) and self.code[self.count] or None

    def scan(self):
        while self.curr:
            if self.curr in " \t\n": self.advance()
            #elif self.curr in '+-/*:.=;,!(){}[]': self.tokens.append(Token(self.curr)); self.advance()
            elif self.curr == '+': self.tokens.append(Token(tok_add, self.line)); self.advance()
            elif self.curr == '-': self.tokens.append(Token(tok_sub, self.line)); self.advance()
            elif self.curr == '/': self.tokens.append(Token(tok_div, self.line)); self.advance()
            elif self.curr == '*': self.tokens.append(Token(tok_mul, self.line)); self.advance()
            elif self.curr == ':': self.tokens.append(Token(tok_colon, self.line)); self.advance()
            elif self.curr == '.': self.tokens.append(Token(tok_dot, self.line)); self.advance()
            elif self.curr == '=': self.tokens.append(Token(tok_assign, self.line)); self.advance()
            elif self.curr == ';': self.tokens.append(Token(tok_semi, self.line)); self.advance()
            elif self.curr == ',': self.tokens.append(Token(tok_comma, self.line)); self.advance()
            elif self.curr == '!': self.tokens.append(Token(tok_bang, self.line)); self.advance()

            # Braces

            elif self.curr == '(': self.tokens.append(Token(tok_rbl, self.line)); self.advance()
            elif self.curr == ')': self.tokens.append(Token(tok_rbr, self.line)); self.advance()

            elif self.curr == '[': self.tokens.append(Token(tok_sbl, self.line)); self.advance()
            elif self.curr == ']': self.tokens.append(Token(tok_sbr, self.line)); self.advance()

            elif self.curr == '{': self.tokens.append(Token(tok_cbl, self.line)); self.advance()
            elif self.curr == '}': self.tokens.append(Token(tok_cbr, self.line)); self.advance()

            elif self.curr in numbers: self.tokens.append(self.number())
            
            elif self.curr in "'\"": 
                tkn = self.make_str()
                if not tkn: return False
                self.tokens.append(tkn)

            elif self.curr in chars: self.tokens.append(self.identifier())
            else: print(f"Error: Unknown Character '{self.curr}' in file '{self.file}' at line {self.line}"); return False

        return True

    def identifier(self):
        iden = ''

        while self.curr and self.curr in "_"+chars:
            iden += self.curr
            self.advance()
        
        return Token(tok_idn, self.line, iden)

    def make_str(self):
        start_quote = self.curr
        self.advance() # After the quote

        given_str = ""

        while self.curr and self.curr != start_quote:
            given_str += self.curr
            self.advance()

        if self.curr != start_quote: print("Error: Unterminated String")
        else: self.advance()

        return Token(tok_str, self.line, given_str)

    def number(self):
        num_str = ""

        while self.curr and self.curr in '.'+numbers:
            if '.' in num_str and self.curr == '.': break
            num_str += self.curr
            self.advance()

        return Token(tok_num, self.line, float(num_str))

    def printTokens(self): print(*self.tokens, sep=', ')
