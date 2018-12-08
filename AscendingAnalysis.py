import numpy as np
np.set_printoptions(threshold=np.inf)
import grammar
class RelationTableMaker:
    def __init__(self,grammar):
        self.grammar = grammar
        self.terminals = []
        self.nonterminals=[]
        self.relationMatrix = None
        self.trn_and_nontrn_table=None
        self.equals_indexes=[]
        self.number_of_nonterminals=None
        self.conflicts=[]
        self.conflicts2={}
        self.process()
    def ruleHasAlternatives(self,array):
        for i in array:
            if isinstance(i,tuple):
                return True
        return False

    def addTrnOrNonTrn(self,element):
        if  self.isTerminal(element):
            if element not in self.terminals:
                self.terminals.append(element)
        else:
            if element not in self.nonterminals:
                self.nonterminals.append(element)

    def fillTrnsAndNonTrns(self):
        for nonterminal in self.grammar.keys():
            self.nonterminals.append('<'+nonterminal+'>')

        for nonterminal in self.grammar.keys():
            if '<'+nonterminal+'>' not in self.nonterminals:
                self.nonterminals.append('<'+nonterminal+'>')
            rule = self.grammar[nonterminal]
            if self.ruleHasAlternatives(rule):
                for variant in rule:
                    for element in variant:
                        self.addTrnOrNonTrn(element)
            else:
                for element in rule:
                    self.addTrnOrNonTrn(element)
    
    def buildRelationEquals(self):
        for nonterminal in self.grammar.keys():
            rule = self.grammar[nonterminal]
            if self.ruleHasAlternatives(rule):
                for variant in rule:
                    for index,element in enumerate(variant[:-1]):
                        i = self.trn_and_nontrn_table[element]
                        j = self.trn_and_nontrn_table[variant[index+1]]
                        self.relationMatrix[i][j] = 1
                        self.equals_indexes.append((i,j,element,variant[index+1]))
                        # print(i,j,element,variant[index+1])
            else:
                for index,element in enumerate(rule[:-1]):
                    i = self.trn_and_nontrn_table[element]
                    j = self.trn_and_nontrn_table[rule[index+1]]
                    self.relationMatrix[i][j] = 1
                    self.equals_indexes.append((i,j,element,rule[index+1]))
                    # print(i,j,element,rule[index+1])
    def isTerminal(self,trn_or_nontrn):
        return not  (trn_or_nontrn[0]=='<' and trn_or_nontrn[-1]=='>')
    def isNonTerminal(self,trn_or_nontrn):
        return not  self.isTerminal(trn_or_nontrn)
    def _first_plus_recursion(self,trn_or_nontrn,array):
        rule = self.grammar[trn_or_nontrn[1:-1]]
        if self.ruleHasAlternatives(rule):
            for variant in rule:
                if  self.isNonTerminal(variant[0]):
                    if variant[0] not in array:
                        array.append(variant[0])
                        self._first_plus_recursion(variant[0],array)
                else:
                    if variant[0] not in array:
                        array.append(variant[0])
        else:
            if  self.isNonTerminal(rule[0]):
                if rule[0] not in array:
                    array.append(rule[0])
                    self._first_plus_recursion(rule[0],array)
            else:
                if rule[0] not in array:
                    array.append(rule[0])

    def firstPlus(self,trn_or_nontrn):
        array = []
        self._first_plus_recursion(trn_or_nontrn,array)
        return array

    def _last_plus_recursion(self,trn_or_nontrn,array):
        rule = self.grammar[trn_or_nontrn[1:-1]]
        if self.ruleHasAlternatives(rule):
            for variant in rule:
                if  self.isNonTerminal(variant[-1]):
                    if variant[-1] not in array:
                        array.append(variant[-1])
                        self._first_plus_recursion(variant[-1],array)
                else:
                    if variant[-1] not in array:
                        array.append(variant[-1])
        else:
            if  self.isNonTerminal(rule[-1]):
                if rule[-1] not in array:
                    array.append(rule[-1])
                    self._last_plus_recursion(rule[-1],array)
            else:
                if rule[-1] not in array:
                    array.append(rule[-1])

    def lastPlus(self,trn_or_nontrn):
        array = []
        self._last_plus_recursion(trn_or_nontrn,array)
        return array

    def buildRelationLess(self):
        left_half_of_table = [i for i in self.equals_indexes if i[1]<=self.number_of_nonterminals-1]
        for (i,j,trn1,trn2) in left_half_of_table:
            # print (i,j,trn1,trn2)
            first_plus = self.firstPlus(trn2)
            # print(first_plus)
            for element in first_plus:
                j = self.trn_and_nontrn_table[element]
                if self.relationMatrix[i][j]==0 or self.relationMatrix[i][j]==2:
                    self.relationMatrix[i][j] = 2
                    # print(i,j,element)
                else:
                    # self.conflicts.append((i,j,trn1,element,self.relationMatrix[i][j],2,'<'))
                    self.conflicts2.update({(i,j):['=','<']})
                    # self.conflicts.update({(trn1,j): [i,j,element,first_plus[index+1],self.relationMatrix[i][j],2]})

    def buildRelationGreater(self):
        top_half_of_table = [i for i in self.equals_indexes if i[0]<=self.number_of_nonterminals-1]
        for (i,j,trn1,trn2) in top_half_of_table:
            # print (i,j,trn1,trn2)
            last_plus = self.lastPlus(trn1)
            # print(last_plus)
            for element in last_plus:
                i = self.trn_and_nontrn_table[element]
                if self.relationMatrix[i][j]==0 or self.relationMatrix[i][j]==3:
                    self.relationMatrix[i][j] = 3
                    # print(i,j,element)
                else:
                    self.conflicts.append((i,j,element,trn2,self.relationMatrix[i][j],3,'>'))
                    if self.conflicts2.get((i,j)):
                        self.conflicts2[(i,j)].append('>')
                    else:
                        self.conflicts2.update({(i,j):['=','>']})
            #3.2            
            if self.isNonTerminal(trn2):     
                first_plus = self.firstPlus(trn2)
                for element in first_plus:
                    j = self.trn_and_nontrn_table[element]
                    if self.relationMatrix[i][j]==0 or self.relationMatrix[i][j]==3:
                        self.relationMatrix[i][j] = 3
                        # print(i,j,element)
                    else:
                        self.conflicts.append((i,j,element,trn2,self.relationMatrix[i][j],3,'>'))
                        if self.conflicts2.get((i,j)):
                            self.conflicts2[(i,j)].append('>')
                        else:
                            self.conflicts2.update({(i,j):['=','>']})


    def process(self):#add this code to __init__
        self.fillTrnsAndNonTrns()
        matrix_size = len(self.terminals)+len(self.nonterminals)
        self.relationMatrix = np.zeros((matrix_size,matrix_size),np.int8) 
        list_ = self.nonterminals + self.terminals
        self.number_of_nonterminals=len(self.nonterminals)
        self.trn_and_nontrn_table = {value:index for index,value in enumerate(list_)}
        self.buildRelationEquals()
        # print(self.equals_indexes)
        self.buildRelationLess()
        self.buildRelationGreater()

        print(self.trn_and_nontrn_table)
        # print(matrix_size)
        # print (self.nonterminals)
        # print (self.terminals)
        # print(list_)
        # print(self.relationMatrix)
        np.savetxt("relationTable",self.relationMatrix,fmt='%.d')
        # print("\n",*self.conflicts,sep='\n')
        # print(len(self.conflicts))
        print("\n",*self.conflicts2.keys(),*self.conflicts2.values(),sep='\n')
        print(len(self.conflicts2))


tableMaker = RelationTableMaker(grammar.grammar)


#TODO
'''
'''