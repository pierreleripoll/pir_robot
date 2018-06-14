#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

from Tkinter import *
from functools import*
from simulation.astar import AStar
from simulation.node import Node
from simulation.robot import Robot
from simulation.cell import Cell
from simulation.coordination import Coordination
import rospy
from std_msgs.msg import String


class Display:

    def __init__(self,grille,astar,dic = None,paths= [],robots=[]):
        self.dic = dic
        self.paths=paths
        self.robots=robots
        self.astar=astar
        self.boxesPerRow=grille.nRows
        self.boxesPerColumn=grille.nColumns
        self.height=700
        self.width=700
        self.boxSide=self.height/(max(self.boxesPerRow,self.boxesPerColumn))
        self.grille = grille
        self.window=Tk()
        self.window.resizable(True,False)
        self.window.title("Workspace")
        #Fenetre secondaire
        self.utility=Toplevel(self.window)
        self.utility.title("Toolbox")
        self.msgButton = Button(self.utility, text='Envoyer les chemins aux robots', command=self.sendRobotsMsgs)
        #Fenetre principal
        self.utility.transient(self.window)
        self.can=Canvas(self.window, width=self.boxSide*self.boxesPerColumn, height=self.boxSide*self.boxesPerRow, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.window, text='Fermer les fenêtres', command=self.window.destroy)
        self.bstop.pack()
        #Pour creation de robots
        self.nbR=0
        self.Rname=None
        self.click=0
        self.start=None
        self.end=None
        #element pour afficher les robots
        self.brobot=Button(self.utility, text='Créer robot',command=partial(self.transition_robot,self.can))
        self.brobot.pack(side="left")
        self.msgButton.pack()
        self.chain = Label(self.window)
        self.can.bind("<Motion>",self.showBox)
        self.chain.pack()

        self.masterPub = rospy.Publisher("master", String, queue_size=10)
        rospy.init_node("master")

#Cree la grille sur l ecran--------------------------------------------------
        for c in range(min(self.boxesPerRow,self.boxesPerColumn)):
                    self.can.create_line(self.width*self.boxSide, 0,self.width*self.boxSide,self.width)
                    self.can.create_line(0,self.height*self.boxSide,self.height,self.height*self.boxSide)
        if dic :
            self.dic = dic
            for typeC in dic:
                self.colorType(typeC,dic[typeC])
        self.window.mainloop()

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

#Fonctions qui affiche les chemins -----------------------------------------------------------------
    def showPath(self,path,color,active) :
        if active ==0:
            for node in path:
                self.showNode(active,node,color)
        elif active==1:
            for node in path:
                    self.showNode(active,node,"white")

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


    def showNode(self,active , node,color = None):

        x=node.x*self.boxSide
        y=node.y*self.boxSide

        #print("Disp ",cell," ",color,"x ",x," y ",y," self.boxSide ",self.boxSide)
        if node.typeC == "S" or node.typeC == "G" :
            color = self.dic[node.typeC]

        txt = self.can.create_text(x+self.boxSide/2, y+self.boxSide/2,fill="white",activefill="yellow", text=node.txt,  width=self.boxSide)

        if active==0:
            rect = self.can.create_rectangle(x,y,x+self.boxSide,y+self.boxSide,fill=color)
            node.rectangle.append(rect)
            self.can.itemconfigure(rect,state="normal")
            if node.dir== "L":
                arrow=self.can.create_line(x,y+20,x+self.boxSide,y+20, arrow="first")
            elif node.dir=="R":
                arrow=self.can.create_line(x+self.boxSide,y+20,x,y+20, arrow="first")
            if node.dir== "D":
                arrow=self.can.create_line(x+20,y+self.boxSide,x+20,y, arrow="first")
            if node.dir== "U":
                arrow=self.can.create_line(x+20,y,x+20,y+self.boxSide, arrow="first")
            node.arrow.append(arrow)
        else:
            for i,p in enumerate(node.rectangle):
                i=i
            self.can.delete(node.rectangle[i])
            self.can.delete(node.arrow[i])
        self.can.tag_raise(txt)


#Fonction qui crée les robots-----------------------------------------------------------------
    def create_robot(self,event):
        print(event.x)
        print(event.y)
        xc , yc = int(event.x/self.boxSide) , int(event.y/self.boxSide)
        cello=self.grille.getCell(xc,yc)


        if (self.click==0):
            self.start=cello
            self.click=1
            self.grille.chgCell(xc,yc,"S")
            for typeC in self.dic:
                self.colorType(typeC,self.dic[typeC])


        elif(self.click==1):
            print("Robot créé")
            self.end=cello
            self.grille.chgCell(xc,yc,"G")
            for typeC in self.dic:
                self.colorType(typeC,self.dic[typeC])
            robotStart=Node(self.start,"L")
            robotEnd=Node(self.end,"L")
            if self.Rname == None:
                self.popup()
                self.window.wait_window(self.top)
                newRobot=Robot(self.Rname,robotStart,robotEnd)
                self.nbR=self.nbR+1
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
                self.afficher_chemin(newRobot,self.nbR)
                self.click=0
            else:
                pass

            self.can.unbind("<ButtonPress>")


        else:
            print ('Ya pas de robot ici Missieu')



    def transition_robot(self,Canvas):
        self.callbutton=self.can.bind("<ButtonPress>",self.create_robot)



    #Afficher des checkbox dynamiques pour les robots-----------------------------------------------------------------
    def cb(self,p,i):
        if p.state.get():
            self.pathColor=self.choiceColor(i)
            self.showPath(p.path,self.pathColor,0)
        else:
            self.pathColor=self.choiceColor(i)
            self.showPath(p.path,self.pathColor,1)


    def afficher_chemin(self,p,i):
        p.state=IntVar(self.utility)
        self.check = Label(self.utility, text=str(p.state.get()))
        self.checkbox =Checkbutton(self.utility,text=self.Rname ,variable=p.state,onvalue=1,offvalue=0,command=lambda m=p, n=i: self.cb(m,n))
        self.checkbox.pack(side="top",anchor="w")
        self.Rname=None

#Fenetre pour nommer les robots -----------------------------------------------------------------
    def popup(self):
        top=self.top=Toplevel(self.utility)
        self.l=Label(top,text="Veuilliez rentrer le nom de votre Robot")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.Rname=self.e.get()
        self.top.destroy()

    def sendRobotsMsgs(self) :
        try:
            print("master")
            for robot in self.robots :
                robotMsg = robot.createMsg()
                self.masterPub.publish(robotMsg)
        except rospy.ROSInterruptException:
            pass
