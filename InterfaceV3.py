from tkinter import *
import tkinter


class Display:

    def __init__(self,grille,dic = None):
        self.boxesPerRow=grille.nRows
        self.height=700
        self.width=700
        rempl=self.height/self.boxesPerRow
        self.grille = grille
        self.window=Tk()
        self.can=Canvas(self.window, width=self.width, height=self.height, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.window, text='Fermer la fenêtre', command=self.window.destroy)
        self.bstop.pack()
        self.chaine = Label(self.window)
        self.can.bind("<Motion>",self.showCase)
        self.chaine.pack()

        for c in range(self.boxesPerRow):
                    self.can.create_line(c*rempl, 0,c*rempl,self.height)
                    self.can.create_line(0,c*rempl,self.width,c*rempl)
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

    def showCase(self,event):
        rempl = self.height/self.boxesPerRow

        xc , yc = int(event.x/rempl) , int(event.y/rempl)
        #print("Case :",repr(self.grille.getCell(xc,yc)))
        cell = self.grille.getCell(xc,yc)
        if cell:
            self.chaine.configure(text = "Case :"+ repr(cell))

    def cell(self,cell, color = None):
        rempl=self.height/self.boxesPerRow
        x=cell.x*rempl
        y=cell.y*rempl

        #print("Disp ",cell," ",color,"x ",x," y ",y," rempl ",rempl)
        if cell.typeC == "S" or cell.typeC == "G" :
            color = self.dic[cell.typeC]


        rect = self.can.create_rectangle(x,y,x+rempl,y+rempl,fill=color)
        txt = self.can.create_text(x+rempl/2, y+rempl/2,fill="white",activefill="yellow", text=cell.txt,  width=rempl)
        self.can.tag_raise(txt)



    def reset(self):
        for typeC in self.dic:
            self.colorType(typeC,self.dic[typeC])

    def showPath(self,path,color,):
        for node in path:
            self.cell(node.cell, color)
