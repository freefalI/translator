from LexicalAnalyzer import *
class SyntaxAnalyzer2:
    def __init__(self,t_lexemes,t_idns,t_constants):
        self.lexemes = t_lexemes
        self.idns = t_idns
        self.constants = t_constants
        # self.i = 0
        self.ERROR = 0
        self.EXIT = 1
        self.states_table=(
            {1: {'label': (1, 2, 3), "state": 2, "nezr": self.ERROR}},
            {2: {'label': 100, "state": 3, "nezr": self.ERROR}},
            {3: (
                {'label': 16, "state": 2},
                {'label': 15, "state": 1},
                {'label': 13, "state": 4, "nezr": self.ERROR}
            )},
            {4: {'label': 15, "stack": 5, "state": 20, "nezr": self.ERROR}},
            {5: {'label': 15, "state": 6, "nezr": self.ERROR}},
            {6: (
                {"stack": 5, "state": 20},
                {'label': 14, "zr": self.EXIT}
            )},
            # Підавтомат вираз
            {10: (
                {'label': (100, 101), "state": 11},
                {'label': 30, "stack": 12, "state": 10, "nezr": self.ERROR}
            )},
            {11: {'label': (26, 27, 28, 29), "state": 10, "nezr": self.EXIT}},
            {12: {'label': 31, "state": 11, "nezr": self.ERROR}},
            # Підавтомат Оператор
            {20: (
                {'label': 6, "stack": 21, "state": 10},
                {'label': 100, "state": 25},
                {'label': 7, "state": 29},
                {'label': 8, "state": 32},
                {'label': 3, "state": 35},
                {'label': 11, "state": 41, "nezr": self.ERROR},
            )},
            {21: {'label': (20, 21, 22, 23, 24, 25), "stack": 22, "state": 10, "nezr": self.ERROR}},
            {22: {'label': 10, "state": 23, "nezr": self.ERROR}},
            {23: {'label': 11, "state": 24, "nezr": self.ERROR}},
            {24: {'label': 102, "zr": self.EXIT, "nezr": self.ERROR}},
            {25: (
                {'label': 32, "zr": self.EXIT},
                {'label': 17, "stack": 26, "state": 10, "nezr": self.ERROR},
            )},
            {26: {'label': (20, 21, 22, 23, 24, 25), "stack": 27, "state": 10, "nezr": self.ERROR}},
            {27: {'label': 33, "stack": 28, "state": 10, "nezr": self.ERROR}},
            {28: {'label': 32, "stack": 0, "state": 10, "nezr": self.ERROR}},
            {29: {'label': 19, "state": 30, "nezr": self.ERROR}},
            {30: {'label': 100, "state": 31, "nezr": self.ERROR}},
            {31: {'label': 19,  "state": 30, "nezr": self.EXIT}},
            {32: {'label': 18, "state": 33, "nezr": self.ERROR}},
            {33: {'label': 100, "state": 34, "nezr": self.ERROR}},
            {34: {'label': 18, "state": 33, "nezr": self.EXIT}},
            {35: {'label': 100, "state": 36, "nezr": self.ERROR}},
            {36: {'label': 17, "stack": 37, "state": 10, "nezr": self.ERROR}},
            {37: {'label': 4, "stack": 38, "state": 10, "nezr": self.ERROR}},
            {38: {'label': 9, "stack": 39, "state": 10, "nezr": self.ERROR}},
            {39: {'label': (20, 21, 22, 23, 24, 25), "stack": 40, "state": 10, "nezr": self.ERROR}},
            {40: {'label': 5, "stack": 0, "state": 10, "nezr": self.ERROR}},
            {41: {'label': 101, "zr": self.EXIT, "nezr": self.ERROR}}
        )

    def run(self):
        
        
        
        
        return 0


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
