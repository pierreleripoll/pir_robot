from tkinter import *
def envoyercoordonnees(event):
    x,y=event.x-event.x%40,event.y-event.y%40
    can.create_rectangle(x, y, x+40, y+40, fill='red')
def affichage(Grille):

    nbreDeCasesParLigne=Grille.nRows
    hauteur=512
    largeur=512
    rempl=hauteur/nbreDeCasesParLigne

    fen=Tk()
    can=Canvas(fen, width=largeur, height=hauteur, bg='ivory')
    #can.bind("<Button-1>", envoyercoordonnees)
    can.pack()
    bstop=Button(fen, text='Fermer la fenêtre', command=fen.destroy)
    bstop.pack()
    for c in range(nbreDeCasesParLigne):
                can.create_line(c*rempl, 0,c*rempl,hauteur)
                can.create_line(0,c*rempl,largeur,c*rempl)

    fen.mainloop()
