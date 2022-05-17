
from pickle import TRUE
import sys
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTextEdit
from PyQt5.QtGui import QFont
from graph import Graph
from algorithms import Algorithms

DISPLAY_TEXT = 'This application is a visualiztion of breath first search(BFS), '\
                  'depth first search(DFS) and dijkstra\'s algorithm. Both BFS and '\
                  'dijkstra\'s algortihm are implemented to return the shortest path, '\
                  'DFS does not guarantee this.\n\n'\
                  'Start by setting the start position and then the end position. Then you can click any button '\
                  'if you want to deactivate it(disconnect from the graph). You can select the algorithm '\
                  'to run in the algorithm drop down menu and hard reset or reset to start over from the drop down '\
                  'command menu\n\n'\
                  'Hard Reset - resets everything in the graph.\n\n'\
                  'Reset - resets the graph but keeps the start position and end position as well as '\
                      'the deactivated vertices.'

class MaindWindow(QMainWindow):
    def __init__(self, posX, posY, parent=None):
        super().__init__()
        self.graph = Graph(self, 20, 30)
        self.move(int(posX * 0.3), int(posY * 0.4))
        self.__reset = True
        self.setCentralWidget(self.graph)
        self.__createMenuBar()
        self.__instructions(posX, posY)

    def __instructions(self, posX, posY):
        width = 500
        height = 500
        dialog = QDialog(self)

        dialog.setModal(True)
        dialog.move(int(posX * 0.7), int(posY * 0.5))
        dialog.resize(width, height)

        textBox = QTextEdit(dialog)
        textBox.setReadOnly(True)
        textBox.setLineWrapMode(True)
        textBox.setFixedWidth(width)
        textBox.setFixedHeight(height)
        textBox.setAlignment(Qt.AlignLeft)
        textBox.setPlainText(DISPLAY_TEXT)
        textBox.setFont(QFont('Times', 22))
        dialog.show()

    def __createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        
        commandMenu = menuBar.addMenu(" &Command")
        commandMenu.addAction("reset", self.__resetBoard)
        commandMenu.addAction("hardReset", self.__hardResetBoard)

        algorithmMenu = menuBar.addMenu(" &Graph Algorithm")
        algorithmMenu.addAction("Breadth First Search", self.__runBFS)
        algorithmMenu.addAction("Depth First Search", self.__runDFS)
        algorithmMenu.addAction("Dijkstra's Algortihm", self.__runDijkstra)

    def __hardResetBoard(self):
        self.__reset = True
        Graph.startPosition = None
        Graph.endPosition = None
        Graph.setWall = False
        vertices = self.graph.getVertices()
        for vertex in vertices:
            vertex.hardReset()

    def __resetBoard(self):
        self.__reset = True
        vertices = self.graph.getVertices()
        for vertex in vertices:
            vertex.reset()

    def __runBFS(self):
        if self.__reset == False: 
            return
        self.__threadSetUp()
        self.thread.started.connect(self.algorithmThread.breadthFirstSearch)
        self.__run()
    
    def __runDFS(self):
        if self.__reset == False: 
            return
        self.__threadSetUp()
        self.thread.started.connect(self.algorithmThread.depthFirstSearch)
        self.__run()

    def __runDijkstra(self):
        if self.__reset == False: 
            return
        self.__threadSetUp()
        self.thread.started.connect(self.algorithmThread.dijkstra)
        self.__run()

    def __threadSetUp(self):
        self.thread = QThread()
        self.algorithmThread = Algorithms(self.graph.getVertices())
        self.algorithmThread.moveToThread(self.thread)

    def __run(self):
        self.algorithmThread.finished.connect(self.thread.quit)
        self.algorithmThread.finished.connect(self.algorithmThread.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.algorithmThread.markVisited.connect(self.__markVisited)
        self.algorithmThread.color.connect(self.__color)
        self.thread.start()
        self.__reset = False

    def __markVisited(self, vertex):
        vertex.markVisited()

    def __color(self, vertex):
        vertex.pathColor()

app = QApplication(sys.argv)
posX = app.desktop().availableGeometry().center().x()
posY = app.desktop().availableGeometry().center().y()

window = MaindWindow(posX, posY)
window.show()
app.exec()