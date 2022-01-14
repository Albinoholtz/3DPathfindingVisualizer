"""
Implementation for 3D visualizer for a pathfinding environment and solution
@author: William Holtz
"""

import math
import pygame
import sys

# define constants
WHITE = (255, 255, 255)
BACKDROP = (149, 162, 207)
GREY = (110,110,110)
START_COLOR = (143, 185, 168)
END_COLOR = (241, 130, 141)
PATH = (234, 230, 182)
SIDE1 = (250,250,250)
SIDE2 = (230,230,230)
SIDE3 = (210,210,210)
SIDE4 = (190,190,190)
SIDE5 = (170,170,170)
SIDE6 = (30,30,50)
BLACK = (0, 0, 0)
# used to reduce speed of rotation
MOUSE_SCALAR = 1/200
# Our display will be square
SIDE_LENGTH = 600
CX = SIDE_LENGTH / 2
CY = SIDE_LENGTH / 2

# camera class has two main attributes, pos and rot
# self.pos = [x,y,z] where x,y,z are the coordinates of the camera
class Camera():

    def __init__(self, pos=[0,0,0], rot=[0,0]):
        self.pos = pos
        self.rot = rot
        self.SPEED_SCALAR = 1/8 # used to slow/hasten the camera's movement

    def cameraEvent(self, s, event, keys):
        # movement handling
        # e for up, q for down
        if keys[pygame.K_q]: self.pos[1] += 1 * s
        if keys[pygame.K_e]: self.pos[1] -= 1 * s

        # adjust movement to match rotation direction
        x,y = math.sin(self.rot[1]) * s, math.cos(self.rot[1]) * s
        # use w,a,s,d to move forward, left, back, right
        if keys[pygame.K_w]: self.pos[0] += x; self.pos[2] += y
        if keys[pygame.K_s]: self.pos[0] -= x; self.pos[2] -= y
        if keys[pygame.K_a]: self.pos[0] -= y; self.pos[2] += x
        if keys[pygame.K_d]: self.pos[0] += y; self.pos[2] -= x

        # handle mouse rotation
        if event.type == pygame.MOUSEMOTION:
            # get amount of mouse movement
            x,y = event.rel
            x = x * MOUSE_SCALAR
            y = y * MOUSE_SCALAR
            self.rot[0] += y
            self.rot[1] += x

# Box class used to represent boxes in 3D space
# Core attributes are verts, boxFaces, faceColors
class Box():

    # create a box instance
    # paramaters: xShift from x = 0, zShift from z = 0, height scalar of the box
    def __init__(self, xShift, zShift, height):
        boxVertices = [[-1,0,-1], [1,0,-1], [1,2,-1], [-1,2,-1],
        [-1,0,1], [1,0,1], [1,2,1], [-1,2,1]]
        for i in range(len(boxVertices)):
	           boxVertices[i][0] += xShift
	           boxVertices[i][2] += zShift
	           boxVertices[i][1] = (boxVertices[i][1] * 0.25 * -height)
        self.verts = boxVertices
        #faceInstructions
        self.boxFaces = [(3,7,6,2),(0,1,2,3),(4,5,6,7),(0,4,7,3),(1,5,6,2),(0,4,5,1)]
        self.faceColors = [SIDE1,SIDE2,SIDE3,SIDE4,SIDE5,SIDE6]

    # convert points in 3D space to 2D given a camera's perspective
    def get2DPoints(self, cam):
    	points2D = []
    	for x, y, z in self.verts:
    		# add to x y and z based on camera pos
    		x -= cam.pos[0]
    		y -= cam.pos[1]
    		z -= cam.pos[2]
    		# account for rotation
    		x, z = rotate2d((x, z), cam.rot[1])
    		y, z = rotate2d((y, z), cam.rot[0])
    		# check if z is behind camera
    		if z <= 0:
    			points2D.append((None,None))
    		else:
    			# adjust x and y based on z such that as z increases,
    			# x and y move towards center
    			zDimensionalAdjustment = SIDE_LENGTH / z
    			x = x * zDimensionalAdjustment
    			y = y * zDimensionalAdjustment
    			# add cy and cx to y and x so the object is drawn around center
    			points2D.append((int(x) + CX, int(y) + CY))
    	return points2D

    # find the average distance of a polygon with given vertices to camPos in 3D
    def distanceFaceToCam(faceVerts, camPos):
    	totalX = 0
    	totalY = 0
    	totalZ = 0
    	for x,y,z in faceVerts:
    		totalX += x
    		totalY += y
    		totalZ += z
    	x_dist = (totalX/4) - camPos[0]
    	y_dist = (totalY/4) - camPos[1]
    	z_dist = (totalZ/4) - camPos[2]
    	distance = ((x_dist**2) + (y_dist**2) + (z_dist**2))
    	return distance

    # returns: list of faces, face = (avg distance from camera, color, points)
    def getFaces(self, cam):
    	global reportRequested

    	faces = []
    	for i in range(len(self.boxFaces)):
    		faceVerts = []
    		faceVertsIn2D = []
    		points2D = self.get2DPoints(cam)
    		for j in range(4):
    			faceVerts.append(self.verts[self.boxFaces[i][j]])
    			faceVertsIn2D.append(points2D[self.boxFaces[i][j]])
    		distance = Box.distanceFaceToCam(faceVerts, cam.pos)
    		if (None,None) in faceVertsIn2D:
    			pass
    		else:
    			faces.append((distance, self.faceColors[i], faceVertsIn2D))
    	return faces

    # reset the boxes colors to default
    def resetColors(self):
    	self.faceColors = [SIDE1,SIDE2,SIDE3,SIDE4,SIDE5,SIDE6]

# rotation helper method
def rotate2d(pos, rad):
    x, y = pos
    s = math.sin(rad)
    c = math.cos(rad)
    return x*c - y*s, y*c + x*s

# color assignment helper method
def getPathColor(sideIndex):
	if sideIndex == 5:
	 return (171, 139, 123)
	color = list(PATH)
	for i in range(3):
		color[i] = color[i] - (20 * sideIndex)
	return tuple(color)

# visualize(input, path, steps)
# input: 2D input array consisting of heights as values. Will detect special
# characters "w","s","e" and make walls, starts, and ends correspondingly
# steps: array of points in consecutive order from start to fin. ex. point:
# [row, col]
def visualize(input, path, pathName):
    # initialize pygame components
    pygame.init()
    clock = pygame.time.Clock()
    # font
    font = pygame.font.SysFont(None, 24)

    # declare useful variables
    steps = path
    step = 0
    cam = Camera([0,0,-5 - len(input)])
    # create a surface on screen with proper size
    dis = pygame.display.set_mode((SIDE_LENGTH, SIDE_LENGTH))
    pygame.display.set_caption("3D Visualizer")
    # define a variable to control the main loop
    running = True


    # start by getting the minimum value in the input
    smallestVal = 1
    maxVal = 1
    for row in range(len(input)):
    	for col in range(len(input[row])):
    		if type(input[row][col]) == int and input[row][col] < smallestVal:
    			smallestVal = input[row][col]
    		if type(input[row][col]) == int and input[row][col] > maxVal:
    			maxVal = input[row][col]
    if maxVal != smallestVal:
    	heightScale = 10 / (maxVal - smallestVal)
    else:
    	heightScale = 1
    if heightScale >= 1:
    	heightScale = 1

    # begin creating boxes
    boxes = []
    rows = len(input)
    cols = len(input[0])
    for row in range(len(input)):
    	boxes.append([])
    	for col in range(len(input[row])):
    		xShift = 2 * (col - ( (cols - 1) / 2 ))
    		zShift = 2 * (row - ( (rows - 1) / 2 ))
    		# add smallest value to height to prevent negative values
    		if type(input[row][col]) == int:
    			box = Box(xShift, zShift, (0.25 + input[row][col] - smallestVal)
                * heightScale)
    		else:
    			val = input[row][col]
    			box = Box(xShift, zShift, (1.25 - smallestVal) * heightScale)
    			if val == "s":
    				# pastel green
    				box.faceColors[0] = START_COLOR
    			elif val == "e":
    				# pastel red
    				box.faceColors[0] = END_COLOR
    			elif val == "w":
    				# empty square
    				box = None
    		# add box to all boxes
    		boxes[row].append(box)

    # grab the mouse so it doesn't leave screen
    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(1)
    mouseVisible = False

    # define a variable to control the main loop
    running = True
    # main loop
    while running:
        if not mouseVisible:
        	dis.fill(BACKDROP)
        else:
        	dis.fill(GREY)
        dt = clock.tick()/50
        points2D = []

        # DRAWING BOXES
        # get all polygons (faces) to draw
        faces = []
        for boxRow in boxes:
            for box in boxRow:
                if box != None:
                	faces = faces + box.getFaces(cam)
        # sort by depth relative to camera with closest last
        sortedFaces = sorted(faces, key=lambda x : x[0], reverse = 1)
        # draw faces in order
        for face in sortedFaces:
        	pygame.draw.polygon(dis, face[1], face[2])

        # path name text
        if pathName != None:
            text = font.render(pathName, True, BLACK)
            dis.blit(text, (10, 10))

        # EVENT HANDLING
        for event in pygame.event.get():
        	# pass event to camera
        	if not mouseVisible:
        		cam.cameraEvent(dt, event, pygame.key.get_pressed())
        	if event.type == pygame.KEYDOWN:
        		# let spacebar pause
        		if event.key == pygame.K_SPACE:
        			if not mouseVisible:
        				pygame.mouse.get_rel()
        				pygame.mouse.set_visible(1)
        				pygame.event.set_grab(0)
        				mouseVisible = True
        			else:
        				pygame.mouse.get_rel()
        				pygame.mouse.set_visible(0)
        				pygame.event.set_grab(1)
        				mouseVisible = False
        		# p increments path step
        		if event.key == pygame.K_p:
        			if len(steps) == step:
        				pass
        			else:
        				row, col = steps[step]
        				box = boxes[row][col]
        				if input[row][col] != "s" and input[row][col] != "e":
        					box.faceColors[0] = getPathColor(0)
        				if step > 0:
        					prevStep = steps[step - 1]
        					prevRow, prevCol = prevStep
        					if prevRow == row - 1:
        						box.faceColors[1] = getPathColor(1)
        					elif prevRow == row + 1:
        						box.faceColors[2] = getPathColor(2)
        					elif prevCol == col - 1:
        						box.faceColors[3] = getPathColor(3)
        					elif prevCol == col + 1:
        						box.faceColors[4] = getPathColor(4)
        				if step < len(steps) - 1:
        					nextStep = steps[step + 1]
        					nextRow, nextCol = nextStep
       						if nextRow == row - 1:
        						box.faceColors[1] = getPathColor(1)
        					elif nextRow == row + 1:
        						box.faceColors[2] = getPathColor(2)
        					elif nextCol == col - 1:
        						box.faceColors[3] = getPathColor(3)
        					elif nextCol == col + 1:
        						box.faceColors[4] = getPathColor(4)
        				step += 1
        		if event.key == pygame.K_r:
        			step = 0
        			if pathNum == len(paths) - 1:
        				pathNum = 0
        			else:
        				pathNum += 1
        			for row in range(len(boxes)):
        				for col in range(len(boxes[row])):
        					if (input[row][col] != "w" and
                            input[row][col] != "s" and input[row][col] != "e"):
        						boxes[row][col].resetColors()
        			steps = paths[pathNum]
        	# close window upon quitting
        	if event.type == pygame.QUIT:
        		# change the value to False, to exit the main loop
        		running = False

		# display everything we've drawn
        pygame.display.update()

    pygame.quit()
