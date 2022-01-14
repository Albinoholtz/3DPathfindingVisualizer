"""
Greedy algorithm, goes for the cheapest step until at the end
@author: Gwen Hardwick
"""


class GreedyAlg():
    # initializes the algorithm, finding the starting and ending points as well as the
    # screen/map to find a path along
    def __init__(self, playscreen):
        self.screen = playscreen
        self.currentY = self.findValue('s', False, self.screen)
        self.currentX = self.findValue('s', True, self.screen)
        self.endingY = self.findValue('e', False, self.screen)
        self.endingX = self.findValue('e', True, self.screen)
        self.path = []

    # finds a spicific location of a value using the algorthm, vlue wanted, if you want the
    # x value or the y, and the screen
    def findValue(self, value, wantX, screen):
        indexX = 0
        indexY = 0
        while indexY < len(self.screen):
            while indexX < len(self.screen):
                if(screen[indexX][indexY] == value):
                    if(wantX):
                        return indexX
                    return indexY
                indexX += 1
            indexY += 1
            indexX = 0
        return -1


    # finds the cheapest step from the current location either up, down, left, or right
    def cheapestStep(self):
        costs = [100, 100, 100, 100]
        viableOptions = ["u", "d", "l", "r"]

        #saves all of the costs
        if self.currentY-1 >= 0 and self.currentY-1 < 10:
            if [self.currentX, self.currentY-1] in self.path:
                costs[0]=100
            else:
                costs[0] = self.screen[self.currentX][self.currentY-1]

        if self.currentY+1 >= 0 and self.currentY+1 < 10:
            if [self.currentX, self.currentY+1] in self.path:
                costs[1]=100
            else:
                costs[1] = self.screen[self.currentX][self.currentY+1]

        if self.currentX-1 >= 0 and self.currentX-1 < 10:
            if [self.currentX-1, self.currentY] in self.path:
                costs[2]=100
            else:
                costs[2] = self.screen[self.currentX-1][self.currentY]

        if self.currentX+1 >= 0 and self.currentX+1 < 10:
            if [self.currentX+1, self.currentY] in self.path:
                costs[3]=100
            else:
                costs[3] = self.screen[self.currentX+1][self.currentY]

        # finds the very smallest cost, removes the rest, assigns weights to make sure
        # the algorithm doesn't go through a wall and goes toward the end
        smallestCost = 100
        index = 0
        while index < len(costs):
            if costs[index]=='e':
                costs[index]=-100
            elif costs[index]=='w':
                costs[index]=99999
            elif costs[index]=='s':
                costs[index]=100
            if int(costs[index]) < int(smallestCost):
                smallestCost = costs[index]
            index += 1
        index = 0
        iterations = 4
        while index < iterations:
            if costs[index] > smallestCost:
                viableOptions.pop(index)
                costs.pop(index)
                iterations -= 1
            else:
                index += 1

        # if there are multiple options with the same cost, pick the one that gets you
        # closer to the end
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
        # if there are still more than one option, figure out which difference (x or y)
        # is bigger and go in that direction
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
        return viableOptions[0]

    # returns the cost, using a method that the only thing that matters
    # is what the value of the element is
    # (going from a 50 node to a 5 node costs 5, going from a -17 to a 10 is 10)
    def getCost(self):
        total = 0
        steps = 1
        while steps < len(self.path)-1:
            cost = self.screen[self.path[steps][0]][self.path[steps][1]]
            if cost == 'e':
                cost = 0
            elif cost == 's':
                cost = 0
            elif cost == 'w':
                cost = 999999999999999999999999
            total += cost
            steps += 1
        return total

    # the full greedy algorithm function, uses the other methods to find a path
    # from the start to the end
    def greedyAlg(self):
        self.path.append([self.currentX, self.currentY])
        while self.currentY != self.endingY or self.currentX != self.endingX:
            dir = self.cheapestStep()
            if dir == "u":
                self.currentY = self.currentY-1
            elif dir == "d":
                self.currentY = self.currentY+1
            elif dir == "r":
                self.currentX = self.currentX+1
            else:
                self.currentX = self.currentX-1

            self.path.append([self.currentX, self.currentY])

        return self.path
