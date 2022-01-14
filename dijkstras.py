"""
Implementation of dijkstra's algorithm
@author: William Holtz
"""

import math
import heapq

class PQueue:

    def __init__(self):
        self.values = {}
        self.heap = []

    # pushes to the priority queue
    # if an obj already exists in the queue, its priority is updated and a new
    # updated entry is added to the heap
    def push(self, obj, priority, prev):
        heapq.heappush(self.heap, (priority, obj, prev))
        self.values[obj] = priority

    # pops from the priority queue
    # if an object doesn't exist in the values list, returns none, if it does
    # exists, but its value doesn't, m
    def pop(self):
        popped = heapq.heappop(self.heap)
        if popped == None or popped[1] not in self.values:
            return None
        while self.values[popped[1]] != popped[0]:
            if not self.heap:
                return None
            popped = heapq.heappop(self.heap)
        self.values.pop(popped[1])
        return popped

# A class structure used to pathfind a 2D array for our project
class DijkstrasAlg:

    def __init__(self, array):
        self.array = array
        self.start = self.findValue('s')
        self.end = self.findValue('e')
        self.path = []

    # finds a spicific location of a value using the algorthm, vlue wanted, if
    # you want the x value or the y, and the array
    def findValue(self, value):
        row = 0
        col = 0
        while row < len(self.array):
            while col < len(self.array[0]):
                if(self.array[row][col] == value):
                    return row,col
                col += 1
            row += 1
            col = 0
        return -1

    # helper method to obtain the neighbors of a coordinate in our array that
    # isn't a wall
    def getNeighborsForDij(self,row,col):
        neighbors = []
        if row > 0:
            if self.array[row-1][col] != "w":
                neighbors.append((row-1,col))
        if row < len(self.array) - 1:
            if self.array[row+1][col] != "w":
                neighbors.append((row+1,col))
        if col > 0:
            if self.array[row][col-1] != "w":
                neighbors.append((row,col-1))
        if col < len(self.array[0]) - 1:
            if self.array[row][col+1] != "w":
                neighbors.append((row,col+1))
        return neighbors

    # finds the cost to travel from p1 to p2 on the array
    def dist(self,p1,p2):
        val1 = self.array[p1[0]][p1[1]]
        val2 = self.array[p2[0]][p2[1]]
        if val2 == "s" or val2 == "e":
        	val2 = 1
        return val2

    # returns a path from start to end, and a total cost of travel
    def dijkstras(self):
        pq = PQueue()
        addedToQ = [self.start]
        startRow, startCol = self.start
        toBeAdded = [[0, startRow, startCol, None]]
        inf = 9999999999999999
        # put all nodes into queue

        # add all nodes to priority queue with a default priority of infinity
        while toBeAdded:
            priority, row, col, prev = toBeAdded.pop()
            pq.push((row, col), priority, prev)
            inf += 1
            new = []
            neighboringPoints = self.getNeighborsForDij(row,col)
            for p in neighboringPoints:
                if p not in addedToQ:
                    new.append((inf, p[0], p[1], None))
                    addedToQ.append(p)
            toBeAdded = list(new + toBeAdded)

        # loop until the queue is empty
        enqueued = {}
        while pq.heap:
            curr = pq.pop() # curr = (priority, obj, prev)
            if curr == None:
                continue
            currNeighbors = self.getNeighborsForDij(curr[1][0],curr[1][1])
            for point in currNeighbors:
                if point in enqueued:
                    continue
                new_dist = curr[0] + self.dist(curr[1],point)
                if pq.values[point] > new_dist:
                    pq.push(point, new_dist, curr[1])
            enqueued[curr[1]] = (curr)
            if curr[1] == self.end:
            	break

        path = []
        end = enqueued[self.end]
        curr = end
        path = [self.end]

        # loop back from the end to start to get path
        while curr[1] != self.start:
            curr = enqueued[curr[2]]
            path = [curr[1]] + path
        # returns array of points traversed from start to end
        # returns cost of total traversal
        return path, end[0]
