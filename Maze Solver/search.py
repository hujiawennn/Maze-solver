# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

import heapq
# Calls functions that are implemented with different algorithms.
def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
        "greedyDots": greedyDots,
    }.get(searchMethod)(maze)

# 
def bfs(maze):
    # return path, num_states_explored
    dem = maze.getDimensions()
    status = [[(0, None) for i in range(dem[1])] for j in range(dem[0])]
    # add start position to queue
    start = maze.getStart()
    status[start[0]][start[1]] = (1, None)
    queue = [start]
    # start searching
    num_explored = 0
    while(len(queue) > 0):
        curr = queue.pop(0)
        num_explored += 1
        # if objective is found
        if (maze.isObjective(curr[0], curr[1])):
            path = [curr]
            temp = curr
            while (status[temp[0]][temp[1]][1] is not None):
                temp = status[temp[0]][temp[1]][1]
                path.append(temp)
            return path[::-1], num_explored
        # if objective is not found
        status[curr[0]][curr[1]] = (2, status[curr[0]][curr[1]][1])
        neighbors = maze.getNeighbors(curr[0], curr[1])
        available = 0
        for neighbor in neighbors:
            if (status[neighbor[0]][neighbor[1]][0] == 0):
                status[neighbor[0]][neighbor[1]] = (1, curr)
                queue.append(neighbor)
                available += 1
        # dead end
        # if available == 0:
    return [], 0


def dfs(maze):
    # create 2D array and mark every point to be unexplored
    start = maze.getStart()
    dem = maze.getDimensions()
    stack = []
    stack.append(start)
    status = [[0 for i in range(dem[1])] for j in range(dem[0])]
    dfs_help(start[0], start[1], stack, status, maze)
    num_states_explored = 0
    for i in range(dem[0]):
        for j in range(dem[1]):
            if status[i][j] == 1:
                num_states_explored += 1
    return stack, num_states_explored


# dfs helper function
def dfs_help(row, column, stack, status, maze):
    status[row][column] = 1
    if (maze.isObjective(row, column)):
        stack.append((row, column))
        return True
    for n in maze.getNeighbors(row, column):
        if len(maze.getNeighbors(row, column)) == 1 and status[n[0]][n[1]] == 1:
            return False
        if status[n[0]][n[1]] != 1:
            stack.append(n)
            if dfs_help(n[0], n[1], stack, status, maze) is False:
                stack.pop()
            else:
                return True
    return False


def greedy(maze):
    heap = []
    start = maze.getStart()
    goal = maze.getObjectives()[0]
    h = calManhattan(start, goal)
    heapq.heappush(heap, (h, start))

    num_states_explored = 0
    visited = []
    reverse_path = dict()

    current = start
    while current != goal:
        current = heapq.heappop(heap)[1]
        visited.append(current)
        num_states_explored += 1
        neighbors = maze.getNeighbors(current[0], current[1])
        for i in neighbors:
            h = calManhattan(i, goal)
            if (h, i) not in heap and i not in visited:
                heapq.heappush(heap, (h, i))
                reverse_path[i] = current
    path = []
    current = goal
    while current != start:
        path.append(current)
        # get parent
        current = reverse_path[current]
    path.append(start)
    path = path[::-1]
    return path, num_states_explored


def astar(maze):
    start = maze.getStart()
    objectives = maze.getObjectives()
    allNodes = [start]
    allNodes.extend(objectives)
    paths = allPaths(maze)
    mst_distances = getMSTList(maze, list(map(lambda x: x[1:], paths[1:])))
    # An integer representation of "all objectives" at the start
    starting_obj_repr = 2**len(objectives) - 1
    # dictionary for storing ancestor and g_distance
    ancestors = dict()
    ancestors[(start, starting_obj_repr)] = ((None, None), 0)
    g = 0
    h1 = nearestObject(maze, start, starting_obj_repr)
    h2 = mst_distances[starting_obj_repr]
    # frontier stores tuple(h + g, (location, remaining_objectives))
    frontier = [(g + h1 + h2, (start, starting_obj_repr))]
    num_states_explored = 0
    # list for storing visited states
    visited = []
    current_state = (start, starting_obj_repr)
    while current_state[1] != 0:
        current_state = heapq.heappop(frontier)[1]
        visited.append(current_state)
        num_states_explored += 1
        current_node = current_state[0]
        current_index = allNodes.index(current_node)
        remaining_objectives = decodeObjectivesRepresentation(maze, current_state[1])
        for node in remaining_objectives:
            node_index = allNodes.index(node)
            # An integer representation of "unexplored objectives"
            remaining_obj_repr = current_state[1] - 2**(node_index - 1)
            h1 = nearestObject(maze, node, remaining_obj_repr)
            h2 = mst_distances[remaining_obj_repr]
            g = ancestors[current_state][1] + len(paths[current_index][node_index])
            frontier_index = frontierIndex(frontier, (node, remaining_obj_repr))
            if (frontier_index >= 0):
                if frontier[frontier_index][0] > (g + h1 + h2):
                    frontier[frontier_index] = (g + h1 + h2, (node, remaining_obj_repr))
                    frontier.sort()
                    ancestors[(node, remaining_obj_repr)] = (current_state, g)
            elif (node, remaining_obj_repr) not in visited:
                heapq.heappush(frontier, (g + h1 + h2, (node, remaining_obj_repr)))
                ancestors[(node, remaining_obj_repr)] = (current_state, g)
    # get path from ancestors list
    sequence = []
    while current_state[0] is not None:
        sequence.append(current_state[0])
        current_state = ancestors[current_state][0]
    sequence = sequence[::-1]
    final_path = []
    for (i, node) in enumerate(sequence[:-1]):
        sub_path = paths[allNodes.index(node)][allNodes.index(sequence[i + 1])]
        if node != sequence[-2]:
            final_path.extend(sub_path[:-1])
        else:
            final_path.extend(sub_path)
    return final_path, num_states_explored



# find the nearest object(in Manhattan distance) to current node
def nearestObject(maze, current, remaining_obj_repr):
    if (remaining_obj_repr == 0):
        return 0
    remaining_objectives = decodeObjectivesRepresentation(maze, remaining_obj_repr)
    result = []
    for objective in remaining_objectives:
        result.append(calManhattan(current, objective))
    return min(result)



def decodeObjectivesRepresentation(maze, remaining_obj_repr):
    objectives = maze.getObjectives()
    bits = str(bin(remaining_obj_repr))[2:]
    result = []
    for (i , c) in enumerate(bits[::-1]):
        if c == '1':
            result.append(objectives[i])
    return result
    


# calculate all the shortest paths between every pair of objects
def allPaths(maze):
    allNodes = [maze.getStart()]
    allNodes.extend(maze.getObjectives())
    dem = len(allNodes)
    paths = [[() for i in range(dem)] for j in range(dem)]
    for i in range(dem):
        for j in range(i + 1):
            if i != j:
                path, _ = astar_helper(maze, allNodes[i], allNodes[j])
                paths[i][j] = tuple(path)
                paths[j][i] = tuple(path[::-1])
    return paths



# calculate all the Manhattan distances between every pair of nodes(start and objects)
def allManhattanDistance(nodes):
    dem = len(nodes)
    manhattanDistances = [[0 for i in range(dem)] for j in range(dem)]
    for i in range(dem):
        for j in range(i + 1):
            if i != j:
                m_distance = calManhattan(nodes[i], nodes[j])
                manhattanDistances[i][j] = m_distance
                manhattanDistances[j][i] = m_distance
    return manhattanDistances



# Astar helper function
# returns the shortest path between two given nodes, and the number of explored states
def astar_helper(maze, start, goal):
    h = calManhattan(start, goal)
    g = 0
    frontier = [(h + g, start)]
    # create a dictionary stores the ancestor and g-distance
    ancestors = dict()
    ancestors[start] = (None, 0)
    num_states_explored = 0
    visited = []
    current = start
    while current != goal:
        current = heapq.heappop(frontier)[1]
        visited.append(current)
        num_states_explored += 1
        neighbors = maze.getNeighbors(current[0], current[1])
        for neighbor in neighbors:
            h = calManhattan(neighbor, goal)
            g = ancestors[current][1] + 1
            frontier_index = frontierIndex(frontier, neighbor)
            if frontier_index >= 0:
                if frontier[frontier_index][0] > (g + h):
                    frontier[frontier_index] = (g + h, neighbor)
                    frontier.sort()
                    ancestors[neighbor] = (current, g)
            elif neighbor not in visited:
                heapq.heappush(frontier, (h + g, neighbor))
                ancestors[neighbor] = (current, g)
    # get path from ancestors list
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = ancestors[current][0]
    path.append(start)
    return path[::-1], num_states_explored


def frontierIndex(frontier, state):
    for (i, node) in enumerate(frontier):
        if node[1] == state:
            return i
    return -1



def convert_int_to_b(int_num, num_bit):
   
    a = [0 for i in range(num_bit)]
    
    a_index = num_bit - 1
    
    for digit in reversed(bin(int_num)[2:]):
        a[a_index] = int(digit)
        a_index -=1
    return a



def getMSTList(maze, paths):
    goals = maze.getObjectives()
    n = len(goals)
    all_combi = {}
    ma = [[0 for i in range(n)] for j in range(n)]
    for row in range(n):
        for col in range(row + 1):
            path_len = len(paths[row][col])
            ma[row][col] = path_len
            ma[col][row] = path_len

    for deci_value in range(1, 2**n):
        binary_list = convert_int_to_b(deci_value, n)
        cl = []
        for i in range(len(binary_list)):
            if binary_list[i] == 1:
                cl.append(len(binary_list) - 1 - i)
        
        all_combi[deci_value] = mst(cl, ma)
    all_combi[0] = 0
    return all_combi


def find(i, parent):
    while parent[i] != i:
        i = parent[i]
    return i

# Disjoint set data structure - union
def union(i, j, parent):
    a = find(i, parent)
    b = find(j, parent)
    parent[a] = b


def mst(cl,m):
    mincost = 0
    n = len(cl)
    parent = [i for i in range(n)]
    edge_count = 0
    while edge_count < (n - 1):
        min = float('inf')
        a = -1
        b = -1
        for i in range(n):
            for j in range(n): 
                if find(i, parent) != find(j, parent) and m[cl[i]][cl[j]] < min: 
                    min = m[cl[i]][cl[j]]; 
                    a = i; 
                    b = j; 
        union(a, b, parent); 
        edge_count+=1
        mincost += min
    
    return mincost


# calculate Manhattan distance between two given points
def calManhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def greedyDots(maze):
    goals = maze.getObjectives()
    remaining_goals = maze.getObjectives()
    start = maze.getStart()
    states_explored = 0
    path = []
    path.append(start)
    while len(remaining_goals) != 0:
        end = find_closest_pt(maze, start, remaining_goals)
        states_explored += greedy_helper(start, end, maze, states_explored, path)
        start = end
    return path, states_explored


def greedy_helper(start, goal, maze, tot_num_states, final_path):
    heap = []
    h = calManhattan(start, goal)
    g = 0
    heapq.heappush(heap, (h + g, g, start))
    num_states_explored = 0
    visited = []
    reverse_path = dict()
    current = start
    while current != goal:
        c_t = heapq.heappop(heap)
        current = c_t[2]
        visited.append(current)
        num_states_explored += 1
        neighbors = maze.getNeighbors(current[0], current[1])
        for i in neighbors:
            g = c_t[1] + 1
            h = calManhattan(i, goal)
            if (h + g, g, i) not in heap and i not in visited:
                heapq.heappush(heap, (h + g, g, i))
                reverse_path[i] = current
    path = []
    current = goal
    while current != start:
        path.append(current)
        # get predecessor
        current = reverse_path[current]
    path = path[::-1]
    final_path.extend(path)
    return num_states_explored


def find_closest_pt(maze, point, remaining_goals):
    min = float("inf")
    result = point
    for pt in remaining_goals:
        x = len(astar_helper(maze, point, pt)[0])
        # x = calManhattan(point, pt)
        if x < min:
            min = x
            result = pt
    remaining_goals.remove(result)
    return result
