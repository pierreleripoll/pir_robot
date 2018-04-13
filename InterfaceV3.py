from tkinter import *



class Affichage:

    def __init__(self,Grille):
        self.nbreDeCasesParLigne=Grille.nRows
        self.hauteur=512
        self.largeur=512
        rempl=self.hauteur/self.nbreDeCasesParLigne
        self.grille = Grille;
        self.fen=Tk()
        self.can=Canvas(self.fen, width=self.largeur, height=self.hauteur, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.fen, text='Fermer la fenêtre', command=self.fen.destroy)
        self.bstop.pack()
        for c in range(self.nbreDeCasesParLigne):
                    self.can.create_line(c*rempl, 0,c*rempl,self.hauteur)
                    self.can.create_line(0,c*rempl,self.largeur,c*rempl)

    def chgColorType(self,typeC,color):
        for column in self.grille.plan:
            for node in column:
                if node.typeN == typeC:
                    self.affNode(node,color)

    def affNode(self,Node, color = "red"):
        rempl=self.hauteur/self.nbreDeCasesParLigne
        x=Node.x*rempl
        y=Node.y*rempl
        self.can.create_rectangle(x,y,x+rempl,y+rempl,fill=color)

    def affChemin(self,path,color = None):
        for node in path:
            if color :
                self.affNode(node,color)
            else :
                self.affNode(node)
