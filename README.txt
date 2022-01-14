3D Pathfinder
Authors: William Holtz, Gwen Hardwick, Moses Solomon

 * Introduction
    
     Our program, 3D Pathfinder, is an easy to use visualizer for paths found in a 2D
 array. First the user is given the ability to create a 10X10 landscape with out input
 GUI. Then, the user is given a choice between one of 3 pathfinding algorithms to find
 a path from a source to a target. These algorithms are designed to minimize the cost
 of this path, where the cost of moving from one square to another, is the value of the
 newly-traveled-to's elevation. Once an array and a pathfinding algorithm are chosen,
 a 3D render of the array appears in an environment the user is free to move and look
 around in. Finally, the user can view the path's movement one square at a time. We hope
 you find that our program is easy to use and understand!
 
 
 * Requirements
    
     - Python ver 3.9.7, 
     - Pygame ver 2.1.0
     - Numpy ver 1.21.3
     
 
 * Running Instructions
 	 
 	 Assuming one has the required libraries installed, simply compile and run the file 
 "inputArray.py". This can be done in a mac terminal with the line:
 
 		"python3 <FILE PATH>/inputArray.py"
 		
 Where <FILE PATH> is the path preceding the file.
 
 
 * Input GUI Controls
 	 
 	 All GUI controls also appear in the console.
 S: Place starting position for the pathfinding algorithm
 E: Place ending position for the pathfinding algorithm
 P: Increase the elevation of square
 O: Decrease the elevation of square
 Left Mouse Button: Place impassable wall
 R: randomize all of the remaining elevations on the map
 1-5: Use premade graph
 Return: Save the graph and freeze the GUI until 7, 8, or 9 are pressed
  - The following keys only apply after Return has been pressed
  	- 7: Use the greedy algorithm to construct a path and pull up the 3D visualizer
  	- 8: Use Dijkstra's algorithm to construct a path and pull up the 3D visualizer
  	- 9: Use the annealing algorithm to construct a path and pull up the 3D visualizer
 
 
 * 3D GUI Controls
 
 W: Move forwards
 S: Move backwards
 A: Move right
 D: Move left
 E: Move up
 Q: Move down
 P: Advance the path
 R: Reset the path's progress
 Space: Pause movement inputs and make mouse visible
 
 	 
 * Common Problems
 
     It should be noted that when creating an array, one must fulfill the following
 conditions: 1.) There is exactly one start and end tile and 2.) there must be a valid 
 path from the start to the end. Additionally, we are aware of problems with our
 annealing algorithm. Notably, is neither technically an anealing algorithm, and it has
 a tendency to fail on sporadic or randomly generated arrays. Finally, we do not claim 
 that the paths discovered by our algorithms are ideal. Rather, they are implemented to 
 display the differences and shortcomings of one another.
