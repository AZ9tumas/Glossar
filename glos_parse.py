from glos_scan import *

class Constant:
    def __init__(self, tok):
        self.token = tok.token
        self.isbool = tok.token == tok_idn and tok.value in ("true", "false")
        self.value = float(tok.value == "true") if self.isbool else tok.value

    def __repr__(self):
        if self.isbool: return "true" if self.value != 0 else "false"
        return str(self.value)
class Parse:
    def __init__(self, tokens, fileName):
        self.tokens = tokens
        self.file = fileName
        self.curr = None
        self.curr:Token
        self.count = -1
        self.instructions = []
        self.hasError = False

        self.advance()

    def add_instruction(self, instruction): self.instructions.append(instruction) # self.instructions = [instruction] + self.instructions

    def displayError(self, err):
        print(f"{err} in file '{self.file}' at line {self.tokens[self.count - 1].line}")
        self.hasError = True

    def advance(self):
        self.count += 1
        self.curr = self.count >= 0 and self.count < len(self.tokens) and self.tokens[self.count] or None

    def grouping(self):
        self.exp()
        if not self.curr or self.curr.token != tok_rbr:
            self.displayError("Error: Expected ')' to close '('")
        self.advance()

    def check_identifier(self):
        if not self.curr.token == tok_idn: return self.displayError(":(")
        
        # This function checks identifiers and keywords.
        if self.curr.value in ("true", "false"):
            self.add_instruction(Constant(self.curr))
        self.advance()

        return True

    def factor(self):
        if not self.curr: self.displayError("Error: Syntax error"); return
        # 1 + 2
        if self.curr.token == tok_num:
            self.add_instruction(Constant(self.curr))
            self.advance()
            return True
        elif self.curr.token == tok_sub:
            # Unary / Negate
            op = self.curr
            op.token = tok_negate
            self.advance()
            self.factor()
            self.add_instruction(op)
            return True
        elif self.curr.token == tok_rbl:
            self.advance()
            self.grouping()
            return True
        elif self.curr.token == tok_idn:
            return self.check_identifier()
        
        self.displayError("Error: Syntax error")
        return not self.hasError

    def term(self):
        success = self.factor()
        if not success: return

        while self.curr and self.curr.token in (tok_div, tok_mul):
            op = self.curr
            self.advance()

            success = self.factor()
            if not success: return

            self.add_instruction(op)
        return True
    
    def arth_exp(self):
        success = self.term()
        if not success: return

        while self.curr and self.curr.token in (tok_add, tok_sub):
            op = self.curr
            self.advance()

            success = self.term()
            if not success: return

            self.add_instruction(op)
        return True
    
    def comp_exp(self):
        success = self.arth_exp()
        if not success: return

        while self.curr and self.curr.token in (tok_greater, tok_lesser, tok_greater_eq, tok_lesser_eq, tok_eq):
            op = self.curr
            self.advance()

            success = self.arth_exp()
            if not success: return

            self.add_instruction(op)
        return True

    def exp(self):
        return self.comp_exp()
    
