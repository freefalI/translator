from LexicalAnalyzer import *
from tkinter import *
from tkinter.filedialog import askopenfilename

def tablesToString(t_lexemes,t_idns,t_constants): 
    lexeme_table = "---Lexemes\n"
    for lexeme in t_lexemes:
        lexeme_table +=str(lexeme)+"\n"
    idn_table = "---Idns\n"
    for idn in t_idns:
        idn_table +=str(idn)+"\n"
    constant_table = "---Constants\n"
    for constant in t_constants:
        constant_table +=str(constant)+"\n"
    return(lexeme_table,idn_table,constant_table)

def makeTables(t_lexemes,t_idns,t_constants):
    lexeme_pattern =  "{:^5}|{:^5}|{:<20}|{:<10}|{:<5}|\n"
    lexeme_table ="---Lexemes\n"+ lexeme_pattern.format("id","line","lexeme","code","fid")+"═"*50+"\n"
    for lexeme in t_lexemes:
        name = lexeme.name if lexeme.name!='\n' else '¶'
        fid = lexeme.fid if lexeme.fid else ''
        lexeme_table += lexeme_pattern.format(lexeme.id,lexeme.line,name,lexeme.code,fid)

    idn_pattern = "{:^5}|{:<20}|{:<10}|{:<5}|\n"
    idn_table = "\n---Idns\n" +idn_pattern.format("id","name","type","line")+"═"*44+"\n"
    for idn in t_idns:
        line = idn.line if idn.line else ''
        idn_table +=idn_pattern.format(idn.id,idn.name,idn.type,line)

    constant_pattern = "{:^5}|{:<10}|{:<10}|\n"
    constant_table = "\n---Constants\n"+ constant_pattern.format("id","name","type")+"═"*28+"\n"
    for constant in t_constants:
        constant_table += constant_pattern.format(constant.id,constant.name,constant.type)

    return(lexeme_table,idn_table,constant_table)
class Complier:
    def __init__(self,root,file_name):
        self.toolbar = Frame(root,bg ="#AAAAAA") 
        self.top_frame = Frame(root,bg="#FAC888") 
        self.bottom_frame = Frame(root,bg="#DDA343") 
        self.toolbar.pack(side =TOP,fill=X)
        self.top_frame.pack(fill="both",expand=False,padx=30,pady=30)#side =TOP)
        self.bottom_frame.pack(side =BOTTOM,fill="both",expand=True,padx=10,pady=10)
        #toolbar
        self.choose_file_button  = Button(self.toolbar,text="Choose file")
        self.compile_button  = Button(self.toolbar,text = "Compile")
        self.choose_file_button.grid(row = 0,column=0,padx=5,pady=5,ipadx=5,ipady=5)
        self.compile_button.grid(row=0,column=1,padx=5,pady=5,ipadx=5,ipady=5)

        self.text_area_top = Text(self.top_frame,font='Consolas 14',height=15,wrap=NONE)

        file = open(file_name,'r')
        text = file.read()
        file.close()
        self.text_area_top.insert(1.0,text)

        self.scrollbar_y_text_area_top = Scrollbar(self.top_frame)
        self.scrollbar_y_text_area_top.pack(side='right',fill=Y)
        self.scrollbar_y_text_area_top['command'] = self.text_area_top.yview
        self.text_area_top['yscrollcommand'] = self.scrollbar_y_text_area_top.set

        self.scrollbar_x_text_area_top = Scrollbar(self.top_frame,orient="horizontal")
        self.scrollbar_x_text_area_top.pack(side='bottom',fill=X)
        self.scrollbar_x_text_area_top['command'] = self.text_area_top.xview
        self.text_area_top['xscrollcommand'] = self.scrollbar_x_text_area_top.set
        self.text_area_top.pack(side=TOP,fill=BOTH)#fill=X,side=LEFT)

        self.text_area_bottom = Text(self.bottom_frame,font='Consolas 14',height=15,wrap=CHAR)
        self.scrollbar_y_text_area_bottom = Scrollbar(self.bottom_frame)
        self.scrollbar_y_text_area_bottom.pack(side='right',fill=Y)
        self.scrollbar_y_text_area_bottom['command'] = self.text_area_bottom.yview
        self.text_area_bottom['yscrollcommand'] = self.scrollbar_y_text_area_bottom.set
        self.text_area_bottom.pack(side=TOP,fill=BOTH)#fill=X,side=LEFT)

        #bind
        self.choose_file_button.bind("<1>",self.choose_file_handler)
        self.compile_button.bind("<1>",self.compile_handler)

    def choose_file_handler(self,event):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.text_area_bottom.delete('1.0', END) 
        self.text_area_bottom.insert(1.0,filename)
        # print(filename)
    def compile_handler(self,event):
        self.text_area_bottom.delete('1.0', END) 
        text = self.text_area_top.get('1.0', END)  
        lexer = LexicalAnalyzer(text)
        try:
            (t_lexemes,t_idns,t_constants) = lexer.run()
            # text2="".join(tablesToString(t_lexemes,t_idns,t_constants))
            text2="".join(makeTables(t_lexemes,t_idns,t_constants))
            self.text_area_bottom.insert(1.0,text2)
        except TranslatorException as ex:
            self.text_area_bottom.insert(1.0,ex.__class__.__name__+"\n"+str(ex))

FILE_NAME  = 'source.txt'
root = Tk()
gui = Complier(root,FILE_NAME)
root.state('zoomed')
root.mainloop()

