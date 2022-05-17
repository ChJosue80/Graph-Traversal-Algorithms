
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy

GREEN = "QPushButton {backGround-color: rgb(102,204,102); border: 0}"
GREY = "QPushButton {backGround-color: rgb(128,128,128); border: 0}"
BLACK = "QPushButton {backGround-color: rgb(0,0,0); border: 0}"
BLUE = "QPushButton {background-color: rgb(0,102,204); border: 0}"

class Graph(QWidget):
    startPosition = None
    endPosition = None
    setWall = False

    def __init__(self, parent=None, rowSize=20, columnSize=20):
        super().__init__()
        self.__rowSize = rowSize
        self.__columnSize = columnSize
        self.__totalVertices = rowSize * columnSize
        self.__vertices = []
        self.__grid = QGridLayout(self)
        self.__createVertices()
        self.__createLayout()

    @staticmethod
    def func(vertex):
        position = vertex.getPosition()
        
        if Graph.setWall:
            vertex.setActive(not vertex.getActive())
        
        if Graph.startPosition != None:
            if Graph.endPosition == None:
                Graph.endPosition= position
                Graph.setWall = True
                vertex.setText("End")
                vertex.setStyleSheet(GREEN)
        else:
            Graph.startPosition = position
            vertex.setText("Start")
            vertex.setStyleSheet(GREEN)

    def getVertices(self):
        return self.__vertices

    def __createVertices(self):
        for position in range(self.__totalVertices):
            vertex = Vertex(position)
            self.__vertices.append(vertex)
            vertex.setAdjacentVertices(self.__totalVertices, self.__columnSize)
            vertex.setDiagonalVertices(self.__totalVertices, self.__columnSize)


    def __createLayout(self):
        for vertex in self.__vertices:
            row = vertex.getPosition() // self.__columnSize
            column = vertex.getPosition() % self.__columnSize
            self.__grid.addWidget(vertex, row, column)
        
        self.__grid.setHorizontalSpacing(5)
        self.__grid.setVerticalSpacing(5)
        self.setLayout(self.__grid)

class Vertex(QPushButton):
    def __init__(self, position, parent=None):
        super().__init__()
        self.__position = position
        self.__previous = None
        self.__visited = False
        self.__active = True
        self.__distance = None
        self.__adjacentVertices = []
        self.__diagonalVertices = []
        self.clicked.connect(lambda: Graph.func(self))
        self.__format()

    def __lt__(self, other):
        if self.__distance < other.getDistance():
            return self
        return other

    def getPosition(self): return self.__position
    
    def getVisited(self): return self.__visited

    def getActive(self): return self.__active

    def getPrevious(self): return self.__previous

    def getDistance(self): return self.__distance

    def getAdjacentVertices(self): return self.__adjacentVertices

    def getDiagonalVertices(self): return self.__diagonalVertices

    def setDistance(self, distance):
        self.__distance = distance

    def setPrevious(self, vertex):
        self.__previous = vertex

    def setActive(self, active):
        self.__active = active
        if active:
            self.setStyleSheet(GREY)
        else:
            self.setStyleSheet(BLACK)

    def setAdjacentVertices(self, totalVertices, columnSize):
        position = self.__position
        if (position >= columnSize): # check top
            self.__adjacentVertices.append(position - columnSize)
        if (position % columnSize != 0): # check left
            self.__adjacentVertices.append(position - 1)
        if (position < totalVertices - columnSize): # check bottom
            self.__adjacentVertices.append(position + columnSize)
        if (position % columnSize != 29): # check right
            self.__adjacentVertices.append(position + 1)

    def setDiagonalVertices(self, totalVertices, columnSize):
        position = self.__position
        if (position >= columnSize): # checks top
            if (position % columnSize != 0): # check left
                self.__diagonalVertices.append(position - columnSize - 1)
            if (position % columnSize != 29): # check right
                self.__diagonalVertices.append(position - columnSize + 1)
        if (position < totalVertices - columnSize): # check bottom
            if (position % columnSize != 0): # check left
                self.__diagonalVertices.append(position + columnSize - 1)
            if (position % columnSize != 29): # check right
                self.__diagonalVertices.append(position + columnSize + 1)

    def markVisited(self):
        self.__visited = True
        self.setStyleSheet(GREEN)

    def pathColor(self):
        self.setStyleSheet(BLUE)

    def hardReset(self):
        self.__previous = None
        self.__visited = False
        self.__active = True
        self.__distance = None
        self.setText("")
        self.setStyleSheet(GREY)

    def reset(self):
        self.__previous = None
        self.__visited = False
        self.__distance = None
        if self.__active:
            self.setStyleSheet(GREY)
        if self.__position == Graph.endPosition:
            self.setText("End")
            self.setStyleSheet(GREEN)
        if self.__position == Graph.startPosition:
            self.setText("Start")
            self.setStyleSheet(GREEN)
            
    def __format(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(GREY)