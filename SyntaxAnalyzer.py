from LexicalAnalyzer import *
# from main import tablesToString
#TODO remove else
class SyntaxAnalyzer:
    def __init__(self,t_lexemes,t_idns,t_constants):
        self.lexemes = t_lexemes
        self.idns = t_idns
        self.constants = t_constants
        self.i = 0
    def run(self):
        print(self.program())
    def lexeme(self,lexeme_code):
        return self.lexemes[self.i].code==lexeme_code
    def line(self):
        return self.lexemes[self.i].line
    def program(self):
        if self.spOg():
            if self.lexeme(13):
                self.i+=1
                if self.lexeme(15):
                    self.i+=1
                    if self.spOp():
                        if self.lexeme(14):
                            self.i+=1
                            return True
                        else:
                            raise SyntaxException("Нема закриваючої фігурної дужки",self.line())
                    else:
                        raise SyntaxException("Невірний список операторів",self.line())
            else:
                raise SyntaxException("Нема відкриваючої фігурної дужки",+self.line())
        else:
            raise SyntaxException("Невірний список оголошень",self.line())
    
    def spOg(self):
        if self.og():
            if self.lexeme(15):
                self.i+=1
                while not self.lexeme(13) and self.og():
                    if self.lexeme(15):
                        self.i+=1
                    else:
                        raise SyntaxException("Відсутній перенос на новий рядок",self.line())
                return True
            else:
                print(self.lexemes[self.i])
                raise SyntaxException("Відсутній перенос на новий рядок",self.line())
        else:
            raise SyntaxException("Відсутнє перше оголошення",self.line())
    
    def og(self):
        if self.type():
            if self.spZm():
                return True
            else:
                raise SyntaxException("Відсутній список змінних",self.line())
        else:
            raise SyntaxException("Відсутній тип",self.line())
    def spOp(self):#TODO refactor same code
        if self.op():
            if self.lexeme(15):
                self.i+=1
                while self.op():
                    if self.lexeme(15):
                        self.i+=1
                    else:
                        raise SyntaxException("Відсутній перенос на новий рядок",self.line())
                return True
            else:
                raise SyntaxException("Відсутній перенос на новий рядок",self.line())
        else:
            raise SyntaxException("Відсутній перший оператор",self.line())
    def type(self):
        if self.lexeme(1) or self.lexeme(2) or self.lexeme(12):
            self.i+=1
            return True
        else:
            raise SyntaxException("Невірний тип",self.line())
            
    def spZm(self):
        if self.idn():
            while self.lexeme(16):
                self.i+=1
                if not self.idn():
                    raise SyntaxException("Відсутній ідентифікатор",self.line())
            return True
        else:
            raise SyntaxException("Відсутній перший ідентифікатор",self.line())


    def op(self):
        if self.input() or self.output() or self.loop() or self.cond() or self.labelCall():
            return True
        elif self.idn():
            if self.lexeme(32):
                self.i+=1
                return True
            elif self.lexeme(17):
                self.i+=1
                if self.expr():
                    if  self.znakVidn():
                        if self.expr():
                            if self.lexeme(33):
                                self.i+=1
                                if self.expr():
                                    if self.lexeme(32):
                                        self.i+=1
                                        if self.expr():
                                            return True

                    if self.lexeme(15):
                        return True
                    else:
                        print("_+_+_+_+")
                else:
                    raise SyntaxException("Невірне присвоєння",self.line())
            else:
                raise SyntaxException("()()()()()",self.line())
        else:
            return False
            raise SyntaxException("Невірний оператор",self.line())
    
    def input(self):
        if self.lexeme(7):
            self.i+=1
            if self.lexeme(19):
                self.i+=1
                if self.idn():
                    while self.lexeme(19):
                        self.i+=1
                        if not self.idn():
                            raise SyntaxException("Відсутній ідентифікатор",self.line())
                    return True   
                else:
                    raise SyntaxException("Відсутній ідентифікатор",self.line())
            else:
                raise SyntaxException("Відсутній оператор >>",self.line())
        return False
        # чи треба else
    def output(self):
        if self.lexeme(8):
            self.i+=1
            if self.lexeme(18):
                self.i+=1
                if self.idn():
                    while self.lexeme(18):
                        self.i+=1
                        if self.lexeme(101):
                            self.i+=1
                        elif self.idn():
                            pass
                        # elif not self.idn():
                        else:
                            raise SyntaxException("Відсутній ідентифікатор або кфт",self.line())
                    return True   
                else:
                    raise SyntaxException("Відсутній ідентифікатор",self.line())
            else:
                raise SyntaxException("Відсутній оператор <<",self.line())
        return False
        # чи треба else
    def loop(self):
        if self.lexeme(3):
            self.i+=1
            if self.idn():
                if self.lexeme(17):
                    self.i+=1
                    if self.expr():
                        if self.lexeme(14):
                            self.i+=1
                            if self.expr():
                                if self.lexeme(9):
                                    self.i+=1
                                    if self.vidn():
                                        if self.lexeme(5):
                                            self.i+=1
                                            if self.op():
                                                return True
        #
        return False     
    def cond(self):
        if self.lexeme(6):
            self.i+=1
            if self.vidn():
                if self.lexeme(10):
                    self.i+=1
                    if self.labelCall():
                        return True
        return False
    def labelCall(self):
        if self.lexeme(11):
            self.i+=1
            if self.lexeme(102):
                self.i+=1
                return True
            else:
                raise SyntaxException("Відсутня мітка",self.line())                
        else:
            return False
    def vidn(self):
        if self.expr():
            if self.znakVidn():
                if self.expr():
                    return True
    def znakVidn(self):
        if self.lexeme(20) or self.lexeme(21) or  self.lexeme(22) or \
            self.lexeme(23) or self.lexeme(24) or self.lexeme(25):
            self.i+=1
            return True
        return False
    def expr(self):
        if self.t():
            while self.lexeme(26) or self.lexeme(27):
                self.i+=1
                if not self.t():
                    return False
            return True
    def t(self):
        if self.f():
            while self.lexeme(28) or self.lexeme(29):
                self.i+=1
                if not self.f():
                    return False
            return True
    def f(self):
        if self.idn():
            return True
        elif self.lexeme(101):
            self.i+=1
            return True
        elif self.lexeme(30):
            self.i+=1
            if self.expr():
                if self.lexeme(31):
                    self.i+=1
                    return True
        return False 
    def idn(self):
        if self.lexeme(100) or self.lexeme(102):
            self.i+=1
            return True
        return False
        raise SyntaxException("Невірний ідентифікатор",self.line())
        


if __name__ == "__main__":
    
    FILE_NAME  = 'source.txt'
    file = open(FILE_NAME,'r')
    input_text = file.read()
    file.close()
    lexer = LexicalAnalyzer(input_text)
    # (t_lexemes,t_idns,t_constants) = lexer.run()
    # text="".join(tablesToString(t_lexemes,t_idns,t_constants))
    # print(text)

    sAn = SyntaxAnalyzer(*lexer.run())
    sAn.run()
