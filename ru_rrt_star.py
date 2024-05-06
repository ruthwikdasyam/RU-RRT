from rrt_star_utils import *


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
# Creating local flow matrix
local_matrix = np.zeros((600,400))
# import flow_matrix
global_matrix = np.load('flow_matrix.npy', allow_pickle=True)
query_trees = np.load('query_trees.npy', allow_pickle=True)

# _____________________ Defining Start and Goal __________________________

start = (200,150)
goal = (500,150)
# print("Error") if matrix[start[0], start[1]]!=0 or matrix[goal[0], goal[1]]!=0 else None
node_radius = 15
rewire_radius = 20

step = 7
goal_threshold = 8
node_dict = {}

pygame.draw.circle(window, (255,0,0), start, 5)
pygame.draw.circle(window, (0,0,0), goal, 5)
#----------------------------------------------------------------------------------------------------------------

# deleting branches of the focus node
def delete_branches(node, graph, node_dict):
    for child in node.children:
        delete_branches(node_dict[child], graph, node_dict)
    graph.remove(node)
    del node_dict[node.state]


# adding tree to the graph
def add_tree(other_map, start, graph, node_dict):
    # add all the nodes of other map dict to  node_dict
    for i in other_map[start].children:
        node_dict[i] = other_map[i]
        graph.append(other_map[i])
        add_tree(other_map, i, graph, node_dict)
    



def rrt_star(start, goal):
    global step
    global goal_threshold
    start_node = Node(start, None, 0)

    graph=[]
    graph.append(start_node)

    global node_dict
    node_dict[start] = start_node

    goal_reached = False
    while True:
        # Generate random node

        # Find nearest node
        rand_point1 = get_random_state(graph, step)

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
            path_ok = path_check(rand_point1, i.state, matrix)
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

        # if no children to parent add generation to the parent node
        # if len(node_dict[new_node.parent].children) == 0:
        #     node_dict[new_node.parent].gen += 1
        #     # update generation of all the parent nodes
        #     update_generations(node_dict[new_node.parent], node_dict)

        # add the new node to the node_dict dictionary
        node_dict[rand_point1] = new_node
        # add the new node to the children of the parent node
        node_dict[new_node.parent].children.add(new_node.state)


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
                path_ok1 = path_check(i.state, new_node.state, matrix)
                if path_ok1:
                    pygame.draw.line(window, white, i.state, i.parent)

                    # remove the node from the children of the parent node
                    node_dict[i.parent].children.remove(i.state)
                    # add the node as child of the new node
                    node_dict[new_node.state].children.add(i.state)

                    difference = i.c2c - (new_node.c2c + dist)

                    i.parent = new_node.state
                    i.c2c = new_node.c2c + dist

                    # pygame.draw.circle(window, (0, 255, 0), new_node.state, 1.5)
                    pygame.draw.line(window, blue, i.state, i.parent)
                    pygame.display.flip()

                    update_children_costs(node_dict, i, difference)
             
        # check if the point is in the goal region and back track
        if not goal_reached:
            if np.sqrt((rand_point1[0] - goal[0])**2 + (rand_point1[1] - goal[1])**2) <= goal_threshold:
                print("Goal Reached")
                path = back_track(graph, new_node, start)
                print_path(path, black, window)
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
                print_path(path, blue, window)
                path = back_track(graph, goal_node, start)
                print_path(path, black, window)
                print(goal_node.c2c)
            
            if no_prints ==20:
                return path, graph

        # n +=1
        # if n == 250:
        #    break

        # Reuse RRT* Algorithm____________________________________________________

        if new_node.great_grand_parent(node_dict):
            focus_state = new_node.great_grand_parent(node_dict)
            focus_node = node_dict[focus_state]
            # checking eligibility for flow
            if focus_node.flow_value() is not None:
                focus_node_flow = focus_node.flow_value() # get flow value of the focus node, check if we need to take node or its parent !!!
                # Get quotient of the flow value
                focus_node_flow_ = focus_node_flow//15
                # checking sub tree size of the focus node
                sub_tree_size = focus_node.sub_tree_size()

                probable_trees=[]
                flow_check_radius = 10
                # get list of all states in the flow check radius fom the focus state
                for i in range(focus_state[0]-flow_check_radius, focus_state[0]+flow_check_radius):
                    for j in range(focus_state[1]-flow_check_radius, focus_state[1]+flow_check_radius):
                        if 0<=i<600 and 0<=j<400:
                            radius = np.sqrt((i-focus_state[0])**2 + (j-focus_state[1])**2)
                            if radius <= flow_check_radius:
                                probable_trees.append([global_matrix[i, j, focus_node_flow_], (i, j)])
                
                # [ [map 2, 265], (i , j) ]

                best_tree = max(probable_trees, key=lambda x: x[0][1])
                
                # checking if its helpful to add the best tree to current tree
                if best_tree[0][1] < 1.2*sub_tree_size:
                    best_tree = None

                # checking if best tree is None
                if best_tree is None:
                    # if not, add the node_flow to the local matrix
                    local_matrix[focus_state[0], focus_state[1]] = (focus_node_flow, sub_tree_size)
                else:
                    # if yes, add the best tree to the local tree
                    #delete all branches of the focus node in the graph
                    delete_branches(focus_node, graph, node_dict)        # check if we aew deleting the focus node too !!!!
                    # update focus node
                    node_dict[focus_node.parent].state = best_tree[1]   # check cost once !!!
                    graph.append(best_tree[1])

                    reusemap_ID = best_tree[0][0] # get the map ID of the best tree
                    other_map = query_trees[reusemap_ID] # get the dict of that map

                    # add the best tree to the graph from start node - (i,j) match 
                    add_tree(other_map, best_tree[1], graph, node_dict) # add_tree(tree, start, new_node, graph, node_dict)



# _____________________ End of RRT* Algorithm __________________________

#______________________ saving node_dict   _______________________
# get the index for which the query_trees is empty
query_id = np.where(query_trees == None)[0][0]
query_trees[query_id] = node_dict


# update flow_matrix with local_matrix
# global_matrix = np.load('flow_matrix.npy')

for i in range(600):
    for j in range(400):
        if local_matrix[i,j] != 0: # if the local matrix is not empty
            k = local_matrix[i,j][0]//15 # quotient of the flow value
            global_matrix[i,j,k] = [query_id, local_matrix[i,j][1]] # [query_id, sub_tree_size]
# save the global_matrix
np.save('flow_matrix.npy', global_matrix)


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

