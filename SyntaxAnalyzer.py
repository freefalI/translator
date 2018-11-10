from LexicalAnalyzer import *
from main import tablesToString

class SyntaxAnalyzer:
    pass
FILE_NAME  = 'source.txt'
file = open(FILE_NAME,'r')
input_text = file.read()
file.close()
# print(input_text)
lexer = LexicalAnalyzer(input_text)
(t_lexemes,t_idns,t_constants) = lexer.run()
text="".join(tablesToString(t_lexemes,t_idns,t_constants))
print(text)