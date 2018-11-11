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
                            raise SyntaxException("Немає закриваючої фігурної дужки",self.line())
                else:
                    raise SyntaxException("Відсутній список операторів",self.line())
            else:
                raise SyntaxException("Немає відкриваючої фігурної дужки",+self.line())
    
    def spOg(self):
        if self.og():
            if self.lexeme(15):
                self.i+=1
                while not self.lexeme(13) and self.og():
                    if self.lexeme(15):
                        self.i+=1
                    else:
                        raise SyntaxException("Відсутній перенос на новий рядок",self.line())
                if self.lexeme(13):
                    return True
                raise SyntaxException("Невірне оголошення",self.line())
            else:
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
            return False
   
    def type(self):
        if self.lexeme(1) or self.lexeme(2) or self.lexeme(12):
            self.i+=1
            return True
        return False
            
    def spZm(self):
        if self.idn():
            while self.lexeme(16):
                self.i+=1
                if not self.idn():
                    raise SyntaxException("Відсутній ідентифікатор",self.line())
            if self.lexeme(15):
                return True
            raise SyntaxException("Невірний список змінних",self.line())
        return False

    def spOp(self):#TODO refactor same code
        if self.op():
            if self.lexeme(15):
                self.i+=1
                while not self.lexeme(14) and self.op():
                    if self.lexeme(15):
                        self.i+=1
                    else:
                        raise SyntaxException("Відсутній перенос на новий рядок",self.line())
                if self.lexeme(14):
                    return True
                raise SyntaxException("Невірний оператор",self.line())
            else:
                raise SyntaxException("Відсутній перенос на новий рядок",self.line())
        else:
            raise SyntaxException("Відсутній перший оператор",self.line())
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
                    if self.znakVidn():
                        if self.expr():
                            if self.lexeme(33):
                                self.i+=1
                                if self.expr():
                                    if self.lexeme(32):
                                        self.i+=1
                                        if self.expr():
                                            return True
                                        else:
                                            raise SyntaxException("Відсутній вираз",self.line())
                                    else:
                                        raise SyntaxException("Відсутній оператор :",self.line())
                                else:
                                    raise SyntaxException("Відсутній вираз",self.line())
                            else:
                                raise SyntaxException("Відсутній оператор ?",self.line())
                        else:
                            raise SyntaxException("Відсутній вираз",self.line())
                    if self.lexeme(15):
                        return True
                    else:
                        raise SyntaxException("Невірне присвоєння",self.line())
                else:
                    raise SyntaxException("Відсутній вираз",self.line())
            else:
                raise SyntaxException("Відсутнє присвоєння або оператор :",self.line())
        return False

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
                    if self.lexeme(15):
                        return True 
                    raise SyntaxException("Невірний синтаксис оператора вводу. Очікується оператор >> або завершення оператора",self.line())
                else:
                    raise SyntaxException("Відсутній ідентифікатор",self.line())
            else:
                raise SyntaxException("Відсутній оператор >>",self.line())
        return False
    def output(self):
        if self.lexeme(8):
            self.i+=1
            if self.lexeme(18):
                self.i+=1
                if self.lexeme(101) or self.idn():
                    if self.lexeme(101):
                        self.i+=1
                    while self.lexeme(18):
                        self.i+=1
                        if self.lexeme(101):
                            self.i+=1
                        elif self.idn():
                            pass
                        else:
                            raise SyntaxException("Відсутній ідентифікатор або кфт",self.line())
                    if self.lexeme(15):
                        return True 
                    raise SyntaxException("Невірний синтаксис оператора виводу. Очікується оператор << або завершення оператора",self.line())
                else:
                    raise SyntaxException("Відсутній ідентифікатор або кфт",self.line())
            else:
                raise SyntaxException("Відсутній оператор <<",self.line())
        return False
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
                                            else:
                                                raise SyntaxException("Відсутній оператор",self.line())
                                        else:
                                            raise SyntaxException("Відсутній оператор do",self.line())
                                    else:
                                        raise SyntaxException("Відсутнє відношення",self.line())
                                else:
                                    raise SyntaxException("Відсутній оператор while",self.line())
                            else:
                                raise SyntaxException("Відсутній вираз",self.line())
                        else:
                            raise SyntaxException("Відсутній оператор by",self.line())
                    else:
                        raise SyntaxException("Відсутній вираз",self.line())
                else:
                    raise SyntaxException("Відсутній оператор =",self.line())
            else:
                raise SyntaxException("Відсутній ідентифікатор",self.line())
        return False     
    def cond(self):
        if self.lexeme(6):
            self.i+=1
            if self.vidn():
                if self.lexeme(10):
                    self.i+=1
                    if self.labelCall():
                        return True
                    else:
                        raise SyntaxException("Відсутній оператор goto",self.line())
                else:
                    raise SyntaxException("Відсутній оператор then",self.line())
        return False
    def labelCall(self):
        if self.lexeme(11):
            self.i+=1
            if self.lexeme(102):
                self.i+=1
                return True
            else:
                raise SyntaxException("Відсутня мітка",self.line())                
        return False
    def vidn(self):
        if self.expr():
            if self.znakVidn():
                if self.expr():
                    return True
                else:
                    raise SyntaxException("Відсутній вираз",self.line())
            else:
                raise SyntaxException("Відсутній знак відношення",self.line())
        raise SyntaxException("Відсутній вираз",self.line())
    def znakVidn(self):
        if self.lexeme(20) or self.lexeme(21) or  self.lexeme(22) or \
            self.lexeme(23) or self.lexeme(24) or self.lexeme(25):
            self.i+=1
            return True
        return False
    def expr(self):
        if self.term():
            while self.lexeme(26) or self.lexeme(27):
                self.i+=1
                if  self.term():
                    pass
                else:
                    raise SyntaxException("Відсутній term",self.line())
            return True
        return False
    def term(self):
        if self.factor():
            while self.lexeme(28) or self.lexeme(29):
                self.i+=1
                if self.factor():
                    pass
                else:
                    raise SyntaxException("Відсутній factor",self.line())
            return True
        return False
        
    def factor(self):
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
                else:
                    raise SyntaxException("Відсутня закриваюча дужка )",self.line())
            else:
                raise SyntaxException("Відсутній вираз",self.line())
        return False 
    def idn(self):
        if self.lexeme(100) or self.lexeme(102):
            self.i+=1
            return True
        return False
        


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
