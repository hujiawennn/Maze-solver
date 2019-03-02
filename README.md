# Maze solver

This project is a homework project from CS 440 in University of Illinois at Urbana-Champaign (Fall 2019). 
Jiawen Hu's major work is in search.py. 

**Project description**:

In different maze layouts, the Pacman-like agent could find the shortest path from a given start state while eating one or dots. Four search strategies were implemented:
- Depth-first search
- Breadth-first search
- Greedy best-first search
- A* search

If there is only one dot to eat in the maze, we calculate the Manhattan distance between dot and current position as heuristic function for greedy best-first search and A* search. 
If there are more than one dots exist in the maze, the heuristic function is composed of two parts:
1. Create a weighted complete graph from the un-visited objectives, where the weight is the Manhattan distance between each pair of objectives. Then calculate the MST edge distance, set it as h1.
2. Calculate the nearest node from the un-visited node to the current node (in Manhattan distance), set it as h2.
The sum of h1 and h2 is the heuristic function for multiple dots.

There is a maze layout called "bigDots" provided by instructors as an extra challenge for students. We solved the bigDots maze by implementing greedy search algorithm mainly. By using the greedy search function for single-dot maze as a helper function, we solved the maze by resetting the start and end for the inputs of the helper function. In other words, the ending point will become the starting point in the next turn and the ending point will be the closest point next to the starting point. Except the initial starting point, all the other “start” and “end” were chosen from the set of remaining dots that were not reached yet. What’s more, the way we decide what is the next node to go is different from the greedy search algorithm. We add up the path length already travelled (g) and the actual distance (using the helper function from A* search algorithm). This search algorithm is very fast when dealing with multiple dots situation, compared to A* search algorithm.
