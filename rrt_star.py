import pygame
import numpy as np
import time

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
        self.children = set()
    
    def __repr__(self) -> str:
        return f"({self.state}, {self.parent}, {self.c2c})"
    
    def __lt__(self, other):
        return self.c2c < other.c2c




# _____________________ Defining Obstacle Space __________________________
print("\n****************** Map *****************")

# print("Input Clearence Value ---")
# clearence = int(input(" "))
clearence = 5


print(" Please wait, Preparing Map ..... ")

# -- Returns value >= 1, if a point is in obstacle space
def obstacle(x,y):
    # y=199-y 
    if x >= 150 and x < 175 and y >= 200:  
        return True             # 1st obstacle
    if x >= 250 and x < 275 and y < 100:
        return True             # 2nd obstacle
    if (x - 420)**2 + (y-120)**2 <= 3600:  
        return True             # equations for lines that surround polygon
    else: 
        return False            
 

matrix = np.zeros((600,400))         # Defining a matrix representing canvas 1200 x 500 with zeros

for i in range(600):                    # looping through all elements in matrix
    for j in range(400):
        if obstacle(i,j):               # checking if point is in obstacle space
            matrix[i,j]=1               # 1 means obstacle
# _____________________ End of Defining Obstacle Space __________________________



# _____________________ RRT* Algorithm __________________________
def get_random_state(graph):
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




def path_check(point, parent):
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
 
def back_track(graph, node):
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


def print_path(path, color):
    for i in range(len(path)-1):
        pygame.draw.line(window, color, path[i], path[i+1])
        pygame.display.flip()


# ____________________ Display Pygame Window _______________________
pygame.init()
#initializing color
white=(230,230,230)
black = (0,0,0)
grey = (150,150,150)
red = (225,50,50)
blue = (105,135,235)
#initializing window
window = pygame.display.set_mode((600,400)) # window size
window.fill(white) # filling it with color


# LOOP to transform matrix into this window
for i in range(600):
    for j in range(400):
            if matrix[i,j]==1: # 1 -> red color showing obstacles
                window.set_at((i,j),red)
            elif matrix[i,j]==2: # 2-> black showing bloating part
                window.set_at((i,j),black)
            elif matrix[i,j]==5:
                window.set_at((i,j),grey)

pygame.display.flip() #updating window
# ____________________ End of Display Pygame Window _______________________


#-------------------------------------------------------------------------
start = (200,150)
goal = (500,150)
# print("Error") if matrix[start[0], start[1]]!=0 or matrix[goal[0], goal[1]]!=0 else None
node_radius = 15
rewire_radius = 20

step = 7
goal_threshold = 8
data = {}

pygame.draw.circle(window, (255,0,0), start, 5)
pygame.draw.circle(window, (0,0,0), goal, 5)
#----------------------------------------------------------------------------------------------------------------



def rrt_star(start, goal):
    global step
    global goal_threshold
    start_node = Node(start, None, 0)

    graph=[]
    graph.append(start_node)

    global data
    data[start] = start_node

    goal_reached = False
    while True:
        # Generate random node

        # Find nearest node
        rand_point1 = get_random_state(graph)

        # find new point in corresponding direction
        
        # check if the point is in obstacle space and continue if true
        if not 0<= rand_point1[0] < 600 or not 0<= rand_point1[1] < 400:
            continue

        # check if the point is in obstacle space and continue if true
        if matrix[rand_point1[0], rand_point1[1]]!=0:
            continue
       
        # check if the point is already in the graph and continue if true
        if rand_point1 in [i.state for i in graph]:
            continue
        
        # Find nearest node with less c2c
        
        neighs = find_neigh(rand_point1, graph, node_radius)
        # else:    
            # neighs = []

        # Add the new node to the graph with less c2c as parent
        for i in neighs:
            path_ok = path_check(rand_point1, i.state)
            if path_ok:
                new_node = Node(rand_point1, i.state, i.c2c+distance(rand_point1, i.state)) 
                break


        # if len(neighs)>0:
        #     new_node = Node(rand_point1, nearest_c2c.state, nearest_c2c.c2c+step)
        # else:
        #     new_node = Node(rand_point1, nearest_node.state, nearest_node.c2c+step)

        # check if the path to the new node is in obstacle space and continue if true
        # path_ok = path_check(new_node.state, new_node.parent)
        # if not path_ok:
        #     continue

        graph.append(new_node)

        # add the new node to the data dictionary
        data[rand_point1] = new_node
        # add the new node to the children of the parent node
        data[new_node.parent].children.add(new_node.state)


        # draw the new node and parent node and line between them
        pygame.draw.circle(window, grey, new_node.state, 2)
        # pygame.draw.circle(window, blue, new_node.parent, 2)
        pygame.draw.line(window, blue, new_node.state, new_node.parent)
        pygame.display.flip()



        neighs = find_neigh(rand_point1, graph, rewire_radius)
        # Rewire the graph
        for i in neighs:
            if i.state == new_node.parent:
                continue
            dist = distance(new_node.state, i.state)
            if i.c2c > new_node.c2c + dist:
                # check if path possible
                path_ok1 = path_check(i.state, new_node.state)
                if path_ok1:
                    pygame.draw.line(window, white, i.state, i.parent)

                    # remove the node from the children of the parent node
                    data[i.parent].children.remove(i.state)
                    # add the node as child of the new node
                    data[new_node.state].children.add(i.state)

                    difference = i.c2c - (new_node.c2c + dist)

                    i.parent = new_node.state
                    i.c2c = new_node.c2c + dist

                    # pygame.draw.circle(window, (0, 255, 0), new_node.state, 1.5)
                    pygame.draw.line(window, blue, i.state, i.parent)
                    pygame.display.flip()

                    update_children_costs(data, i, difference)
             
        # check if the point is in the goal region and back track
        if not goal_reached:
            if np.sqrt((rand_point1[0] - goal[0])**2 + (rand_point1[1] - goal[1])**2) <= goal_threshold:
                print("Goal Reached")
                path = back_track(graph, new_node)
                print_path(path, black)
                goal_node = new_node
                goal_cost = goal_node.c2c
                print(goal_cost)
                extra_n=0
                no_prints = 0
                goal_reached = True
            
        if goal_reached:
            extra_n += 1
            if extra_n == 200:
                no_prints+=1
                extra_n = 0
                print_path(path, blue)
                path = back_track(graph, goal_node)
                print_path(path, black)
                print(goal_node.c2c)
            
            if no_prints ==20:
                return path, graph

        # n +=1
        # if n == 250:
        #    break

# _____________________ End of RRT* Algorithm __________________________




# ____________________ RRT* Algorithm _______________________


path, graph = rrt_star(start, goal)
# rrt_star(start, goal)

# ____ Draw the explored Graph ______
# for i in graph[1:]:             # skipping the start node, it has no parent
#     pygame.draw.line(window, (0, 0, 255), i.state, i.parent)
#     pygame.display.flip()
    # time.sleep(0.1)

# ____ Draw the path ______

# ____________________ End of RRT* Algorithm _______________________



# _____________Keep Pygame Window Open_________________
run = True
while run: 
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
    # time.sleep(5)
            run = False
    pygame.display.update()

# time.sleep(5)
pygame.quit()
# _____________End of Pygame Window____________________