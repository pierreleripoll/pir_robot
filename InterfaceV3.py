from tkinter import *



class Affichage:

    def __init__(self,Grille):
        self.nbreDeCasesParLigne=Grille.nRows
        self.hauteur=512
        self.largeur=512
        rempl=self.hauteur/self.nbreDeCasesParLigne

        self.fen=Tk()
        self.can=Canvas(self.fen, width=self.largeur, height=self.hauteur, bg='ivory')
        self.can.pack()
        self.bstop=Button(self.fen, text='Fermer la fenêtre', command=self.fen.destroy)
        self.bstop.pack()
        for c in range(self.nbreDeCasesParLigne):
                    self.can.create_line(c*rempl, 0,c*rempl,self.hauteur)
                    self.can.create_line(0,c*rempl,self.largeur,c*rempl)

    def affNode(self,Node):
        x=Node.x
        y=Node.y
        rempl=self.hauteur/self.nbreDeCasesParLigne
        self.can.create_rectangle(x,y,x+rempl,y+rempl,fill='red')
