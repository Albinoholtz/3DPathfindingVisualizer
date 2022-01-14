"""
Annealing algorithm that uses all nodes around the greedy solution to find a better way of doing the path
@author: Gwen Hardwick
"""

# origonal greedy algorithm, only difference is accepting a past path and taking in the already selected points for the start and end
class greedyAlg():
    # initializes the algorithm, finding the starting and ending points as well as the screen/map to find a path along
    def __init__(self, playscreen, endX, endY, startX, startY, path):
        self.screen = playscreen
        self.currentY = startY
        self.currentX = startX
        self.endingY = endY
        self.endingX = endX
        self.path = path

    # finds the cheapest step from the current location either up, down, left, or right
    def cheapestStep(self):
        costs = [100, 100, 100, 100]
        viableOptions = ["u", "d", "l", "r"]

        # saves all of the costs as what they actually are
        if self.currentY-1 >= 0 and self.currentY-1 < len(self.screen):
            if [self.currentX, self.currentY-1] in self.path:
                costs[0] = 100
            else:
                costs[0] = self.screen[self.currentX][self.currentY-1]

        if self.currentY+1 >= 0 and self.currentY+1 < len(self.screen):
            if [self.currentX, self.currentY+1] in self.path:
                costs[1] = 100
            else:
                costs[1] = self.screen[self.currentX][self.currentY+1]

        if self.currentX-1 >= 0 and self.currentX-1 < len(self.screen):
            if [self.currentX-1, self.currentY] in self.path:
                costs[2] = 100
            else:
                costs[2] = self.screen[self.currentX-1][self.currentY]

        if self.currentX+1 >= 0 and self.currentX+1 < len(self.screen):
            if [self.currentX+1, self.currentY] in self.path:
                costs[3] = 100
            else:
                costs[3] = self.screen[self.currentX+1][self.currentY]

        # finds the very smallest cost, removes the rest, puts in placeholder numbers for walls, end, and start
        smallestCost = 100
        index = 0
        while index < len(costs):
            if costs[index] == 'e':
                costs[index] = -100
            elif costs[index] == 'w':
                costs[index] = 99999
            elif costs[index] == 's':
                costs[index] = 100
            if int(costs[index]) < int(smallestCost):
                smallestCost = costs[index]
            index += 1
        # removes the options and costs if they are more expensive than the cheapest
        index = 0
        iterations = 4
        while index < iterations:
            if costs[index] > smallestCost:
                viableOptions.pop(index)
                costs.pop(index)
                iterations -= 1
            else:
                index += 1
        # if there are multiple options with the same cost, pick the one that gets you closer to the end
        if "u" in viableOptions and "d" in viableOptions:
            if self.currentY > self.endingY:
                viableOptions.remove("d")
            else:
                viableOptions.remove("u")
        if "l" in viableOptions and "r" in viableOptions:
            if self.currentX > self.endingX:
                viableOptions.remove("r")
            else:
                viableOptions.remove("l")
        # if there still more than one options, look at which needs more change, x or y, remove accordingly
        if len(viableOptions) > 1:
            difX = self.currentX-self.endingX
            if difX < 0:
                difX = -difX
                if "u" in viableOptions:
                    viableOptions.remove("u")
        if len(viableOptions) > 1:
            difY = self.currentY-self.endingY
            if difY < 0:
                difY = -difY
                if "l" in viableOptions:
                    viableOptions.remove("l")
        if len(viableOptions) > 1:
            if difX > difY:
                if "u" in viableOptions:
                    viableOptions.remove("u")
                elif "d" in viableOptions:
                    viableOptions.remove("d")
            else:
                if "l" in viableOptions:
                    viableOptions.remove("l")
                elif "r" in viableOptions:
                    viableOptions.remove("r")
        # return a direction, either "u" "d" "l" or "r"
        return viableOptions[0]

    # the full greedy algorithm function, uses the other methods to find a path from the start to the end
    def greedyAlg(self):
        looper = 0  # new looping varible. If the greedy algorithm gets stuck in a loop that runs for over 200 times, give up on the path
        self.path.append([self.currentX, self.currentY])
        try:
            # while the path hasn't reached the endpoint, find the next cheapest place to go and update the location
            while (self.currentY != self.endingY or self.currentX != self.endingX) and looper < 200:
                looper += 1
                direc = self.cheapestStep()
                if direc == "u":
                    self.currentY = self.currentY-1
                elif direc == "d":
                    self.currentY = self.currentY+1
                elif direc == "r":
                    self.currentX = self.currentX+1
                else:
                    self.currentX = self.currentX-1

                self.path.append([self.currentX, self.currentY])
        except IndexError:
            return
        if looper >= 200:
            return
        return self.path

# the algorithm for the annealing
class AnnealingAlg():
    # initializer for the annealing. Saves the 2d array, finds the start and end points,
    def __init__(self, playscreen):
        self.screen = playscreen
        self.startingY = self.findValue('s', True, self.screen)
        self.startingX = self.findValue('s', False, self.screen)
        self.endingY = self.findValue('e', False, self.screen)
        self.endingX = self.findValue('e', True, self.screen)
        self.paths = []

    # finds a spicific location of a value using the algorthm, value wanted, if you want the x value or the y, and the screen
    def findValue(self, value, wantX, screen):
        indexX = 0
        indexY = 0
        while indexY < len(self.screen):
            while indexX < len(self.screen):
                if(screen[indexY][indexX] == value):
                    if(wantX):
                        return indexX
                    return indexY
                indexX += 1
            indexY += 1
            indexX = 0
        return -1

    # returns the cost, using a method that the only thing that matters is what the value of the element is (going from a 50 node to a 5 node costs 5, going from a -17 to a 10 is 10)
    def getCost(self, path):
        total = 0
        steps = 1
        while steps < len(path)-1:
            cost = self.screen[path[steps][0]][path[steps][1]]
            if cost == 'e':
                cost = 0
            elif cost == 's':
                cost = 0
            elif cost == 'w':
                cost = 999999999999999999999999
            total += cost
            steps += 1
        return total

    # figures out which places around a specific element are viable options, so not walls and within the 2d array
    def viableOptions(self, currentStep, pastPath):
        options = []
        x = currentStep[0]
        y = currentStep[1]
        if y-1 >= 0 and y-1 < len(self.screen):
            if self.screen[x][y-1] != 0 and [x, y-1] not in pastPath:
                options.append([x, y-1])
        if y+1 >= 0 and y+1 < len(self.screen):
            if self.screen[x][y+1] != 0 and [x, y+1] not in pastPath:
                options.append([x, y+1])
        if x-1 >= 0 and x-1 < len(self.screen[0]):
            if self.screen[x-1][y] != 0 and [x-1, y] not in pastPath:
                options.append([x-1, y])
        if x+1 >= 0 and x+1 < len(self.screen[0]):
            if self.screen[x+1][y] != 0 and [x+1, y] not in pastPath:
                options.append([x+1, y])
        return options

    # from a path, iterates off one step to try and find another
    def getAllStepsOff(self, path):
        index = 0
        counter = 1
        currentStep = path[index]
        pastPath = [path[index]]
        # while not at the
        while currentStep is not [self.endingX, self.endingY] and index < len(path):
            options = self.viableOptions(currentStep, pastPath)
            for i in options:
                greedy = greedyAlg(self.screen, self.endingX,
                                   self.endingY, i[0], i[1], pastPath)
                newpath = greedy.greedyAlg()
                pastPath = [path[0]]
                counter = 1
                while counter <= index:
                    pastPath.append(path[counter])
                    counter += 1
                if newpath is not None:
                    step = 0
                    while step < len(newpath):
                        if newpath[step] not in pastPath:
                            newpath[step] = [i[0], i[1]]
                            step = len(newpath)
                        else:
                            step += 1
                    self.paths.append(newpath)
            pastPath.append(path[index])
            index += 1
            if (index < len(path)):
                currentStep = path[index]

    # full annealing algorithm method, find the greedy solution and checks each step
    def annealingAlg(self):
        greedy = greedyAlg(self.screen, self.endingY,
                           self.endingX, self.startingX, self.startingY, [])
        self.paths = [greedy.greedyAlg()]
        self.getAllStepsOff(self.paths[0])
        bestCost = self.getCost(self.paths[0])
        bestPath = self.paths[0]
        badPaths = []

        for i in self.paths:
            if i[len(i)-1] != [self.endingY, self.endingX]:
                badPaths.append(i)
        for i in self.paths:
            if i not in badPaths and self.getCost(i) <= bestCost:
                bestPath = i
                bestCost = self.getCost(i)
        return bestPath
