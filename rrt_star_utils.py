import pygame
import numpy as np
import math



class Node:
    def __init__(self, state, parent, c2c):
        self.state = state
        self.parent = parent
        self.c2c = c2c
        # if self.parent is None:
        #     self.step = 0
        #     self.c2c = 0
        # else:
        #     self.step = distance(self.state, self.parent)
        #     self.c2c = data[self.parent].c2c + self.step
        self.gen = 0    # generation number
        self.children = set()
    
    def __repr__(self) -> str:
        return f"({self.state}, {self.parent}, {self.c2c})"
    
    def __lt__(self, other):
        return self.c2c < other.c2c








# _____________________ RRT* Algorithm __________________________
def get_random_state(graph, step):
    # Select a random point
    rand_point = (np.random.randint(0,599), np.random.randint(0,399))
    # find the nearest node to the random point
    temp_dist = []
    for i in graph:
        dist = distance(rand_point, i.state)
        # angle = np.arctan2(randnode[1] - i.state[1], randnode[0] - i.state[0])
        temp_dist.append(dist)
    index = temp_dist.index(min(temp_dist))
    # return graph[index]
    # find the new point in the direction of the random point
    nearest_state = graph[index].state
    theta = np.arctan2(rand_point[1] - nearest_state[1], rand_point[0] - nearest_state[0])
    x = nearest_state[0] + step*np.cos(theta)
    y = nearest_state[1] + step*np.sin(theta)
    return (int(x), int(y))



def find_neigh(rand_point1, graph, node_radius):
    # global NODE_RADIUS
    neigh_nodes = []
    for node in graph:
        dist = np.sqrt((rand_point1[0] - node.state[0])**2 + (rand_point1[1] - node.state[1])**2)
        if dist <= node_radius:
            neigh_nodes.append((node, dist+node.c2c))
    
    neigh_nodes.sort(key=lambda x:x[1])   
    # neigh_nodes=neigh_nodes[]     
    return [node for node, _ in neigh_nodes]




def path_check(point, parent, matrix):
    # if slope is infinite -- vertical line
    if point[0] == parent[0]:
        for y in np.arange(parent[1], point[1], 1):
            if matrix[int(point[0]), int(y)] == 1:
                return False
        return True
    # if slope not infinite
    m = (point[1] - parent[1])/(point[0] - parent[0])
    c = point[1] - m*point[0]
    for x in np.arange(parent[0], point[0], 1):
        y = m*x + c
        if matrix[int(x), int(y)] == 1:
            return False
    return True


def get_new_point(rand_point, nearest_node, step):
    # if dist<=step:
    #     return rand_point # since step changed, it is less than the original step
    # else:
    theta = np.arctan2(rand_point[1] - nearest_node[1], rand_point[0] - nearest_node[0])
    x = nearest_node[0] + step*np.cos(theta)
    y = nearest_node[1] + step*np.sin(theta)
    return (int(x), int(y))
 
def back_track(graph, node, start):
    path = []
    # node = graph[-1]
    while node.state!=start:
        path.append(node.state)
        node = [i for i in graph if i.state == node.parent][0]
    path.append(start)
    path.reverse()
    return path


def distance(state1, state2):
    dist = np.sqrt((state1[0]-state2[0])**2+(state1[1]-state2[1])**2)
    return dist

def update_children_costs(data, node, difference):
    for child in node.children:
        data[child].c2c -= difference
        update_children_costs(data, data[child], difference)


def print_path(path, color, window):
    for i in range(len(path)-1):
        pygame.draw.line(window, color, path[i], path[i+1])
        pygame.display.flip()


def calculate_angle(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    rad = math.atan2(y2 - y1, x2 - x1)  # get the angle in radians
    deg = math.degrees(rad)  # convert to degrees
    return deg if deg >= 0 else deg + 360


def update_generations(node, data):
    parent = node.parent
    while parent is not None:
        data[parent].gen += 1
        node = data[parent]
        parent = node.parent


