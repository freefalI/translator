from LexicalAnalyzer import *
from SyntaxAnalyzer import *
from SyntaxAnalyzer2 import *
from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename

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
    lexeme_pattern =  "{:^5}|{:^5}|{:<20}|{:<10}|{:^10}|{:^10}|{:^10}|\n"
    lexeme_table ="---Lexemes\n"+ lexeme_pattern.format("id","line","lexeme","code","idn code","con code","label code")+"═"*77+"\n"
    for lexeme in t_lexemes:
        name = lexeme.name if lexeme.name!='\n' else '¶'
        f1=f2=f3=""
        if lexeme.code==LexicalAnalyzer.IDN_CODE:
            f1 = lexeme.fid
        if lexeme.code==LexicalAnalyzer.CON_CODE:
            f2 = lexeme.fid
        if lexeme.code==LexicalAnalyzer.LAB_CODE:
            f3 = lexeme.fid
        lexeme_table += lexeme_pattern.format(lexeme.id,lexeme.line,name,lexeme.code,f1,f2,f3)

    idn_pattern = "{:^5}|{:<20}|{:<10}|{:^5}|\n"
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
        self.top_frame = Frame(root,bg="#AACAAA") 
        self.bottom_frame = Frame(root,bg="#AADADA") 
        self.toolbar.pack(side =TOP,fill=X)
        self.top_frame.pack(fill="both",expand=False,padx=30,pady=30)#side =TOP)
        self.bottom_frame.pack(side =BOTTOM,fill="both",expand=True,padx=10,pady=10)
        #toolbar
        self.open_file_button  = Button(self.toolbar,text="Open file")
        self.compile_button  = Button(self.toolbar,text = "Analyse")
        self.save_button  = Button(self.toolbar,text = "Save to file")
        self.open_file_button.grid(row = 0,column=0,padx=5,pady=5,ipadx=5,ipady=5)
        self.compile_button.grid(row=0,column=2,padx=5,pady=5,ipadx=5,ipady=5)
        self.save_button.grid(row=0,column=1,padx=5,pady=5,ipadx=5,ipady=5)

        self.text_area_top = Text(self.top_frame,font='Consolas 14',height=15,wrap=NONE)
        # self.text_area_line_numbers = Text(self.top_frame,font='Consolas 14',width=2,height=15,wrap=NONE)

        file = open(file_name,'r')
        text = file.readlines()
        # num_lines = sum(1 for line in text)
        # print(file.readlines())
        # num_lines = sum(1 for i in file.readlines())
        file.close()
        self.text_area_top.insert(1.0,"".join(text))
        # line_numbers = "\n".join(str(i) for i in range(1,num_lines+1))
        # print(line_numbers)
        # self.text_area_line_numbers.insert(1.0,line_numbers)

        self.scrollbar_y_text_area_top = Scrollbar(self.top_frame)
        self.scrollbar_y_text_area_top.pack(side='right',fill=Y)
        self.scrollbar_y_text_area_top['command'] = self.text_area_top.yview
        # self.scrollbar_y_text_area_top['command'] = self.on_top_scrollbar
        # self.text_area_top['yscrollcommand'] = self.on_textscroll
        self.text_area_top['yscrollcommand'] = self.scrollbar_y_text_area_top.set

        # self.scrollbar_y_text_area_top['command'] = self.text_area_line_numbers.yview
        # self.text_area_line_numbers['yscrollcommand'] = self.on_textscroll
        # self.text_area_line_numbers['yscrollcommand'] = self.scrollbar_y_text_area_top.set


        self.scrollbar_x_text_area_top = Scrollbar(self.top_frame,orient="horizontal")
        self.scrollbar_x_text_area_top.pack(side='bottom',fill=X)
        self.scrollbar_x_text_area_top['command'] = self.text_area_top.xview
        self.text_area_top['xscrollcommand'] = self.scrollbar_x_text_area_top.set
        # self.text_area_line_numbers.pack(side=LEFT,fill=BOTH)#fill=X,side=LEFT)
        # self.text_area_line_numbers.config(state=DISABLED)
        # text_area_bottom.config(state=DISABLED)
        self.text_area_top.pack(side=TOP,fill=BOTH)#fill=X,side=LEFT)


        self.text_area_bottom = Text(self.bottom_frame,font='Consolas 14',height=15,wrap=CHAR)
        self.scrollbar_y_text_area_bottom = Scrollbar(self.bottom_frame)
        self.scrollbar_y_text_area_bottom.pack(side='right',fill=Y)
        self.scrollbar_y_text_area_bottom['command'] = self.text_area_bottom.yview
        self.text_area_bottom['yscrollcommand'] = self.scrollbar_y_text_area_bottom.set
        self.text_area_bottom.pack(side=TOP,fill=BOTH)#fill=X,side=LEFT)

        #bind
        self.open_file_button.bind("<1>",self.open_file_handler)
        self.compile_button.bind("<1>",self.compile_handler)
        self.save_button.bind("<1>",self.save_handler)

        self.text_area_bottom.config(state=DISABLED)

        # self.text_area_top.bind("<Any-KeyPress>",self.update_line_numbers)
        
    # def update_line_numbers(self,event):
    #     line,_ = self.text_area_top.index('end').split('.')
    #     line = int(line)
    #     print(line)
    #     line_numbers = "\n".join(str(i) for i in range(1,line))
    #     self.text_area_line_numbers.config(state=NORMAL)
    #     self.text_area_line_numbers.delete('1.0', END)             
    #     self.text_area_line_numbers.insert(1.0,line_numbers)
    #     self.text_area_line_numbers.config(state=DISABLED)




    # def on_top_scrollbar(self, *args):
    #     '''Scrolls both text widgets when the scrollbar is moved'''
    #     self.text_area_line_numbers.yview(*args)
    #     self.text_area_top.yview(*args)

    # def on_textscroll(self, *args):
    #     '''Moves the scrollbar and scrolls text widgets when the mousewheel
    #     is moved on a text widget'''
    #     self.scrollbar_y_text_area_top.set(*args)
    #     self.on_top_scrollbar('moveto', args[0])

    def edit_bottom_textarea(method_to_decorate):
        def wrapper(*args, **kwargs):
            args[0].text_area_bottom.config(state=NORMAL)
            # try:
            method_to_decorate(*args, **kwargs)
            # except Exception as ex:
                # print(ex)
            args[0].text_area_bottom.config(state=DISABLED)
        return wrapper
    
    @edit_bottom_textarea
    def open_file_handler(self,event):
        filename = askopenfilename(filetypes = (("txt files","*.txt"),("all files","*.*"))) 
        try:
            file = open(filename,'r')
            text = file.readlines()
            # num_lines = sum(1 for line in text)
            file.close()

            # line_numbers = "\n".join(str(i) for i in range(1,num_lines+1))
            
            # self.text_area_line_numbers.config(state=NORMAL)
            # self.text_area_line_numbers.delete('1.0', END)             
            # self.text_area_line_numbers.insert(1.0,line_numbers)
            # self.text_area_line_numbers.config(state=DISABLED)

            self.text_area_top.delete('1.0', END) 
            self.text_area_top.insert(1.0,"".join(text))
        except UnicodeDecodeError as ex:
            self.text_area_bottom.delete('1.0', END) 
            self.text_area_bottom.insert(1.0,"Wrong file format!")

    @edit_bottom_textarea
    def compile_handler(self,event):
        self.text_area_bottom.delete('1.0', END) 
        text = self.text_area_top.get('1.0', END)  
        lexer = LexicalAnalyzer(text)
        try:
            (t_lexemes,t_idns,t_constants) = lexer.run()
            sAn = SyntaxAnalyzer2(t_lexemes,t_idns,t_constants)
            sAn.run()
            # text2="".join(tablesToString(t_lexemes,t_idns,t_constants))
            text2="".join(makeTables(t_lexemes,t_idns,t_constants))
            self.text_area_bottom.insert(1.0,text2)
        except TranslatorException as ex:
            self.text_area_bottom.insert(1.0,ex.__class__.__name__+"\n"+str(ex))

    @edit_bottom_textarea
    def save_handler(self,event):
        filename = asksaveasfilename(filetypes = (("txt files","*.txt"),("all files","*.*")))
        file = open(filename,'w')
        file.write(self.text_area_top.get(1.0,END))
        file.close()
        # self.text_area_top.delete('1.0', END) 
        # self.text_area_top.insert(1.0,text)

if  __name__ == "__main__":
    FILE_NAME  = 'source.txt'
    root = Tk()
    gui = Complier(root,FILE_NAME)
    root.state('zoomed')
    root.mainloop()

