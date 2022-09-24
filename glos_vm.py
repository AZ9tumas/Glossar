from glos_parse import *

class VM:
    
    def __init__(self, instructions, fileName):
        self.instructions = instructions
        self.file = fileName

        self.hasError = False
        
        self.curr = None
        self.curr:Token
        self.count = -1

        self.stack = []

        self.advance()

    def displayError(self, err):
        print(f"{err} in file '{self.file}' at line {self.instructions[self.count].line}")
        self.hasError = True

    def advance(self):
        self.count += 1
        self.curr = 0 <= self.count < len(self.instructions) and self.instructions[self.count] or None

    def push(self, constant): self.stack = [constant] + self.stack; #print(self.stack)

    def pop(self):
        if len(self.stack) <= 0: return None
        a = self.stack[0]
        del self.stack[0]
        #print(self.stack)
        return a

    def execute(self):
        while self.curr:

            if self.curr.token == tok_num:
                self.push(self.curr)
                self.advance()
            elif self.curr.token == tok_str:
                self.push(self.curr)
                self.advance()

            elif self.curr.token == tok_idn:
                # Variables will be added soon
                if self.curr.isbool: self.push(self.curr)

                self.advance()

            elif self.curr.token in (tok_add, tok_sub, tok_negate, tok_div, tok_mul, tok_greater, tok_lesser, tok_greater_eq, tok_lesser_eq, tok_eq):
                b_tok = self.pop()
                a_tok = self.pop()
                b = b_tok.value
                a = a_tok.value if a_tok else None

                final = None

                blacklist = {
                    tok_str: (tok_sub, tok_negate, tok_div)
                }

                tok = a_tok.token in blacklist and a_tok.token or b_tok.token in blacklist and b_tok.token or None
                if tok and self.curr.token in blacklist[tok]: return self.displayError(f"Error: Cannot pefrorm {self.curr.token} to {a_tok.token} and {b_tok.token}")

                if self.curr.token == tok_add:
                    final = a + b
                elif self.curr.token == tok_mul:
                    if isinstance(a, str) and isinstance(b, float): b = int(b)
                    elif isinstance(b, str) and isinstance(a, float): a = int(a)

                    final = a * b

                elif self.curr.token == tok_negate:
                    final = -b
                    if a: self.push(Constant(Token(tok_num, None, a)))
                    
                elif self.curr.token == tok_sub:
                    final = a - b
                elif self.curr.token == tok_div:
                    if b == 0: return self.displayError("Error: Division by zero")
                    final = a / b

                elif self.curr.token == tok_greater:
                    final = a > b
                elif self.curr.token == tok_lesser:
                    final = a < b
                elif self.curr.token == tok_greater_eq:
                    final = a >= b
                elif self.curr.token == tok_lesser_eq:
                    final = a <= b
                elif self.curr.token == tok_eq:
                    final = a == b

                self.advance()
                if str(final) == "True" or str(final) == "False":
                    self.push(Constant(Token(tok_idn, None, final and "true" or "false")))
                else: self.push(Constant(Token(tok_num, None, final)))

            
        return True
            
