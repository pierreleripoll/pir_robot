from tkinter import *
import tkinter
from functools import*

class Display:

    def __init__(self,grille,dic = None,pathes= []):
        self.dic = dic
        self.pathes=pathes
        self.boxesPerRow=grille.nRows
        self.height=700
        self.width=700
        self.boxSide=self.height/self.boxesPerRow
        self.grille = grille
        self.window=Tk()
        #Ajouté
        self.window.resizable(True,False)
        self.window.title("Workspace")
        self.utility=Toplevel(self.window)
        self.utility.title("Toolbox")
                #Ajouté

        self.utility.transient(self.window)
        self.can=Canvas(self.window, width=self.width, height=self.height, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.window, text='Fermer la fenêtre', command=self.window.destroy)
        self.bstop.pack()
        #

        #self.bstart=Button(self.utility, text='Positionner le départ',command=self.transition_start(self.can))
        #self.end=Button(self.utility, text='Positionner la fin', command=self.transition_end(self.can))
        #self.brobot=Button(self.utility, text='Créer robot',command=self.transition_start(self.can))
        #self.bstart.pack(side="left")
        #self.end.pack(side="left")
        #self.brobot.pack(side="left")
            #
        #CheckButton Ajouté
        for i, p in enumerate(self.pathes):
            self.is_checked =StringVar(self.utility, 'red')
            self.check = Label(self.utility, text=str(self.is_checked.get()))
            self.pathColor=self.choiceColor(i)
            self.checkbox = Checkbutton(self.utility,text="Robot n°"+str(i) ,variable=self.is_checked, onvalue="red",offvalue="white",command=partial(self.showPath,p,self.pathColor))
            self.checkbox.pack()
        #
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
            self.showNode(node,color)
    #RAJOUT -----------------------------------------------------------------
    def choiceColor(self,i):
        if i == 0:
            return "red"
        elif i==1:
            return "yellow"
        elif i==2:
            return "purple"
        elif i==3:
            return "brown"
        elif i==4:
            return "orange"
        elif i==5:
            return "pink"
        elif i==6:
            return "thistle"
        elif i==7:
            return "black"


    def showNode(self, node,color = None):

        x=node.x*self.boxSide
        y=node.y*self.boxSide

        #print("Disp ",cell," ",color,"x ",x," y ",y," self.boxSide ",self.boxSide)
        if node.typeC == "S" or node.typeC == "G" :
            color = self.dic[node.typeC]

        rect = self.can.create_rectangle(x,y,x+self.boxSide,y+self.boxSide,fill=color)
        txt = self.can.create_text(x+self.boxSide/2, y+self.boxSide/2,fill="white",activefill="yellow", text=node.txt,  width=self.boxSide)

        if node.dir== "L":
            arrow=self.can.create_line(x,y+20,x+self.boxSide,y+20, arrow="first")
        elif node.dir=="R":
            arrow=self.can.create_line(x+self.boxSide,y+20,x,y+20, arrow="first")
        if node.dir== "D":
            arrow=self.can.create_line(x+20,y+self.boxSide,x+20,y, arrow="first")
        if node.dir== "U":
            arrow=self.can.create_line(x+20,y,x+20,y+self.boxSide, arrow="first")

        self.can.tag_raise(txt)
        #RAJOUT ET PROBLEME ICI-----------------------------------------------------------------
#LEs Probleme viennent après
#Probleme avec unbindTheButton ne peut plus agir ensuite
    def unbindTheButton(self,event):
        self.can.unbind("<ButtonRelease>",self.callfunction)
        self.can.unbind("<ButtonPress>",self.callbutton)
        return

    def create_robot(self,event):
        print(event.x)
        print(event.y)
        cello=self.grille.getCell(event.x,event.y)
        self.booleanstart=False
        self.booleanend=False
        if cello.typeC =="S":
            self.start=cello
            self.booleanstart=True
        elif cello.typeC =="G":
            self.end=cello
            self.booleanend=True

        elif(self.booleanstart==True and self.booleanend==True):
            newRobot=Robot("B",self.start,self.end)
            self.robots.append(newRobot)
            paths = self.astar.findAllPaths(self.robots)
            self.booleanstart=False
            self.booleanend=False
            return


    def transition_start(self,Canvas):
        self.callbutton=self.can.bind("<ButtonPress>",self.create_start)

    def transition_end(self,Canvas):
        self.callbutton=self.can.bind("<ButtonPress>",self.create_end)

    def transition_robot(self,Canvas):
        self.callbutton=self.can.bind("<ButtonPress>",self.create_robot)

    def create_start(self,event):
        X=event.x
        Y=event.y
        print("j'y suis arrivé DEBUT")
        Node(Cell(X,Y,"S"),"L")

        for typeC in self.dic:
            self.colorType(typeC,self.dic[typeC])
        self.callfunction=self.can.bind("<ButtonRelease>",self.unbindTheButton)
        return
    def create_end(self,event):
        X=event.x
        Y=event.y
        Node(Cell(X,Y,"G"),"L")
        print("j'y suis arrivé FIN")
        for typeC in self.dic:
            self.colorType(typeC,self.dic[typeC])
        self.callfunction=self.can.bind("<ButtonRelease>",self.unbindTheButton)
        return
    #RAJOUT-----------------------------------------------------------------
