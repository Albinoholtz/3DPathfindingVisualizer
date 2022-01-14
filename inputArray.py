"""
Implementation for the sandbox to draw and change map for pathfinding algorithm to traverse
@author: Moses Solomon
"""
import pygame
import numpy as np
import sys
import time

from greedy import *
from dijkstras import *
from annealing import AnnealingAlg
from visualizePath import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

# height of the grid of boxes
HEIGHT = 10

# width of the grid of boxes
WIDTH = 10

#number of pixels in each squares
STEP_SIZE = 40

# get the dimensions in pixels of the screen
SCREEN_HEIGHT = HEIGHT * STEP_SIZE
SCREEN_WIDTH = WIDTH * STEP_SIZE

# initialize our data 2d Array with 1s
data = [[1 for i in range(WIDTH)] for j in range(HEIGHT)]

# initialize whether a start and end point has been decided, and positions
start = False
end = False
start_pos = None
end_pos = None

global freezeCommands
freezeCommands = False
notOver = True
waitForKey = False

# Making a pygame display.
screen = pygame.display.set_mode((SCREEN_WIDTH+200,SCREEN_HEIGHT))
pygame.display.set_caption('PathFinder')
screen.fill(BLACK)


pygame.init()
# PyGame clock object.
clock = pygame.time.Clock()


# based on the value at each position in the graph, draw the appropriate image
def updateGrid():
    global start, end, data;
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # iterate through the data and draw appropriate rectangle
            # for all elevations
            if data[y][x] != 'w' and data[y][x] != 's' and data[y][x] != 'e':

                #draw white border for all squares
                rect = pygame.Rect(x*STEP_SIZE, y*STEP_SIZE, STEP_SIZE, STEP_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 5)

                #draw a slightly smaller black square over each square
                rect = pygame.Rect(x*STEP_SIZE, y*STEP_SIZE, STEP_SIZE-1, STEP_SIZE-1)
                pygame.draw.rect(screen, BLACK, rect, 0)

                font = pygame.font.Font('freesansbold.ttf', 25)
                # create a text surface object on which text is drawn on it.
                text = font.render(str(data[y][x]), True, WHITE)

                # create a rectangular object for the
                # text surface object
                textRect = text.get_rect()

                # set the center of the rectangular object.
                textRect.center = ((x*STEP_SIZE) + STEP_SIZE//2, (y*STEP_SIZE) + STEP_SIZE//2)
                # put the text onto the square
                screen.blit(text, textRect)

            # draw red square for wall
            if data[y][x] == 'w':
                rect = pygame.Rect(x*STEP_SIZE, y*STEP_SIZE, STEP_SIZE, STEP_SIZE)
                pygame.draw.rect(screen, RED, rect, 0)

            # draw green start position
            if data[y][x] == 's':
                rect = pygame.Rect(x*STEP_SIZE, y*STEP_SIZE, STEP_SIZE, STEP_SIZE)
                pygame.draw.rect(screen, (0, 255, 0), rect, 0)

            # draw blue end position
            if data[y][x] == 'e':
                rect = pygame.Rect(x*STEP_SIZE, y*STEP_SIZE, STEP_SIZE, STEP_SIZE)
                pygame.draw.rect(screen, (0, 0, 255), rect, 0)

# based on the command, update the value in 2d array
def updateSquare(command):
    global start, end, start_pos, end_pos;
    pos = pygame.mouse.get_pos()
    # rescales the mouse position so we can identify the specific square we are clicking
    x_update = int(pos[0]/STEP_SIZE)
    y_update = int(pos[1]/STEP_SIZE)

    # make sure you can only click on the grid
    if x_update > len(data[1]) - 1:
        return
    if y_update > len(data[0]) - 1:
        return

    # don't allow any walls, or start/end positions to be changed once they have been placed
    if data[y_update][x_update] != 'w' and data[y_update][x_update] != 's' and data[y_update][x_update] != 'e' and freezeCommands == False:
        if command == 'wall':
            data[y_update][x_update] = 'w'
        elif command == 'increase':
            data[y_update][x_update] += 1
        elif command == 'decrease':
            data[y_update][x_update] -= 1

        elif command == 'start' and start == False:
            data[y_update][x_update] = 's'

            # update that a start and end position have been chosen and store their positions globally
            start = True
            start_pos = (y_update, x_update)
        elif command == 'end' and end == False:
            data[y_update][x_update] = 'e'
            end = True
            end_pos = (y_update, x_update)
        print(pos)


# get all of the random values that are not 0 in a range
def randomData():
    random_values = []
    for i in range(-50, 0):
        random_values.append(i)
        random_values.append(abs(i))
    return random_values

"""
terrain elevation: pick peaks and smooth out the mountain tops
"""
def randomizeElevation():
    random_values = randomData()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # randomly choose from random values array as to still avoid choosing 0
            random_index = np.random.randint(0, len(random_values))
            if data[y][x] != 'w' and data[y][x] != 's' and data[y][x] != 'e':
                data[y][x] = random_values[random_index]


# based on the number pressed on the keyboard update the board
def usePremadeGraph(n):
    if not freezeCommands:
        if n == 1:
            data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 's', 1, 1, 1, 1, 1, 1, 1],
            [10, 10, 10, 10, 10, 10, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 10, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 10, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 10, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 10, 1, 1],
            [1, 1, 1, 1, 1, 1, 'e', 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]

        elif n == 2:
            data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 2, 6, 6],
            [1, 1, 1, 1, 1, 1, 1, 2, 6, 24],
            [1, 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 50],
            ['s', 10, 15, 20, 25, 20, 15, 10, 10, 'e'],
            [1, 2, 4, 6, 6, 10, 6, 6, 4, 2],
            [1, 1, 1, 2, 4, 3, 2, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
        elif n == 3:
            data = [
            [1, 1, 1, 1, 's', 1, 40, -1, -1, -1],
            [1, 1, 1, 1, 'w', 16, 33, 40, -1, -1],
            [1, 1, 1, 1, 'w', 10, 12, 26, 40, -1],
            [1, 1, 1, 1, 'w', 1, 10, 26, 40, 2],
            [1, 1, 1, 1, 'w', 1, 8, 24, 40, 2],
            [1, 1, 1, 1, 'w', 1, 6, 21, 35, 4],
            [1, 1, 1, 1, 'w', 1, 1, 1, 1, 'e'],
            [1, 1, 1, 1, 'w', 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]

        elif n == 4:
            data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 'w', 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 'w', 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 'w', 1, 1, 1],
            ['s', 1, 1, 1, 1, 1, 1, 'w', 1, 'e'],
            [1, 1, 1, 1, 1, 1, 'w', 1, 1, 1],
            [1, 1, 1, 1, 1, 'w', 1, 1, 1, 1],
            [1, 1, 1, 1, 'w', 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
        elif n == 5:
            # graph appears on screen as it appears below
            data = [
            ['s', 1, 1, 3, 4, 6, 8, 8, 6, 4],
            [1, 1, 2, 4, 16, 20, 16, 22, 10, 5],
            [0,'w', 10, 14, 20, 24, 20, 15, 1, -1],
            [10, 14, 15, 25, 30, 20, 10, 5,'w', -1],
            [1, 1, 1, 1, 23, 24, 22, 1, 1, 1],
            [10, 10, 10, 10,'w', 15, 6, 8, 15, 20],
            [20, 23, 30,'w', 40, 20, 14, 7, 12, 23],
            [40, 31, 14, 43, 50, 30,'w', 7, 7, 7],
            [40,'w', 30, 30, 40, 20,'w', 'w', 'w', 7],
            [0, 24, 22, 20, 20, 14, 'e', 7, 7, 7]
            ]

        return data

def printCommands():
    print("Hello! List of Useful Hotkeys:")
    print("S: Place starting position for the pathfinding algorithm")
    print("E: Place ending position for the pathfinding algorithm")
    print("P: Increase the elevation of square")
    print("O: Decrease the elevation of square")
    print("Left Mouse Button: Place impassable wall")
    print("R: randomize all of the remaining elevations on the map")
    print("1-5: Use premade graph")
    print("Return: save the graph and run the pathfinding algorithm")
    print("After selecting an algorithm: press p to step through the" +
    "pathfinding!")

printCommands()


def runInput():
    global notOver, data, freezeCommands, waitForKey
    # main function of the grid
    while True:
        #constantly update the grid
        if notOver:
            updateGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                printArray()
                print(start_pos)
                print(end_pos)
                sys.exit()
            # draw wall
            if event.type == pygame.MOUSEBUTTONDOWN:
                # initialize the first square on mouse down so once into new square,
                # then can call update square, shouldn't constantly run if in same squares
                updateSquare('wall')
            if event.type == pygame.KEYDOWN:
                #increase elevation of node
                if event.key == pygame.K_p:
                    updateSquare('increase')
                # decrease elevation of node
                if event.key == pygame.K_o:
                    updateSquare('decrease')
                # choose the starting and ending points for the algorithm
                # temporary solution because buttons suck
                if event.key == pygame.K_s:
                    updateSquare('start')
                if event.key == pygame.K_e:
                    updateSquare('end')
                if event.key == pygame.K_r:
                    randomizeElevation()
                if event.key == pygame.K_RETURN:
                    waitForKey = True
                    freezeCommands = True
                    print("save state and run algorithm")
                    print("press 7 to run the Greedy algorithm")
                    print("press 8 to run Dijkstra's algorithm")
                    print("press 9 to run the Annealing algorithm")
                if event.key == pygame.K_1:
                    data = usePremadeGraph(1)
                if event.key == pygame.K_2:
                    data = usePremadeGraph(2)
                if event.key == pygame.K_3:
                    data = usePremadeGraph(3)
                if event.key == pygame.K_4:
                    data = usePremadeGraph(4)
                if event.key == pygame.K_5:
                    data = usePremadeGraph(5)
                if event.key == pygame.K_7 and waitForKey == True:
                    greedy = GreedyAlg(data)
                    path = greedy.greedyAlg()
                    waitForKey = False
                    notOver = False
                    return data, path, "Greedy Alg."
                elif event.key == pygame.K_8 and waitForKey == True:
                    dijk = DijkstrasAlg(data)
                    path, cost = dijk.dijkstras()
                    waitForKey = False
                    notOver = False
                    return data, path, "Dijkstra's Alg."
                elif event.key == pygame.K_9 and waitForKey == True:
                    ann = AnnealingAlg(data)
                    path = ann.annealingAlg()
                    waitForKey = False
                    notOver = False,
                    # return the path so that the 3d representation can use it
                    return data, path, "Annealing Alg."
        pygame.display.update()

# main to run program
def main():
    inputArr, path, pathName = runInput()
    visualize(inputArr, path, pathName)

if __name__ == "__main__":
    main()
