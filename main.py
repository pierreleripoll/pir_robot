
from node import Node
from grille import Grille
from astar import AStar

lab = Grille(30,30);
lab.setRect(15,15,10,2,".");
lab.setRect(15,15,2,10,".");
lab.setRect(20,15,2,10,".");
lab.setRect(15,22,10,2,".");
start = Node(15,20,"S");
goal = Node(20,15,"G");

lab.setNode(start);
lab.setNode(goal);

astar = AStar(lab)

path = astar.findPath(start,goal)
