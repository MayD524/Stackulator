## just for making life easier
from cmath import e
from math import pi

from tkinter.messagebox import showerror
from stackulator import stackulator, stackArray
import tkinter as tk

DEFAULT_SIZE = (470, 635)

class gui:
    def __init__(self) -> None:
        self.root  = tk.Tk()
        self.stack = stackulator()
        self.allowTyping = True
        self.root.title("Stackulator")
        self.root.geometry("{}x{}".format(DEFAULT_SIZE[0], DEFAULT_SIZE[1]))
        #self.root.resizable(False, False)
        self.layout()
        
    def layout(self) -> None:
        
        ## add a listbox for the stack
        self.stackList = tk.Listbox(self.root, width=30, height=10, font=("Courier", 15))
        self.stackList.grid(row=0, column=0, sticky="nsew")
        self.stackList.config(justify="right")
        
        sc = tk.Scrollbar(self.root, orient="vertical", command=self.stackList.yview)
        sc.grid(row=0, column=1, sticky="nsew")
        
        ## link the scrollbar to the listbox
        sc.config(command=self.stackList.yview)
        self.stackList.config(yscrollcommand=sc.set)
        
        ## text entry for the current value
        self.curVal = tk.StringVar()
        self.curVal.set("0")
        
        entry = tk.Entry(self.root, textvariable=self.curVal, width=8, font=("Courier", 20))
        entry.grid(row=1, column=0, sticky="nsew")
        entry.config(justify="right")
        entry.config(state="readonly")
        
        
        self.root.bind("<Return>", self.enter)
        
        btnFrame = tk.Frame(self.root, padx=5)
        ## add buttons
        self.ops = {
            "+"    : self.stack.add,
            "-"    : self.stack.sub,
            "*"    : self.stack.mul,
            "/"    : self.stack.div,
            "^"    : self.stack.pow,
            "!"    : self.stack.fact,
            "√"    : self.stack.sqrt,
            "x√"   : self.stack.xroot,
            "Join" : self.stack.join,
            "sin"  : self.stack.sin,
            "cos"  : self.stack.cos,
            "tan"  : self.stack.tan,
            "log"  : self.stack.log,
            "ln"   : self.stack.ln,
            "atan" : self.stack.atan,
            "asin" : self.stack.asin,
            "acos" : self.stack.acos,
            "abs"  : self.stack.abs,
            "fact" : self.stack.fact,
            "π"    : self.setPi,
            "Pop"  : self.stack.pop,
            "CLR"  : self.stack.clear,
            "Dup"  : self.stack.dup,
            "Roll" : self.stack.roll,
            "Swap" : self.stack.swap,
            "="    : self.enter,
            "-/+"  : self.neg,
        }
        ## add the buttons for numbers
        cRow = 0
        cCol = 0
        for i in range(9, -1, -1):
            btn = tk.Button(btnFrame, width=5,text=str(i), font=("Courier", 16), command=lambda i=i: self.curVal.set(self.curVal.get()+str(i)))
            if i == 0:
                btn.grid(row=cRow, column=cCol+1, sticky="nsew")
                continue
            btn.grid(row=cRow, column=cCol, sticky="nsew")
            cCol += 1
            if cCol > 2 :
                cRow += 1
                cCol = 0
                
        cRow = 0
        cCol = 3
        for k, f in self.ops.items():
            tk.Button(btnFrame, text=k, font=("Courier", 16), command=lambda f=f: self.btnCallback(f)).grid(row=cRow, column=cCol, sticky="nsew")
            
            cCol += 1
            if cCol > 5 :
                cRow += 1
                cCol = 3
                
        btnFrame.grid(row=2, column=0, sticky="nsew")
    
        ## on any action, update the stack
        self.root.bind("<Button-1>", self.displayStack)
        self.root.bind("<Key>", self.displayStack)
        ## on number press, update the entry
        self.root.bind("<Key>", self.updateEntry)
        ## on backspace, delete the last character
        self.root.bind("<BackSpace>", lambda event: self.curVal.set(self.curVal.get()[:-1]))
        
    def neg(self) -> None:
        x = self.curVal.get()
        x = x[:-1] if x[-1] == '-' else '-'+x
        self.curVal.set(x)
        
    def setPi(self) -> None:
        self.curVal.set(pi)
        
    def btnCallback(self, func) -> None:
        x = self.curVal.get()
        if x != "0":
            if '.' in x:
                x = float(x)
            else:
                x = int(x)
            self.stack.push(x)
        func()
        x = self.stack.pop()
        self.displayStack()
        self.curVal.set(x)
        
    def updateEntry(self, event=None) -> None:
        cValue = self.curVal.get()
        if len(cValue) > 10:
            showerror("Error", "Value too large")
            return
        if event.char.isdigit():
            self.curVal.set(self.curVal.get() + event.char)
        elif event.char == ".":
            self.curVal.set(self.curVal.get() + event.char)
        else:
            match event.char:
                case "+":
                    self.btnCallback(self.stack.add)
                case "-":
                    self.btnCallback(self.stack.sub)
                case "*":
                    self.btnCallback(self.stack.mul)
                case "/":
                    self.btnCallback(self.stack.div)
                case "^":
                    self.btnCallback(self.stack.pow)
                case "!":
                    self.btnCallback(self.stack.fact)
                case "c":
                    self.btnCallback(self.stack.clear)
                case "d":
                    self.stack.dup()
                case "r":
                    self.stack.roll()
                case "s":
                    self.stack.swap()
                case "p":
                    self.curVal.set(str(pi))
                case "x":
                    self.stack.pop()
                case "e":
                    self.curVal.set(str(e))
                case "j":
                    self.btnCallback(self.stack.join)
        self.displayStack()
        
    def enter(self, event=None) -> None:
        ## get the current value in the entry
        val = self.curVal.get()
        if val.isalpha() and '-' not in val:
            showerror("Error", "Invalid input")
            return
        try:
            if "[" in val:
                val = val[1:-1]
                val = [float(x) if '.' in x else int(x) for x in val.split(",")]
                val = stackArray(val)
            elif '.' in val:
                val = float(val)
            elif val.isnumeric():
                val = int(val)
        except ValueError as e:
            showerror("Error", "Invalid input: " + str(e))
            return
        
        try:
            self.stack.push(val)
            self.curVal.set("0")
        except Exception as e:
            showerror("Error", str(e))
        self.displayStack()
        
    def displayStack(self, event=None) -> None:
        ## clear the stackList
        self.stackList.delete(0, tk.END)
        
        for i in range(len(self.stack.stack)):
            self.stackList.insert(tk.END, "{0:>5} {1:20}".format(len(self.stack.stack)-(i+1), self.stack.stack[i]))
        
    def bindControls(self) -> None:
        pass
        
    def mainloop(self) -> None:
        self.root.mainloop()
    
    
if __name__ == "__main__":
    g = gui()
    g.mainloop()