from glos_parse import *

class VM:
    
    def __init__(self, instructions, fileName):
        self.instructions = instructions
        self.file = fileName
        
        self.curr = None
        self.curr:Token
        self.count = -1

        self.stack = []

        self.advance()

    def advance(self):
        self.count += 1
        self.curr = self.count >= 0 and self.count < len(self.instructions) and self.instructions[self.count] or None

    def push(self, constant): self.stack = [constant] + self.stack

    def pop(self):
        a = self.stack[0]
        del self.stack[0]
        return a

    def execute(self):
        while self.curr:

            if self.curr.token == tok_num:
                self.push(self.curr.value)
                self.advance()

            elif self.curr.token in (tok_add, tok_sub, tok_div, tok_mul):
                b = self.pop()
                a = self.pop()
                if self.curr.token == tok_add:
                    self.push(a + b)
                elif self.curr.token == tok_sub:
                    self.push(a - b)
                elif self.curr.token == tok_mul:
                    self.push(a * b)
                elif self.curr.token == tok_div:
                    self.push(a / b)
                self.advance()

            
        return True
            
