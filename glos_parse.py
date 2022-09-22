from glos_scan import *

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

    def factor(self):
        if not self.curr: self.displayError("Error: Syntax error"); return
        # 1 + 2
        if self.curr.token == tok_num:
            self.add_instruction(self.curr)
            self.advance()
            return True
        elif self.curr.token == tok_sub:
            # Unary / Negate
            op = self.curr
            self.advance()
            self.factor()
            self.add_instruction(op)
            return True
        elif self.curr.token == tok_rbl:
            self.advance()
            self.grouping()
            return True
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
    
    def exp(self):
        success = self.term()
        if not success: return

        while self.curr and self.curr.token in (tok_add, tok_sub):
            op = self.curr
            self.advance()

            success = self.term()
            if not success: return

            self.add_instruction(op)
        
        return True
    
