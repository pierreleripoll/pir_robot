from tkinter import *
def envoyercoordonnees(event):
    x,y=event.x-event.x%40,event.y-event.y%40
    can.create_rectangle(x, y, x+40, y+40, fill='red')
fen=Tk()
can=Canvas(fen, width=320, height=320, bg='ivory')
can.bind("<Button-1>", envoyercoordonnees)
can.pack()
bstop=Button(fen, text='Fermer la fenêtre', command=fen.destroy)
bstop.pack()
for c in range(8):
            can.create_line(c*40, 0,c*40,320)
            can.create_line(0,c*40,320,c*40)

fen.mainloop()
