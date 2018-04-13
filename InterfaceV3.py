from tkinter import *





def affichage(Grille):
    nbreDeCasesParLigne=Grille.nRows
    hauteur=512
    largeur=512
    rempl=hauteur/nbreDeCasesParLigne

    fen=Tk()
    can=Canvas(fen, width=largeur, height=hauteur, bg='ivory')
    can.pack()
    bstop=Button(fen, text='Fermer la fenêtre', command=fen.destroy)
    bstop.pack()
    for c in range(nbreDeCasesParLigne):
                can.create_line(c*rempl, 0,c*rempl,hauteur)
                can.create_line(0,c*rempl,largeur,c*rempl)

    fen.mainloop()

def affChemin(Node,ajustage):
    x=Node.x
    y=Node.y
    rempl=ajustage
    can.create_rectangle(x,y,x+rempl,y+rempl,fill='red')
