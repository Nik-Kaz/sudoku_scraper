from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("SUDOKU")
root.geometry('440x500')


class Sudoku():

    def __init__(self):
        self.root = root
        self.current = []
        self.root.resizable(0,0)
        self.entry_box_list = []
        self.sudoku = self.scrapSudoku()
        self.entries = self.defEntry()
        self.buttons = self.getButtons()
        self.complete = self.isComplete()
        self.focusedEntry = ""
        # self.completeBut = self.completeSudoku()
    """Web scrapper"""

    def scrapSudoku(self):
        page = requests.get(
            "https://randompearls.com/reference/tools/sudoku-solver/")
        soup = BeautifulSoup(page.content, 'html.parser')
        for i in range(0, 81):
            self.current.append(soup.find(id="cell_" + str(i)).text)


    """Making rows in the same horizontal, vertical rows and 3x3 squares not repeat themselves"""

                
    def unavaibleNums(self,position):
        numbForCheck = []
        def addTolist(list,elem):
            if elem != '' and int(elem) not in list:
                list.append(int(elem))
        position = int(position)
        column = position % 9
        row = int(position / 9)
        """Horizontal rows"""
        for i in range(0, 9):
            if column < i:
                addTolist(numbForCheck,self.current[position + i-column])
            elif column > i:
                addTolist(numbForCheck,self.current[position - (column - i)])
        """Vertical rows"""
        for j in range(0,9):
            if row < j:
                addTolist(numbForCheck,self.current[position + 9*(j-row)])
            elif row > j:
                addTolist(numbForCheck,self.current[position - 9*(row-j)])
        """numbers from the same 3x3 square"""
        squareCol = (column + 1)%3
        squareRow = int((row + 1)%3)
        for i in range(0,3):
            var = i if squareCol == 1 else (-(1-i) if squareCol == 2 else -i)
            colVar1 = 9 if squareRow == 1 or squareRow == 2 else -9
            colVar2 = 18 if squareRow == 1 else (-9 if squareRow == 2 else -18)
            addTolist(numbForCheck,self.current[position + var])                
            addTolist(numbForCheck,self.current[position + colVar1 + var])
            addTolist(numbForCheck,self.current[position + colVar2 + var])
        return numbForCheck


            
    def defEntry(self):
        
        def isCorrectNum(num, position):
            position = int(position)
            existingNums = self.unavaibleNums(position)
            if num in existingNums:
                return False
            else:
                self.current[position]=num
                if self.complete:
                    messagebox.showinfo("Congratulations","End of the game")
                return True
            

        def validateInput(P, e, currVal):
            if P.isdigit():
                i = int(P)
                if i < 1 or i > 9:
                    return False
                else:
                    return isCorrectNum(i, str(e).split('_')[2])
            elif P == '':
                posisiton = int(str(e).split('_')[2])
                self.current[posisiton]=''
                return True
            else:
                return False

        """Making Entry and validations"""

        reg = self.root.register(validateInput)
        for i in range(0, 81):
            var = StringVar()
            entry_box = Entry(
                self.root, width=2, textvariable=var, name='entry_Name_' + str(i), font='Montserrat 25', justify='center')
            var.set(self.current[i])
            
            """Dynamic creation of entries"""
            entry_box.config(validate='key',validatecommand=(reg, '%P', entry_box,entry_box.get()))
            entry_box.grid(row=int(i/9), column=int((i+9) % 9))

            """Chaning entry  colors by using if statements"""
            if(self.current[i] != ''):
                entry_box.config(state='readonly')
            if((i % 9 in (0, 1, 2, 6, 7, 8) and i not in range(27, 54)) or i in (30, 31, 32, 39, 40, 41, 48, 49, 50)):
                entry_box.config(readonlybackground='#E8E8CC', bg='#E8E8CC')
            else:
                entry_box.config(readonlybackground='#0B4619', bg='#0B4619')

            self.entry_box_list.append(entry_box)
            
    """Buttons"""
    def getButtons(self):
        for i in range(1, 10):
            btn = Button(self.root, width=3, height=1, text=i, bg='#116530',
                         font='Montserrat', justify='center')
            btn.grid(row=9, column=int((i+8) % 9),sticky='nsew')
            
                
            
                    
    def isComplete(self):
        for x in self.current:
            if x == '':
                return False
        return True

    def run(self):
        self.root.mainloop()
        
    # def completeSudoku(self):
    #     i = 0
    #     while i < 81:
    #         existElems = self.unavaibleNums(i)
    #         print(existElems)
    #         i = i + 1

    # def finishSudoku(self):
    #     w = Button(self.root,text="Finish",command=self.completeSudoku,width=3, height=1,)
    #     w.grid(row=10,column=1)

if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.run()
