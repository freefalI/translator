from LexicalAnalyzer import *
class SyntaxAnalyzer2:
    def __init__(self,t_lexemes,t_idns,t_constants):
        self.lexemes = t_lexemes
        self.idns = t_idns
        self.constants = t_constants
        self.i = 0
        self.stack = []
        self.cur_state = 1
        self.analysis_table=[]
        self.ERROR = 0
        self.EXIT = 1
        self.transition_table={
            1: {'label': (1, 2, 12), "state": 2, "nezr": self.ERROR, 'error_msg': "Відсутнє оголошення"},
            2: {'label': (100, 102), "state": 3, "nezr": self.ERROR, 'error_msg': "Невірний список змінних"},
            3: (
                {'label': 16, "state": 2, 'error_msg': "massag3"},
                {'label': 15, "state": 1, 'error_msg': "massage4"},
                {'label': 13, "state": 4, "nezr": self.ERROR,
                    'error_msg': "Немає відкриваючої фігурної дужки"}
            ),
            4: {'label': 15, "stack": 5, "state": 20, "nezr": self.ERROR, 'error_msg': "Відсутній перенос на новий рядок"},
            5: {'label': 15, "state": 6, "nezr": self.ERROR, 'error_msg': "Відсутній перенос на новий рядок"},
            6: (
                {'label': 14, "zr": self.EXIT},
                {"label": "any", "stack": 5, "state": 20}
            ),
            # Підавтомат вираз
            10: (
                {'label': (100, 101), "state": 11, 'error_msg': "massage10"},
                {'label': 30, "stack": 12, "state": 10, "nezr": self.ERROR,
                    'error_msg': "Відсутній ідентифікатор або кфт"}
            ),
            11: {'label': (26, 27, 28, 29), "state": 10, "nezr": self.EXIT},
            12: {'label': 31, "state": 11, "nezr": self.ERROR, 'error_msg': "Відсутня закриваюча дужка"},
            # Підавтомат Оператор
            20: (
                {'label': 6, "stack": 21, "state": 10, 'error_msg': "massage20"},
                {'label': (100, 102), "state": 25, 'error_msg': "massage201"},
                {'label': 7, "state": 30, 'error_msg': "massage202"},
                {'label': 8, "state": 33, 'error_msg': "massage203"},
                {'label': 3, "state": 36, 'error_msg': "massage204"},
                {'label': 11, "state": 43, "nezr": self.ERROR,
                    'error_msg': "Невірний оператор"},
            ),
            21: {'label': (20, 21, 22, 23, 24, 25), "stack": 22, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній знак відношення"},
            22: {'label': 10, "state": 23, "nezr": self.ERROR, 'error_msg': "Відсутній оператор then"},
            23: {'label': 11, "state": 24, "nezr": self.ERROR, 'error_msg': "Відсутній оператор goto"},
            24: {'label': 102, "zr": self.EXIT, "nezr": self.ERROR, 'error_msg': "Відсутній ідентифікатор"},
            25: (
                {'label': 32, "zr": self.EXIT, 'error_msg': "massage25"},
                {'label': 17, "stack": 26, "state": 10, "nezr": self.ERROR,
                    'error_msg': "Відсутнє присвоєння або оператор :"},
            ),
            26: {'label': (20, 21, 22, 23, 24, 25), "stack": 27, "state": 10, "nezr": self.EXIT, 'error_msg': "massage26"},
            27: {'label': 33, "stack": 28, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній оператор ?"},
            28: {'label': 32, "stack": 29, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній оператор :"},
            29: {},
            30: {'label': 19, "state": 31, "nezr": self.ERROR, 'error_msg': "Відсутній оператор >>"},
            31: {'label': 100, "state": 32, "nezr": self.ERROR, 'error_msg': "Відсутній ідентифікатор"},
            32: {'label': 19,  "state": 31, "nezr": self.EXIT, 'error_msg': "massage32"},
            33: {'label': 18, "state": 34, "nezr": self.ERROR, 'error_msg': "Відсутній оператор <<"},
            34: {'label': (100, 101), "state": 35, "nezr": self.ERROR, 'error_msg': "Відсутній ідентифікатор"},
            35: {'label': 18, "state": 34, "nezr": self.EXIT, 'error_msg': "massage35"},
            36: {'label': 100, "state": 37, "nezr": self.ERROR, 'error_msg': "Відсутній ідентифікатор"},
            37: {'label': 17, "stack": 38, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній оператор ="},
            38: {'label': 4, "stack": 39, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній оператор by"},
            39: {'label': 9, "stack": 40, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній оператор while"},
            40: {'label': (20, 21, 22, 23, 24, 25), "stack": 41, "state": 10, "nezr": self.ERROR, 'error_msg': "Відсутній знак відношення"},
            41: {'label': 5, "stack": 42, "state": 20, "nezr": self.ERROR, 'error_msg': "Відсутній оператор do"},
            42: {},
            43: {'label': 102, "zr": self.EXIT, "nezr": self.ERROR, 'error_msg': "Відсутній ідентифікатор(мітка)"}
        }

    def nextLexeme(self):
        lexeme = self.lexemes[self.i]
        self.i += 1
        return lexeme

    def line(self):
        return self.lexemes[self.i].line

    def run(self):
        while self.i < len(self.lexemes):
            lexeme = self.nextLexeme()
            # print(" state = {}, lexeme_code = {}, lexeme = {}, stack = {}".format(
            #             self.cur_state,lexeme.code,lexeme.name,self.stack))
            self.analysis_table.append([self.cur_state,self.stack[:]])
            self.processState(self.cur_state, lexeme.code)
        return self.analysis_table

    def processState(self, state, lexeme_code):
        transitions = self.transition_table[state]
        if not isinstance(transitions, tuple):
            transitions = (transitions,)
        for transition in transitions:
            if transition.get("label") == None:
                self.exit()
                return
            labels = transition['label']
            if labels == "any":
                self.i -= 1
                self.stack.append(transition['stack'])
                self.cur_state = transition['state']
                return
            if not isinstance(labels, tuple):
                labels = (labels,)
            for label in labels:
                if label == lexeme_code:
                    if transition.get("zr") != None:
                        if transition['zr'] == self.EXIT:
                            self.i += 1
                            self.exit()
                            return
                    if transition.get("stack") != None:
                        self.stack.append(transition['stack'])
                        self.cur_state = transition['state']
                        return
                    self.cur_state = transition['state']
                    return
            if transition.get("nezr") != None:
                if transition['nezr'] == self.EXIT:
                    self.exit()
                elif transition['nezr'] == self.ERROR:
                    # raise SyntaxException("{} \n state = {}, lexeme_code = {}, lexeme = {}, stack = {}".format(
                    #    transition['error_msg'], self.cur_state, lexeme_code, self.lexemes[self.i].name, self.stack,))
                    raise SyntaxException(
                        transition['error_msg'], self.line()-1)



    def exit(self):
        # print("EXIT")
        self.i-=1
        try:
            state = self.stack.pop()
            self.cur_state=state
        except IndexError as ex:
            pass

if __name__ == "__main__":
    
    FILE_NAME  = 'source.txt'
    file = open(FILE_NAME,'r')
    input_text = file.read()
    file.close()
    lexer = LexicalAnalyzer(input_text)
    # (t_lexemes,t_idns,t_constants) = lexer.run()
    # text="".join(tablesToString(t_lexemes,t_idns,t_constants))
    # print(text)

    sAn = SyntaxAnalyzer2(*lexer.run())
    print(sAn.run())
