# Maze solver

This project is a homework project from CS 440 in University of Illinois at Urbana-Champaign (Fall 2019). 
Jiawen Hu's major work is in search.py. 

**Project description**:

In different maze layouts, the Pacman-like agent could find the shortest path from a given start state while eating one or dots. Four search strategies were implemented:
- Depth-first search
- Breadth-first search
- Greedy best-first search
- A* search

If there is only one dot to eat in the maze, we calculate the Manhattan distance betwee dot and current positio as heuristic function fo greedy best-first search and A* search. 
If there are more tha one dots exist in the maze, the heuristic function is composed of two parts:
1. Create a weighted complete graph from the un-visited objectives, where the weight is the Manhattan distance between each pair of objectives. Then calculate the MST edge distance, set it as h1.
2. Calculate the nearest node from the un-visited node to the current node(in Manhattan distance), set it as h2.
The sum of h1 and h2 is the heuristic function for multiple dots.
