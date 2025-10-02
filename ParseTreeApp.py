#Case Samples
#e=Z/(5*X)
#Y=e+x+Z*9
#z=(E-e)/2
#x=(2+e)*(2-e)

import sys
import nltk
import tkinter as tk
from nltk.tree import *
from tkinter import *
from tabulate import tabulate

root = Tk()


ProductionRules = """
assign -> id '=' expr
expr -> '(' expr ')' | expr '*' expr
expr -> id '/' expr | expr '/' const | expr '/' id
expr -> id '+' expr | id '-' expr | id '*' expr | id '/' expr
expr -> id '+' id | id '-' id |id '/' id | id '*' const | id '-' const
expr -> const '+' id | const '-' id | const '*' id | const '/' id
id -> 'E' | 'X' | 'Y' | 'Z' | 'e' | 'x' | 'y' | 'z'9
const -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
"""

grammar = nltk.CFG.fromstring(ProductionRules)

def Start_Parsing(String):
    global Lexemes
    
    ProductionRulesUsed.grid_remove()
    DisplayLexemesTokens.grid_remove()
    button1.config(state = "disabled")
    textbox.config(state="disabled")
    

    def Start_LexicalAnalysis(Lexemes):
        global LexemesTokens, LexemeCount, TokenCount, Count, Expressions
        LexemesTokens = {'id': [], 'const': [], 'optr': [], 'punctuator': []}
        Expressions = []
        LexemeCount = 0
        TokenCount = 0
        Count = 0
        current_expr = ''
        ExpressionStructure = []
        AmbiguousStructure = ["id+id+id","id-id-id","id*id*id","id/id/id",
                            "const+const+const","const-const-const","const*const*const","const/const/const",
                            "id+id+const","id-id+const","id*id+const","id/id+const",
                            "id+id-const","id-id-const","id*id-const","id/id-const",
                            "id+id*const","id-id*const","id*id*const","id/id*const",
                            "id+id/const","id-id/const","id*id/const","id/id/const"]


        StrLexemes = ''.join(str(char) for char in Lexemes)

        for lexeme in Lexemes:
            if lexeme == "=":
                equals_index = StrLexemes.find('=')
                if equals_index != -1:
                    WholeExpression = StrLexemes[equals_index + 1:].strip()
                    Expressions.append(WholeExpression)

                LexemesTokens['optr'].extend(lexeme)

                LexemeCount += 1
                TokenCount += 1
                Count += 1

            elif lexeme in ['E', 'X', 'Y', 'Z', 'e', 'x', 'y', 'z']:
                if lexeme in LexemesTokens.get('id', ['E', 'X', 'Y', 'Z', 'e', 'x', 'y', 'z']):
                    pass
                else:
                    LexemesTokens['id'].extend(lexeme)

                LexemeCount += 1
                TokenCount += 1
                Count += 1

                ExpressionStructure.append("id")

            elif lexeme in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if lexeme in LexemesTokens.get('const', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                    pass
                else:
                    LexemesTokens['const'].extend(lexeme)

                LexemeCount += 1
                TokenCount += 1
                Count += 1

                ExpressionStructure.append("const")

            elif lexeme in ['+', '-', '*', '/', '=']:
                if lexeme in LexemesTokens.get('optr', ['+', '-', '*', '/', '=']):
                    pass
                else:
                    LexemesTokens['optr'].extend(lexeme)

                LexemeCount += 1
                TokenCount += 1
                Count += 1

                if lexeme == "=":
                    pass
                else:
                    ExpressionStructure.append(lexeme)

            elif lexeme == ")":
                if lexeme in LexemesTokens.get('punctuator', [")"]):
                    pass
                else:
                    LexemesTokens['punctuator'].extend(lexeme)
                
                LexemeCount += 1
                TokenCount += 1
                Count += 1

                ExpressionStructure.append(")")

            elif lexeme == "(":
                if lexeme in LexemesTokens.get('punctuator', ["("]):
                    pass
                else:
                    LexemesTokens['punctuator'].extend(lexeme)
                
                LexemeCount += 1
                TokenCount += 1
                Count += 1

                ExpressionStructure.append("(")

                current_expr = '('
                open_parentheses = 1
                for char in Lexemes[LexemeCount:]:
                    current_expr += char
                    if char == "(":
                        open_parentheses += 1
                    elif char == ")":
                        open_parentheses -= 1
                        if open_parentheses == 0:
                            Expressions.append(current_expr)
                            current_expr = ''
                            break
                if current_expr:
                    Expressions.append(current_expr)


            else:
                pass

        DefineAmbiguity(ExpressionStructure, AmbiguousStructure)    


    def DefineAmbiguity(ExpressionStructure, AmbiguousStructure):
        ExpressionStructure = ''.join(str(char) for char in ExpressionStructure)
        DisplayAmbiguity.grid(row=0, padx=10, pady=10, sticky="NE")

        def Substring(substring, string):
            return substring in string
        Ambiguous = any(Substring(substring, ExpressionStructure) for substring in AmbiguousStructure)
        if Ambiguous:
            DisplayAmbiguity.config(text=f"{input_string.get()} is AMBIGUOUS!",bg="#CE4257",fg="#4F000B")
        else:
            DisplayAmbiguity.config(text=f"{input_string.get()} is NOT AMBIGUOUS!",bg="#4E148C",fg="#858AE3")




    def add_spaces(string):
        return ' '.join(string)


    def parse_expression(Lexemes):
        parser = nltk.ChartParser(grammar)
        for tree in parser.parse(Lexemes):
            return tree


    Character = add_spaces(String.get())
    Lexemes = Character.split()

#Events
    def enable_button2():
        button2.config(state = "normal")
        button2.bind("<Enter>", on_enterBtn2)
        button2.bind("<Leave>", on_leaveBtn2)
    enable_button2()

    def Reset():
        enable_button2()
    Reset()

    def DisableAllWidgets():
        textbox.config(state = "disabled")
        button1.config(state = "disabled")
        button2.config(state = "disabled")

    def EnableAllWidgets():
        textbox.config(state="normal")
        textbox.delete(0,tk.END)
        button1.config(state="normal")
        WarningWindow.destroy()
        
    def WarningWindowFunction(message):
        DisableAllWidgets()
        global WarningWindow
        WarningWindow = tk.Toplevel(root)
        WarningWindow.title("WARNING!")
        WarningWindow.geometry("550x200")
        WarningWindow.config(bg="#9FD8CB")

        WarningMessage = tk.Label(WarningWindow, text=f"{message}", width=45, font=("Arial Bold", 14))
        WarningMessage.place(relx=.5, rely=.5,anchor= CENTER)
        WarningMessage.config(bg="#9FD8CB",fg="#191E29")

        WarningWindow.protocol("WM_DELETE_WINDOW",EnableAllWidgets)

#Exception Catchers
    try:
        Start_LexicalAnalysis(Lexemes)
        parse_tree = parse_expression(Lexemes)
        parse_tree.draw()
    except (ValueError, AttributeError, UnboundLocalError):
        DisplayAmbiguity.grid_remove()
        WarningWindowFunction("Please refer to the Production Rules of the Program!")


def ShowProductionRulesUsed(Lexemes):
    parser = nltk.ChartParser(grammar)

    textbox.config(state="normal")
    button1.config(state = "normal")
    ProductionRulesUsed.grid(row=5, padx=10, pady=10, sticky="E")
    DisplayLexemesTokens.grid(row=5, padx=10, pady=10, sticky="W")
    DisplayLexemesTokens.config(text=f"Lexical Analysis:\n\n{tabulate(LexemesTokens.items(), headers=['Tokens', 'Lexemes',], tablefmt='grid')}\n\nNumber of Lexemes: {LexemeCount}\nNumber of Tokens: {TokenCount}\nCount: {Count}\nExpressions\n{Expressions}")
    button2.config(state = "disabled")
    
    for tree in parser.parse(Lexemes):
        production_text = "\n"
        for production in tree.productions():
            production_text += str(production) + "\n"
            ProductionRulesUsed.config(text=f"Used Production Rules of\n{input_string.get()}:\n{''.join({tk.END, production_text})}")
    textbox.delete(0,tk.END)


#User Interface        
def GUI():
    global textbox, button1, button2, ProductionRulesUsed, input_string, DisplayLexemesTokens, DisplayAmbiguity, on_enterBtn2, on_leaveBtn2


    bgColor = "#191E29"
    btnColor = "#132D46"
    btnfgColor = "#9FD8CB"

    logo_image = tk.PhotoImage(file="TSULogo.png")
    root.iconphoto(True, logo_image)

    root.title("Parsing Tree App")
    root.geometry('590x850')
    root.config(bg=f"{bgColor}")

    def on_enterBtn1(event):
        button1.config(cursor="hand2",bg="#9FD8CB",fg="#132D46")

    def on_leaveBtn1(event):
        button1.config(cursor="",bg=f"{btnColor}",fg=f"{btnfgColor}")

    def on_enterBtn2(event):
        button2.config(cursor="hand2",bg="#9FD8CB",fg="#132D46")

    def on_leaveBtn2(event):
        button2.config(cursor="",bg=f"{btnColor}",fg=f"{btnfgColor}")

    def CloseApp():
        sys.exit()


    label1 = Label(root, text="Enter your Expression below: ", font=("Arial Bold", 12))
    label1.grid(row=0, column=0, padx=10 ,pady=10, sticky=W)
    label1.config(bg=f"{bgColor}",fg="#9FD8CB")

    DisplayProductionRule = Label(root, text=f"ProductionRules:\n{ProductionRules}", width=56, font=("Arial Bold",12))
    DisplayProductionRule.config(bg="#122932",fg="#01C38D")
    DisplayProductionRule.grid(row=4, column=0, padx=10, pady=10, sticky=W)

    input_string = StringVar()
    textbox = Entry(root, textvariable=input_string, width=25, font=("Arial Bold", 12))
    textbox.grid(row=1, column=0, padx=10 ,pady=10, sticky=W)
    textbox.config(bg="#132D46",fg="#9FD8CB")

    ProductionRulesUsed = Label(root, text="", width=25, font=("Arial Bold", 12))
    ProductionRulesUsed.config(bg="#495159",fg="#A1E8CC")
    ProductionRulesUsed.grid_remove()

    DisplayLexemesTokens = Label(root, text="", width=30, font=("Arial Bold", 12))
    DisplayLexemesTokens.config(bg="#495159",fg="#A1E8CC")
    DisplayLexemesTokens.grid_remove()

    DisplayAmbiguity = Label(root, text="", width=30, font=("Arial Bold", 12))
    DisplayAmbiguity.grid_remove()

    button1 = Button(root, command=lambda: Start_Parsing(input_string), text="Show Parse Tree Diagram", font=("Arial Bold", 12))
    button1.grid(row=2,column=0,sticky=W, padx=10, pady=10)
    button1.config(bg=f"{btnColor}",fg=f"{btnfgColor}")
    button1.bind("<Enter>", on_enterBtn1)
    button1.bind("<Leave>", on_leaveBtn1)

    button2 = Button(root, command=lambda:ShowProductionRulesUsed(Lexemes), text="Show Lexical Analysis and Production Rule Used in Expression", font=("Arial Bold", 12), state = "disabled")
    button2.grid(row=3,column=0,sticky=W,padx=10 ,pady=10)
    button2.config(bg=f"{btnColor}",fg=f"{btnfgColor}")

        
    root.protocol("WM_DELETE_WINDOW",CloseApp)
    root.mainloop()
    

GUI()