class Grille:

    def __init__(self,r,c):
        self.nRows = r
        self.nColumns = c
        self.plan = []

        for i in range(c):
            self.plan.append([])
            for j in range(r):
                self.plan[i].append(Node(i,j))

    def chgNode(self,x,y,typeN):
        self.plan[x][y].changeType(typeN)


    def findVoisins(self,node, obstacle = "false",range = 1):
        voisins = []
        X = node.x
        Y = node.y

        voisin = self.getNode(X+range,Y)
        if not voisin.isObstacle() or obstacle=="true":
            voisins.append(voisin)
        voisin = self.getNode(X,Y+range)
        if not voisin.isObstacle()or obstacle=="true":
            voisins.append(voisin)
        voisin = self.getNode(X-range,Y)
        if not voisin.isObstacle()or obstacle=="true":
            voisins.append(voisin)
        voisin = self.getNode(X,Y-range)
        if not voisin.isObstacle()or obstacle=="true":
            voisins.append(voisin)

        return voisins


    def getCarre(self,pos,l = 0):
        carre= []

        for i in range(2*l+1)
            carre.append(self.getNode(pos.x-l+i,pos.y-l).copy())
            carre.append(self.getNode(pos.x-l+i,pos.y+l).copy())

        for i in range(2*(l-1)+2):
            carre.append(self.getNode(pos.x-l,pos.y-l+i).copy())
            carre.append(self.getNode(pos.x+l,pos.y-l+i).copy())

        #sorted(carre, key= lambda Node: Node.dist(pos))
        return carre


    def getNode(self,x,y):
        #print("Get Node :",repr(self.plan[y][x]),file=sys.stderr)
        if x < 0 or x >=self.nColumns or y<0 or y>=self.nRows:
            print("Out of boundary",file=sys.stderr)
            return
        return self.plan[x][y]

    def resetNodes(self):
        for r in self.plan:
            for c in r:
                c.reset()




    def chgRow(self,i,row):
        #print("New row : ",row,file=sys.stderr)
        for j,node in enumerate(row):
            self.chgNode(j,i,node)



    def __repr__(self):
        toPrint = []
        for j in range(self.nRows):
            toPrint.append("")
        for column in self.plan:
            for i,node in enumerate(column):
                    toPrint[i] += str(node)+" "

        returnPrint  ="  "

        for i in range(self.nColumns):
            if(len(str(i))<2):
                returnPrint+=" "
            returnPrint += str(i)

        returnPrint += '\n'

        for i,string in enumerate(toPrint):
            if(len(str(i))<2):
                returnPrint += " "
            returnPrint += str(i)+" "+string+"\n"

        return returnPrint
