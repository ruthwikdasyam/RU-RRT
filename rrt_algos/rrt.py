import pygame
import numpy as np

class Node:
    def __init__(self, state, parent, c2c):
        self.state = state
        self.parent = parent
        self.c2c = c2c
    
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
    y=199-y 
    if x >= 150 and x < 175 and y >= 100:  
        return True             # 1st obstacle
    if x >= 250 and x < 275 and y < 100:
        return True             # 2nd obstacle
    if (x - 420)**2 + (y-120)**2 <= 3600:  
        return True             # equations for lines that surround polygon
    else: 
        return False            
 

matrix = np.zeros((600,200))         # Defining a matrix representing canvas 1200 x 500 with zeros

for i in range(600):                    # looping through all elements in matrix
    for j in range(200):
        if obstacle(i,j):               # checking if point is in obstacle space
            matrix[i,j]=1               # 1 means obstacle
# _____________________ End of Defining Obstacle Space __________________________



# _____________________ RRT Algorithm __________________________
def find_nearest_node(rand_point, graph):
    temp_dist = []
    for i in graph:
        dist = np.sqrt((rand_point[0] - i.state[0])**2 + (rand_point[1] - i.state[1])**2)
        # angle = np.arctan2(randnode[1] - i.state[1], randnode[0] - i.state[0])
        temp_dist.append(dist)
    index = temp_dist.index(min(temp_dist))
    return graph[index]

def get_new_point(rand_point, nearest_node, step):
    dist = np.sqrt((rand_point[0] - nearest_node[0])**2 + (rand_point[1] - nearest_node[1])**2)
    if dist<=step:
        return rand_point
    else:
        theta = np.arctan2(rand_point[1] - nearest_node[1], rand_point[0] - nearest_node[0])
        x = nearest_node[0] + step*np.cos(theta)
        y = nearest_node[1] + step*np.sin(theta)
        return (int(x), int(y))
    

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


def back_track(graph):
    path = []
    node = graph[-1]
    while node.state!=start:
        path.append(node.state)
        node = [i for i in graph if i.state == node.parent][0]
    path.append(start)
    path.reverse()
    return path

def rrt(start, goal):
    global step
    global goal_threshold
    start_node = Node(start, None, 0)

    graph=[]
    graph.append(start_node)
    while True:
        # Generate random node
        rand_point = (np.random.randint(0,600), np.random.randint(0,200))

        # Find nearest point
        nearest_node = find_nearest_node(rand_point, graph)

        # find new point in corresponding direction
        rand_point1 = get_new_point(rand_point, nearest_node.state, step)
        
        # check if the point is in obstacle space and continue if true
        if matrix[rand_point1[0], rand_point1[1]]!=0:
            continue
       
        # check if the point is already in the graph and continue if true
        if rand_point1 in [i.state for i in graph]:
            continue
        
        # Create a new node
        new_node = Node(rand_point1, nearest_node.state, nearest_node.c2c+step)

        # check if the path to the new node is in obstacle space and continue if true
        path_ok = path_check(new_node.state, new_node.parent)
        if not path_ok:
            continue

        # Add the new node to the graph
        graph.append(new_node)
        
        # draw the new node and existing node and line between them
        pygame.draw.circle(window, blue, new_node.state, 1.5)
        pygame.draw.circle(window, blue, nearest_node.state, 1.5)
        pygame.draw.line(window, grey, nearest_node.state, new_node.state)
        pygame.display.flip()

             
        # check if the point is in the goal region and back track
        if np.sqrt((new_node.state[0] - goal[0])**2 + (new_node.state[1] - goal[1])**2) <= goal_threshold:
            print("Goal Reached")
            path = back_track(graph)
            for i in range(len(path)-1):
                pygame.draw.line(window, (0, 255, 0), path[i], path[i+1])
                pygame.display.flip()
            break
        
 

# _____________________ End of RRT Algorithm __________________________







# ____________________ Display Pygame Window _______________________
pygame.init()
#initializing window
window = pygame.display.set_mode((600,200)) # window size
window.fill((255,255,255)) # filling it with color
#initializing color
white=(230,230,230)
black = (0,0,0)
grey = (150,150,150)
red = (225,50,50)
blue = (105,135,235)

# LOOP to transform matrix into this window
for i in range(600):
    for j in range(200):
            if matrix[i,j]==1: # 1 -> red color showing obstacles
                window.set_at((i,j),red)
            elif matrix[i,j]==2: # 2-> black showing bloating part
                window.set_at((i,j),black)
            elif matrix[i,j]==5:
                window.set_at((i,j),grey)

pygame.display.flip() #updating window
# ____________________ End of Display Pygame Window _______________________



# ____________________ RRT Algorithm _______________________
start = (50,50)
goal = (550,150)
step = 10
goal_threshold = 5
pygame.draw.circle(window, (255,0,0), start, 2)
pygame.draw.circle(window, (0,255,0), goal, 2)
rrt(start, goal)
# ____________________ End of RRT Algorithm _______________________



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