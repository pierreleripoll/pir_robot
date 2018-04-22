from tkinter import *



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
            for typeN in dic:
                self.colorType(typeN,dic[typeN])

    def colorType(self,typeN,color):
        for column in self.grille.plan:
            for node in column:
                if node.typeN == typeN:
                    self.node(node,color)

    def showCase(self,event):
        rempl = self.height/self.boxesPerRow
        self.chaine.configure(text = "X =" + str(event.x) +", Y =" + str(event.y))
        xc , yc = int(event.x/rempl) , int(event.y/rempl)
        print("Case :",repr(self.grille.getNode(xc,yc)))

    def node(self,node, color):
        rempl=self.height/self.boxesPerRow
        x=node.x*rempl
        y=node.y*rempl
        color = self.dic[node.typeN]
        rect = self.can.create_rectangle(x,y,x+rempl,y+rempl,fill=color)
        if node.typeN == "S" or node.typeN == "G" :
            txt = self.can.create_text(x+rempl/2, y+rempl/2,fill="white",activefill="yellow", text=node.txt,  width=rempl)
            self.can.tag_raise(txt)


    def dispPath(self,path,color):
        for node in path:
            self.node(node, color)
