from LexicalAnalyzer import *
from AscendingAnalysis import RelationTableMaker
import grammar
from itertools import chain 
from classes import Lexeme

# print(tableMaker.getRelationTable())
class SyntaxAnalyzer3:
    def __init__(self,t_lexemes,t_idns,t_constants,tableMaker):
        self.lexemes = t_lexemes
        self.idns = t_idns
        self.constants = t_constants
        self.i = 0
        # self.stack = []
        # self.cur_state = 1
        # self.analysis_table=[]
        # self.ERROR = 'error'
        # self.EXIT = 'exit'
        # self.relation_table=relation_table

        self.input_row = []
        self.stack = []
        self.TableMaker=tableMaker
        self.relation_table = tableMaker.getRelationTable()
        # print(self.TableMaker.all_elements_dict)


        # print(self.lexemes)
        # print(self.lexemes)
    def nextLexeme(self):
        lexeme = self.lexemes[self.i]
        self.i += 1
        return lexeme

    def line(self):
        return self.lexemes[self.i].line

    def run(self):
        self.lexemes.append(None)
        self.stack.append(None)
        it=0
        while True:
            print("NEW ITERATION",it,"\n   stack")
            print(*self.stack,sep="\n")
            it+=1
            current_lexeme = self.lexemes[0]
            print("  cur lexeme\t",current_lexeme)
            relation = self.TableMaker.relationBetween(self.stack[-1],
                                                    self.lexemes[0])
            print(relation)
            if relation==0:
                print(self.stack[-1], self.lexemes[0])
                raise SyntaxException("X")
            if relation in[1,2]:
                print("action1")
                self.stack.append(self.lexemes.pop(0))
            else:
                print("action2")
                # print(self.stack)
                base=[]

                el2=self.stack[-1]
                for i in range(len(self.stack)-2,-1,-1):
                    el1=self.stack[i]
                    try:
                        if el1.name:
                            print(el1.name)
                    except AttributeError:
                        print( el1)
                    relation = self.TableMaker.relationBetween(el1,el2)
                    relation_map=['','=','<','>']
                    print("    ", relation_map[relation])
                    if relation!=2:
                        base.insert(0,el2)
                    else:
                        base.insert(0,el2)
                        break
                    el2=el1
                print(self.stack[0])

                print("BASE=",base)
                base2=[]
                IDN_CODE = 100
                CON_CODE = 101
                LAB_CODE = 102
                for lexeme in base:
                    if isinstance(lexeme, Lexeme):
                        if lexeme.code==IDN_CODE:
                            i = base2.append("idn")
                        elif lexeme.code==CON_CODE:
                            i = base2.append("constant")
                        elif lexeme.code==LAB_CODE:
                            i = base2.append("lab")
                        elif lexeme.code==15:
                            i = base2.append("¶")
                        else:
                            i = base2.append(lexeme.name)

                    # except AttributeError:
                    else:
                        i = base2.append(lexeme)



                # base2 = tuple([i.name for i in base])
                base2 = tuple(base2)
                # for i in base:
                    # base2.append(i.name)
                print("BASE2=",base2)
                #find left part of rule in grammar
                answer=None
                find=False
                for nonterminal in self.TableMaker.grammar.keys():
                    right_part_of_rule = self.TableMaker.grammar[nonterminal]
                    if self.TableMaker.ruleHasAlternatives(right_part_of_rule):
                        # right_part_of_rule = list(chain.from_iterable(right_part_of_rule))
                        # right_part_of_rule = list(chain.from_iterable(right_part_of_rule))
                        for i in right_part_of_rule:
                            if i==base2:
                                answer = nonterminal
                                find=True
                                break
                    else:
                        if right_part_of_rule==base2:
                            answer = nonterminal
                            find=True
                            # break
                    if find:
                        break
                print("ANSWER=",answer)
                if base2==('<program>',):
                    print("successful compilation")
                    return True

                if answer==None:
                    raise SyntaxException("XXX")
                count=len(base2)
                for i in range(count):
                    self.stack.pop()
                self.stack.append(answer)
            print("\n\n")
        '''
        while self.i < len(self.lexemes):
            lexeme = self.nextLexeme()
            # print(" state = {}, lexeme_code = {}, lexeme = {}, stack = {}".format(
            #             self.cur_state,lexeme.code,lexeme.name,self.stack[:]))
            
            self.analysis_table.append([self.cur_state,self.stack[:]])
            self.processState(self.cur_state, lexeme.code)
        return self.analysis_table
        '''

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
    tableMaker = RelationTableMaker(grammar.grammar)
    # relation_table = tableMaker.getRelationTable()
    sAn = SyntaxAnalyzer3(*lexer.run(),tableMaker)
    # sAn.run()
    print(*sAn.run(),sep="\n")
