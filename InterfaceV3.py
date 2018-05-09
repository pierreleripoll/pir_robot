from tkinter import *
import tkinter


class Display:

    def __init__(self,grille,dic = None):
        self.boxesPerRow=grille.nRows
        self.height=700
        self.width=700
        self.boxSide=self.height/self.boxesPerRow
        self.grille = grille
        self.window=Tk()
        self.can=Canvas(self.window, width=self.width, height=self.height, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.window, text='Fermer la fenêtre', command=self.window.destroy)
        self.bstop.pack()
        self.chain = Label(self.window)
        self.can.bind("<Motion>",self.showBox)
        self.chain.pack()

        for c in range(self.boxesPerRow):
                    self.can.create_line(c*self.boxSide, 0,c*self.boxSide,self.height)
                    self.can.create_line(0,c*self.boxSide,self.width,c*self.boxSide)
        if dic :
            #print("Dic exists :",dic)
            self.dic = dic
            for typeC in dic:
                self.colorType(typeC,dic[typeC])

    def colorType(self,typeC,color):
        for column in self.grille.plan:
            for cell in column:
                if cell.typeC == typeC:
                    self.cell(cell,color)

    def showBox(self,event):
        xc , yc = int(event.x/self.boxSide) , int(event.y/self.boxSide)
        #print("Box :",repr(self.grille.getCell(xc,yc)))
        cell = self.grille.getCell(xc,yc)
        if cell:
            self.chain.configure(text = "Box :"+ repr(cell))

    def cell(self,cell, color = None):
        x=cell.x*self.boxSide
        y=cell.y*self.boxSide

        #print("Disp ",cell," ",color,"x ",x," y ",y," self.boxSide ",self.boxSide)
        if cell.typeC == "S" or cell.typeC == "G" :
            color = self.dic[cell.typeC]

        rect = self.can.create_rectangle(x,y,x+self.boxSide,y+self.boxSide,fill=color)
        txt = self.can.create_text(x+self.boxSide/2, y+self.boxSide/2,fill="white",activefill="yellow", text=cell.txt,  width=self.boxSide)
        self.can.tag_raise(txt)



    def reset(self):
        for typeC in self.dic:
            self.colorType(typeC,self.dic[typeC])

    def showPath(self,path,color) :
        for node in path:
            self.cell(node, color)
