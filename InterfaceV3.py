from tkinter import *
from functools import*
from astar import AStar
from node import Node
from robot import Robot
from cell import Cell
from coordination import Coordination
import pdb
class Display:

    def __init__(self,grille,astar,dic = None,paths= [],robots=[]):

        self.dic = dic
        self.paths=paths
        self.robots=robots
        self.astar=astar
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
        self.booleanstart=False
        self.booleanend=False
        self.click=0
        self.nbrTot=0
        self.start=None
        self.end=None
        self.brobot=Button(self.utility, text='Créer robot',command=partial(self.transition_robot,self.can))
        self.brobot.pack(side="left")
            #
        #CheckButton Ajouté
        self.afficher_chemin()
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

#RAJOUT -----------------------------------------------------------------
    def showPath(self,path,color,active) :
        if active==1 or active ==0:
            for node in path:
                self.showNode(node,color)
        elif active==0:
            for node in path:
                self.showNode(node,"white")

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


    def create_robot(self,event):
        print(event.x)
        print(event.y)
        xc , yc = int(event.x/self.boxSide) , int(event.y/self.boxSide)
        cello=self.grille.getCell(xc,yc)


        if (self.click==0):
            print("start positionné")
            self.start=cello
            self.click=1
            self.grille.chgCell(xc,yc,"S")
            for typeC in self.dic:
                self.colorType(typeC,self.dic[typeC])


        elif(self.click==1):
            print("Robot créé")
            print("end positionné")
            self.end=cello
            self.grille.chgCell(xc,yc,"G")
            print("j'y suis arrivé FIN")
            for typeC in self.dic:
                self.colorType(typeC,self.dic[typeC])
            robotStart=Node(self.start,"L")
            robotEnd=Node(self.end,"L")
            self.nbr_R=self.nbr_R+1
            newRobot=Robot(str(self.nbr_R),robotStart,robotEnd)
            self.robots.append(newRobot)
            self.grille.setRobots(self.robots)
            newRobot.path=self.astar.findPath(robotStart,robotEnd)
            self.paths.append(newRobot.path)


            coor = Coordination(self.robots)
            check , node = coor.validatePath(newRobot)
            print("\n",check,repr(node))

            if node:
                node.changeType("?")
                self.grille.setCell(node)
                newRobot.path=self.astar.findPath(robotStart,robotEnd)
                self.paths.append(newRobot.path)
                node.changeType(".")
                self.grille.setCell(node)
                check , node = coor.validatePath(newRobot)
                print("\n\nAFTER CHANGING OBSTACLE\n",check,repr(node))

            newRobot.setTime()
            self.afficher_chemin()
            self.click=0
            self.can.unbind("<ButtonPress>")


        else:
            print ('Ya pas de robot ici Missieu')



    def transition_robot(self,Canvas):
        #pdb.set_trace()
        self.callbutton=self.can.bind("<ButtonPress>",self.create_robot)



    #RAJOUT-----------------------------------------------------------------
    def afficher_chemin(self):
            for i, p in enumerate(self.paths):
                if self.nbrTot==i:
                    self.is_checked =IntVar(self.utility)
                    self.nbr_R=i
                    self.check = Label(self.utility, text=str(self.is_checked.get()))
                    self.pathColor=self.choiceColor(i)
                    self.checkbox = Checkbutton(self.utility,text="Robot n°"+str(i) ,variable=self.is_checked,onvalue=1,offvalue=0,command=partial(self.showPath,p,self.pathColor,self.is_checked.get()))
                    self.checkbox.pack()
                    self.nbrTot=self.nbrTot+1
                else:
                    pass
