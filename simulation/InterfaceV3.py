#!/usr/bin/env python
# -*- coding: utf-8 -*

from Tkinter import *
from functools import*
from astar import AStar
from node import Node
from robot import Robot
from cell import Cell
from coordination import Coordination
#import rospy
#from std_msgs.msg import String



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
        #Fenetre principal
        self.utility.transient(self.window)
        self.can=Canvas(self.window, width=self.boxSide*self.boxesPerColumn, height=self.boxSide*self.boxesPerRow, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.window, text='Fermer les fenêtres', command=self.window.destroy)
        self.bstop.pack()
        self.chain = Label(self.window)
        self.can.bind("<Motion>",self.showBox)
        self.chain.pack()
        #Pour creation de robots
        self.nbR=0
        self.Rname=None
        self.click=0
        self.start=None
        self.end=None
        self.decompte=0
        self.directionStart=None
        self.directionEnd=None
        self.check=[]
        self.checkbox=[]
        self.buttonactive=False
        self.buttonactive2=False
        #Element dans la fenetre secondaire
        self.introUtility=Label(self.utility,text="Voici les possibilité pour agir sur la fenêtre principale")
        self.introUtility.pack(side="top",anchor="s")
        self.baddObstacle=Button(self.utility, text='Ajouter un obstacle',command=partial(self.transition_obstacle,self.can))
        self.baddObstacle.pack(anchor="w")
        self.bdeleteObstacle=Button(self.utility, text='Retirer un obstacle',command=partial(self.transition_deleteObstacle,self.can))
        self.bdeleteObstacle.pack(anchor="w")
        self.msgButton = Button(self.utility, text='Envoyer les chemins aux robots')#self.sendRobotsMsgs)
        self.msgButton.pack(side="bottom",anchor="s")
        self.brobot=Button(self.utility, text='Créer robot',command=partial(self.transition_robot,self.can))
        self.brobot.pack(anchor="w")
        self.bdelete=Button(self.utility, text='Supprimer un robot',command=partial(self.deleteRobot))
        self.bdelete.pack(side="left",anchor="w")
        #self.masterPub = rospy.Publisher("master", String, queue_size=10)
        #rospy.init_node("master")
#Cree la grille sur l ecran--------------------------------------------------
        for c in range(max(self.boxesPerRow,self.boxesPerColumn)):
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
            cell.display_txt = self.can.create_text(x+self.boxSide/2, y+self.boxSide/2,fill="black",activefill="yellow", text=cell.txt,  width=self.boxSide)
            self.can.tag_raise(cell.display_txt)
        elif cell.typeC == "." :
            color = self.dic[cell.typeC]
        rect = self.can.create_rectangle(x,y,x+self.boxSide,y+self.boxSide,fill=color)
        cell.rectangle.append(rect)



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
            return "goldenrod"
        elif i==4:
            return "orange"
        elif i==5:
            return "pink"
        elif i==6:
            return "thistle"
        elif i==7:
            return "aqua"
        elif i==8:
            return "fuchsia"

    def showNode(self,active , node,color = None):

        x=node.x*self.boxSide
        y=node.y*self.boxSide

        #print("Disp ",node," ",color,"x ",x," y ",y," self.boxSide ",self.boxSide)
        # if node.typeC == "S" or node.typeC == "G" :
        #     color = self.dic[node.typeC]

        node.display_txt = self.can.create_text(x+self.boxSide/2, y+self.boxSide/2,fill="black",activefill="yellow", text=node.txt,  width=self.boxSide)

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
        elif active==1:
            for i,p in enumerate(node.rectangle):
                i=i
            self.can.delete(node.rectangle[i])
            self.can.delete(node.arrow[i])

        self.can.tag_raise(node.display_txt)

#Fonction qui crée les robots-----------------------------------------------------------------
    def create_robot(self,event):
        xc , yc = int(event.x/self.boxSide) , int(event.y/self.boxSide)
        cello=self.grille.getCell(xc,yc)
        if cello.typeC=="?":
            self.danger(self.can,"Vous avez séléctioné une position sur un obstacle, ce n'est pas possible")
            self.window.wait_window(self.attention)
        else:
            if (self.click==0):
                self.start=cello
                self.click=1
                self.grille.chgCell(xc,yc,"S")
                self.reset()


            elif(self.click==1):
                self.can.unbind("<ButtonPress>")
                self.end=cello
                self.grille.chgCell(xc,yc,"G")
                self.reset()
                if self.Rname == None:
                    self.popup()
                    self.window.wait_window(self.top)
                    self.directionStart=self.var.get()
                    self.directionEnd=self.var2.get()
                    print("direction de depart:",self.directionStart)
                    print("direction d arivee:", self.directionEnd)
                    robotStart=Node(self.start,self.directionStart)
                    robotEnd=Node(self.end,self.directionEnd)
                    newRobot=Robot(self.Rname,robotStart,robotEnd)
                    self.robots.append(newRobot)
                    self.grille.setRobots(self.robots)
                    newRobot.path=self.astar.findPath(robotStart,robotEnd)
                    self.paths.append(newRobot.path)


                    coor = Coordination(self.robots)
                    check , node = coor.validatePath(newRobot)

                    if node:
                        node.changeType("?")
                        self.grille.setCell(node)
                        newRobot.path=self.astar.findPath(robotStart,robotEnd)
                        self.paths.append(newRobot.path)
                        node.changeType(".")
                        self.grille.setCell(node)
                        check , node = coor.validatePath(newRobot)


                    self.afficher_chemin(newRobot,self.nbR)
                    self.nbR=self.nbR+1
                    newRobot.setTime()
                    self.click=0
                self.reset()
                self.buttonactive=False

    def transition_robot(self,Canvas):
        if self.buttonactive==True:
            pass
        else:
            self.buttonactive=True
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
        self.check.append( Label(self.utility, text=str(p.state.get())))
        self.checkbox.append(Checkbutton(self.utility,text=p.name ,variable=p.state,onvalue=1,offvalue=0,command=lambda m=p, n=i: self.cb(m,n)))
        self.checkbox[i].pack(anchor="w")
        self.Rname=None

#Fenetre pour nommer les robots et choisir leur directions de départs-----------------------------------------------------------------
    def popup(self):
        top=self.top=Toplevel(self.utility)
        self.top.title("Robot Configuration")
        self.l=Label(top,text="Veuilliez rentrer le nom de votre Robot")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.var = StringVar(top,"L")
        self.var2 = StringVar(top,"L")
        self.lD=Label(top,text="Veuilliez choisir la direction de départ votre Robot")
        self.lD.pack()
        Radiobutton(top, text = "Left", variable=self.var, value = 'L').pack(anchor="w")
        Radiobutton(top, text = "Right", variable=self.var, value = 'R').pack(anchor="w")
        Radiobutton(top, text = "Up", variable=self.var, value ="U").pack(anchor="w")
        Radiobutton(top, text = "Down", variable=self.var, value = "D").pack(anchor="w")
        self.lE=Label(top,text="Veuilliez choisir la direction d'arrivée votre Robot")
        self.lE.pack()
        Radiobutton(top, text = "Left", variable=self.var2, value = "L").pack(anchor="w")
        Radiobutton(top, text = "Right", variable=self.var2, value = "R").pack(anchor="w")
        Radiobutton(top, text = "Up", variable=self.var2, value ="U").pack(anchor="w")
        Radiobutton(top, text = "Down", variable=self.var2, value = "D").pack(anchor="w")
        self.b=Button(top,text='Ok',command=self.cleanupB)
        self.b.pack()
        top.bind('<Return>', self.cleanup)
    def cleanup(self,event):
        self.Rname=self.e.get()
        for i,p in enumerate(self.robots):
            if p.name==self.Rname:
                self.danger(self.top,"Le nom du Robot est déjà pris. Veuilliez en choisir un autre")
                self.window.wait_window(self.attention)
                self.buttonactive2=True
                self.Rname=None
        if self.buttonactive2==False:
            self.top.destroy()
        else:
            self.buttonactive2=False
    def cleanupB(self):
        self.Rname=self.e.get()
        for i,p in enumerate(self.robots):
            if p.name==self.Rname:
                self.danger(self.top,"Le nom du Robot est déjà pris. Veuilliez en choisir un autre")
                self.window.wait_window(self.attention)
                self.buttonactive2=True
                self.Rname=None
        if self.buttonactive2==False:
            self.top.destroy()
        else:
            self.buttonactive2=False

	# def sendRobotsMsgs(self) :
    #     try:
    #         print("master")
    #         for robot in self.robots :
    #             robotMsg = robot.createMsg()
    #             self.masterPub.publish(robotMsg)
    #     except rospy.ROSInterruptException:
    #         pass
#Supprimer un robot ----------------------------------------------------------------------------------------------------------------------------
                    ## DEBUG: Recalculer les chemins à la suppression

    def deleteRobot(self):
        if self.buttonactive==False:
            self.buttonactive=True
            self.listbox = Listbox(self.utility)
            for i,p in enumerate(self.robots):
                self.listbox.insert(END,p.name)
            self.listbox.pack()

            self.blistbox = Button(self.utility, text="Supprimer le robot",
               command=self.removingRobot)
            self.blistbox.pack()

            self.bcancel= Button(self.utility, text="Annuler",
               command=self.cancel)
            self.bcancel.pack()

        else:
            pass
    def removingRobot(self):
        item = self.listbox.curselection()
        value= self.listbox.get(item[0])
        for nbA,p in enumerate(self.robots):
            if value==p.name:
                #remettons tout à 0
                xc , yc = p.start.x , p.start.y
                cello=self.grille.getCell(xc,yc)
                self.grille.chgCell(xc,yc,".")
                self.can.delete(cello.display_txt)
                self.grille.chgTxt(xc,yc," ")
                self.grille.setCell(cello)
                print("Disp ",cello.typeC,"x ",xc," y ",yc," node.txt ",cello.txt)
                self.reset()
                xc , yc = p.goal.x , p.goal.y
                cello=self.grille.getCell(xc,yc)
                self.grille.chgCell(xc,yc,".")
                self.grille.chgTxt(xc,yc," ")
                self.grille.setCell(cello)
                print("Disp ",cello.typeC,"x ",xc," y ",yc," node.txt ",cello.txt)
                self.can.delete(cello.display_txt)
                self.reset()
                #supprimons mtn
                for num,robi in enumerate(self.robots):
                    self.checkbox[0].pack_forget()
                    del self.checkbox[0]
                self.checkbox=[]
                del self.robots[nbA]
                del self.paths
                self.paths=[]


                print ("List des robots",self.robots)
                print("List des paths", self.paths)

                coor = Coordination(self.robots)

                for nbr,bot in enumerate(self.robots):
                    check , node = coor.validatePath(bot)
                    if node:
                        node.changeType("?")
                        self.grille.setCell(node)
                        newRobot.path=self.astar.findPath(bot.start,bot.End)
                        self.paths.append(bot.path)
                        node.changeType(".")
                        self.grille.setCell(node)
                        check , node = coor.validatePath(bot)

                    bot.setTime()
                    self.afficher_chemin(bot,nbr)
                self.nbR=len(self.robots)
            else:
                pass
        self.cancel()

    def cancel(self):
        self.listbox.delete(0, END)
        self.listbox.pack_forget()
        self.blistbox.pack_forget()
        self.bcancel.pack_forget()
        self.buttonactive=False


#Message d'erreur---------------------------------------------------------------------------
    def danger(self,app,strg):
        self.attention=Toplevel(app)
        self.attention.title("ATTENTION")
        self.txtAttention=Label(self.attention,text=strg)
        self.txtAttention.pack()
        self.bAttention=Button(self.attention,text='Ok',command=self.destroyDanger)
        self.bAttention.pack()
    def destroyDanger(self):
        self.attention.destroy()


#Ajouter un obstacle-------------------------------------------------------------------------
    def addObstacle(self,event):
        xc , yc = int(event.x/self.boxSide) , int(event.y/self.boxSide)
        cello=self.grille.getCell(xc,yc)
        if cello.typeC=="?":
            self.danger(self.can,"Vous avez séléctioné de mettre un obstacle sur un obstacle, pourquoi voulez-vous faire ceci?")
            self.window.wait_window(self.attention)
        elif cello.typeC=="G" or cello.typeC=="S" :
            self.danger(self.can,"Vous avez séléctioné un obstacle sur une position spécifique de robots")
            self.window.wait_window(self.attention)
        else:
            self.grille.chgCell(xc,yc,"?")
            self.reset()


    def transition_obstacle(self,Canvas):
        self.callbutton=self.can.bind("<ButtonPress>",self.addObstacle)


#Retirer un obstacle-------------------------------------------------------------------------------
    def deleteObstacle(self,event):
        xc , yc = int(event.x/self.boxSide) , int(event.y/self.boxSide)
        cello=self.grille.getCell(xc,yc)
        if cello.typeC==".":
            self.danger(self.can,"Il n'y a pas d'obstacle ici. Séléctionnez un autre emplacement")
            self.window.wait_window(self.attention)
        elif cello.typeC=="G" or cello.typeC=="S" :
            self.danger(self.can,"C'est une position spécifique de robots, il n'y a pas d'obstacle ici")
            self.window.wait_window(self.attention)
        else:
            self.grille.chgCell(xc,yc,".")
            for typeC in self.dic:
                self.colorType(typeC,self.dic[typeC])


    def transition_deleteObstacle(self,Canvas):
        self.callbutton=self.can.bind("<ButtonPress>",self.deleteObstacle)
