
import queue
from queue import PriorityQueue
from time import sleep
from graph import Vertex, Graph
from PyQt5.QtCore import QObject, pyqtSignal

class Algorithms(QObject):
    finished = pyqtSignal()
    markVisited = pyqtSignal(Vertex)
    color = pyqtSignal(Vertex)

    def __init__(self, graph):
        super().__init__()
        self.__graph = graph

    def breadthFirstSearch(self):
        aQueue = queue.Queue()
        startVertex = self.__graph[Graph.startPosition]
        endVertex = self.__graph[Graph.endPosition]
        aQueue.put(startVertex)
        currVertex = None

        while currVertex != endVertex:
            currVertex = aQueue.get()

            if not currVertex.getVisited():
                sleep(0.0075)
                self.markVisited.emit(currVertex)

                for position in currVertex.getAdjacentVertices():
                    nextVertex = self.__graph[position]
                    
                    if not nextVertex.getVisited() and nextVertex.getActive():
                        aQueue.put(nextVertex)
                        nextVertex.setPrevious(currVertex)

        path = []
        while currVertex != startVertex:
            path.append(currVertex)
            currVertex = currVertex.getPrevious()
        path.append(currVertex)

        for vertex in path:
            self.color.emit(vertex)

        self.finished.emit()



    def depthFirstSearch(self):
        stack = []
        startVertex = self.__graph[Graph.startPosition]
        endVertex = self.__graph[Graph.endPosition]
        stack.append(startVertex)
        currVertex = None

        while currVertex != endVertex:
            currVertex = stack.pop()
            
            if not currVertex.getVisited():
                sleep(0.025)
                self.markVisited.emit(currVertex)

                for position in currVertex.getAdjacentVertices():
                    nextVertex = self.__graph[position]

                    if not nextVertex.getVisited() and nextVertex.getActive():
                        stack.append(nextVertex)
                        nextVertex.setPrevious(currVertex)

        path = []
        while currVertex != startVertex:
            path.append(currVertex)
            currVertex = currVertex.getPrevious()
        path.append(currVertex)

        for vertex in path:
            self.color.emit(vertex)

        self.finished.emit()



    def dijkstra(self):
        priorityQueue = PriorityQueue()
        startVertex = self.__graph[Graph.startPosition]
        endVertex = self.__graph[Graph.endPosition]
        
        for vertex in self.__graph:
            vertex.setDistance(100000)
        startVertex.setDistance(0)

        priorityQueue.put((0, startVertex))
        currVertex = None

        while currVertex != endVertex:
            currTuple = priorityQueue.get()
            currVertex = currTuple[1]

            if not currVertex.getVisited():
                sleep(0.0075)
                self.markVisited.emit(currVertex)

                for position in currVertex.getAdjacentVertices():
                    nextVertex = self.__graph[position]

                    if not nextVertex.getVisited() and nextVertex.getActive():
                        totalDistance = currTuple[0] + 1

                        if totalDistance < nextVertex.getDistance():
                            priorityQueue.put((totalDistance, nextVertex))
                            nextVertex.setDistance(totalDistance)
                            nextVertex.setPrevious(currVertex)

                for position in currVertex.getDiagonalVertices():
                    nextVertex = self.__graph[position]

                    if not nextVertex.getVisited() and nextVertex.getActive():
                        totalDistance = currTuple[0] + 1.4

                        if ( totalDistance < nextVertex.getDistance()):
                            priorityQueue.put((totalDistance, nextVertex))
                            nextVertex.setDistance(totalDistance)
                            nextVertex.setPrevious(currVertex)


        path = []
        while currVertex != startVertex:
            path.append(currVertex)
            currVertex = currVertex.getPrevious()
        path.append(currVertex)

        for vertex in path:
            self.color.emit(vertex)

        self.finished.emit()