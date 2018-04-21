from tkinter import *



class Display:

    def __init__(self,grille,dic = None):
        self.boxesPerRow=grille.nRows
        self.height=512
        self.width=512
        rempl=self.height/self.boxesPerRow
        self.grille = grille
        self.window=Tk()
        self.can=Canvas(self.window, width=self.width, height=self.height, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.window, text='Fermer la fenêtre', command=self.window.destroy)
        self.bstop.pack()
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

    def node(self,node, color):
        rempl=self.height/self.boxesPerRow
        x=node.x*rempl
        y=node.y*rempl
        if node.typeN == "S" or node.typeN == "G" :
            color = self.dic[node.typeN]
        rect = self.can.create_rectangle(x,y,x+rempl,y+rempl,fill=color)
        txt = self.can.create_text(x, y, text=node.txt, anchor="nw", width=rempl)
        self.can.tag_raise(txt)

    def dispPath(self,path,color):
        for node in path:
            self.node(node, color)
