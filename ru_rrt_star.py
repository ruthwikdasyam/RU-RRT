from rrt_star_utils import *
import copy


# # _____________________ Defining Obstacle Space - Type 1 __________________________
# print("\n****************** Map *****************")

# # print("Input Clearence Value ---")
# # clearence = int(input(" "))
# clearence = 5

# width = 600
# height = 400

# print(" Please wait, Preparing Map ..... ")

# # -- Returns value >= 1, if a point is in obstacle space
# def obstacle(x,y):
#     # y=199-y 
#     if x >= 150 and x < 175 and y >= 200:  
#         return True             # 1st obstacle
#     if x >= 250 and x < 275 and y < 100:
#         return True             # 2nd obstacle
#     if (x - 420)**2 + (y-120)**2 <= 3600:  
#         return True             # equations for lines that surround polygon
#     else: 
#         return False            
 

# matrix = np.zeros((width,height))         # Defining a matrix representing canvas 1200 x 500 with zeros

# for i in range(width):                    # looping through all elements in matrix
#     for j in range(height):
#         if obstacle(i,j):               # checking if point is in obstacle space
#             matrix[i,j]=1               # 1 means obstacle
# # _____________________ End of Defining Obstacle Space __________________________


# _____________________ Defining Obstacle Space - Type 2 __________________________
print("\n****************** Map *****************")

# print("Input Clearence Value ---")
# clearence = int(input(" "))
clearence = 5
width = 1200
height = 800

print(" Please wait, Preparing Map ..... ")

# -- Returns value >= 1, if a point is in obstacle space
def obstacle(x,y):
    # y=199-y 
    if x>=120 and x<=180 and y>=460 and y<=520:     # box1
        return True
    if x>=300 and x<=315 and y>=0 and y<=360:       # line1
        return True
    if x>=420 and x<=480 and y>=120 and y<=180:     # box2.1
        return True
    if x>=420 and x<=480 and y>=460 and y<=520:     # box2.2
        return True       
    if x>=600 and x<=615 and y>=240 and y<=800:     # line2
        return True
    if x>=720 and x<=780 and y>=120 and y<=180:     # box3.1
        return True
    if x>=720 and x<=780 and y>=460 and y<=520:     # box3.2
        return True
    if x>=900 and x<=915 and y>=0 and y<=360:       # line3
        return True
    if x>=1020 and x<=1080 and y>=120 and y<=180:   # box4.1
        return True
    if x>=1020 and x<=1080 and y>=460 and y<=520:   # box4.2
        return True

matrix = np.zeros((1200,800))         # Defining a matrix representing canvas 1200 x 500 with zeros

for i in range(1200):                    # looping through all elements in matrix
    for j in range(800):
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
window = pygame.display.set_mode((width,height)) # window size
window.fill(white) # filling it with color


# LOOP to transform matrix into this window
for i in range(width):
    for j in range(height):
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
local_matrix = np.empty((width,height), dtype=object)
# make all elements of local_matrix as empty arrays
local_matrix.fill([])



# import flow_matrix
global_matrix = np.load('flow_matrix.npy', allow_pickle=True)
query_trees = np.load('query_trees.npy', allow_pickle=True)

# _____________________ Defining Start and Goal __________________________

start = (100,350)
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
def delete_branches(node, node_dict):
    for child in node.children:        
        delete_branches(node_dict[child], node_dict)
    # graph.remove(node)
    pygame.draw.line(window, white, node.state, node.parent)
    del node_dict[node.state]


# adding tree to the node dict
def add_tree(other_map, start, diff_in_c2c, node_dict, new_tree_states):
    # add all the nodes of other map dict to  node_dict
    for i in other_map[start].children:
        print("adding  ",len(other_map[start].children))
        print(i)
        print(other_map[i])
        # adding to current node_dict
        # node_dict[i] = Node(i, other_map[i].parent, other_map[i].c2c)
        try:
            if node_dict[i]:
                # delete this chilren for its parent
                need_to_update_parent_state = other_map[i].parent
                node_dict[need_to_update_parent_state].children.remove(node_dict[i].state) 


                continue
        except KeyError:


            node_dict[i] = copy.deepcopy(other_map[i])
            node_dict[i].ext = 1
            # updating costs
            node_dict[i].c2c -= diff_in_c2c
            # appending to graph
            # graph.append(node_dict[i])
            new_tree_states.append(node_dict[i].state)
            pygame.draw.line(window, (100, 250, 50), node_dict[i].state, node_dict[i].parent)
        
        add_tree(other_map, i, diff_in_c2c, node_dict, new_tree_states)

    return new_tree_states
    

focus_nodes_list=[]
cleared_trees_list=[]

def rrt_star(start, goal):
    global step
    global goal_threshold
    start_node = Node(start, None, 0)

    # graph=[]
    # graph.append(start_node)

    global node_dict
    node_dict[start] = start_node

    goal_reached = False
    n=0
    while True:
        # generate a list with node_dict values
        graph = list(node_dict.values())

        # Generate random node
        # Find nearest node
        rand_point1 = get_random_state(graph, step)

        # find new point in corresponding direction
        
        # check if the point is in obstacle space and continue if true
        if not 0<= rand_point1[0] < width or not 0<= rand_point1[1] < height:
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
        if not path_ok:
            continue


        # if len(neighs)>0:
        #     new_node = Node(rand_point1, nearest_c2c.state, nearest_c2c.c2c+step)
        # else:
        #     new_node = Node(rand_point1, nearest_node.state, nearest_node.c2c+step)

        # check if the path to the new node is in obstacle space and continue if true
        # path_ok = path_check(new_node.state, new_node.parent)
        # if not path_ok:
        #     continue

        # graph.append(new_node)

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

                    print("parent error: ", node_dict[i.parent])
                    print(node_dict[i.parent].children)
                    print("state error: ", node_dict[i.state])
                    # remove the node from the children of the parent node
                    if i.state in node_dict[i.parent].children:
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
            if in_goal_radius(rand_point1, goal, goal_threshold):
                print("Goal Reached")
                path = back_track(node_dict, new_node, start)
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
                path = back_track(node_dict, goal_node, start)
                print_path(path, black, window)
                print(goal_node.c2c)
            
            if no_prints ==10:
                return path

        # n +=1
        # if n == 250:
        #    break

        # Reuse RRT* Algorithm____________________________________________________

        if new_node.great_grand_parent(node_dict):
            focus_state = new_node.great_grand_parent(node_dict)
            # print(focus_state)
            focus_node = node_dict[focus_state]

            # checking if it has parent
            if focus_node.parent is not None:
             if focus_node.ext == 0:  
            #   print("focus node  ", focus_node)
            #   print("focus node  parent ", node_dict[focus_node.parent])
            #   print("focus node  parent ka children ", node_dict[focus_node.parent].children)


            # checking eligibility for flow
              if focus_node.flow_value(node_dict) is not None:
                focus_node_flow = focus_node.flow_value(node_dict) # get flow value of the focus node, check if we need to take node or its parent !!!
                # Get quotient of the flow value
                focus_node_flow_ = focus_node_flow//15
                # checking sub tree size of the focus node
                sub_tree_size = focus_node.subtree_size(node_dict) # get subtree size of the focus node

                probable_trees=[]
                flow_check_radius = int(distance(focus_node.state, focus_node.parent)-1) # get flow check radius
                # get list of all states in the flow check radius fom the focus state
                for i in range(focus_state[0]-flow_check_radius, focus_state[0]+flow_check_radius):
                    for j in range(focus_state[1]-flow_check_radius, focus_state[1]+flow_check_radius):
                        if 0<=i<width and 0<=j<height:
                            radius = np.sqrt((i-focus_state[0])**2 + (j-focus_state[1])**2)
                            if radius <= flow_check_radius:
                              if len(global_matrix[i, j, focus_node_flow_]) !=0:
                                probable_trees.append([global_matrix[i, j, focus_node_flow_], (i, j)])
                
                if len(probable_trees) == 0:
                    # if not, add the node_flow to the local matrix
                    local_matrix[focus_state[0], focus_state[1]] = (focus_node_flow, sub_tree_size)
                    # print in pygame
                    pygame.draw.line(window, red, focus_node.state, focus_node.parent)
                    pygame.display.flip()


                # if probable_trees is not empty
                if len(probable_trees) != 0:
                    # [ [map 2, 265], (i , j) ]
                    best_tree = max(probable_trees, key=lambda x: x[0][1])
                    
                    # checking if its helpful to add the best tree to current tree
                    if best_tree[0][1] < 1.5*sub_tree_size:
                        best_tree = None

                    # checking if best tree is None
                    if best_tree is None:
                        # if not, add the node_flow to the local matrix
                        local_matrix[focus_state[0], focus_state[1]] = (focus_node_flow, sub_tree_size)
                        # print in pygame
                        pygame.draw.line(window, red, focus_node.state, focus_node.parent)
                        pygame.display.flip()

                    else:
                        print("Added tree")
                        cleared_trees_list.append(focus_node.state)
                        focus_node.ext = 1

                        # if yes, add the best tree to the local tree
                        #delete all branches of the focus node in the graph
                        focus_parent = focus_node.parent
                        # deleting focus node state from childrens of its parent
                        # node_dict[focus_parent].children.remove(focus_node.state)
                        # print("before deleting branches", node_dict[focus_node.state])
                        # print("before deleting branches focus node parent ", node_dict[focus_node.parent])
                        # delete_branches(focus_node, node_dict)       
                        # print("after deleting branches focus node parent ", node_dict[focus_parent])
                        # print("after deleting branches", node_dict[focus_node.state])
                        focus_nodes_list.append(best_tree[1])
                        # focus_nodes_list.append("ONEIT")
                        print(focus_nodes_list)
                        print(cleared_trees_list)

                        # if there is already a tree in the new tree start node, then we will add them to this new tree
                        try:
                            if node_dict[best_tree[1]]:
                                my_old_children = node_dict[best_tree[1]].children
                                my_old_parent = node_dict[best_tree[1]].parent
                        except KeyError:
                            my_old_children = None
                            pass

                        # update focus node
                        new_focus_node = Node(best_tree[1], focus_parent, node_dict[focus_parent].c2c + distance(focus_parent, best_tree[1]))
                        node_dict[new_focus_node.state] = new_focus_node  
                        # graph.append(new_focus_node)
                        # adding this new one as child , back to its parent
                        node_dict[focus_parent].children.add(best_tree[1])
                        # node_dict[focus_node.state] = focus_node     

                        reusemap_ID = best_tree[0][0] # get the map ID of the best tree
                        other_map = query_trees[reusemap_ID] # get the dict of that map

                        diff_in_c2c = other_map[new_focus_node.state].c2c - new_focus_node.c2c
                        # this focus points, children are updated from importing map start node
                        node_dict[new_focus_node.state].children = copy.deepcopy(other_map[new_focus_node.state].children)
                        node_dict[new_focus_node.state].ext = 1
                        
                        if my_old_children is not None:
                            # new_focus_node_actual_parent = node_dict[my].parent
                            node_dict[my_old_parent].children.remove(best_tree[1])

                            for child in my_old_children:
                                node_dict[my_old_parent].children.add(child)
                                node_dict[child].parent = my_old_parent
                         
                        #empty list to store new tree nodes
                        new_tree_states = []
                        # add the best tree to the graph from start node - (i,j) match
                        add_tree(other_map, new_focus_node.state, diff_in_c2c, node_dict, new_tree_states) # add_tree(tree, start, new_node, graph, node_dict)
                            # need to update the costs and check for goal_reached too
                        for i in new_tree_states:
                            if in_goal_radius(i, goal, goal_threshold):
                                print("Goal Reached in imported tree :) ")
                                path = back_track(node_dict, node_dict[i], start)
                                print_path(path, black, window)
                                goal_node = node_dict[i]
                                goal_cost = goal_node.c2c
                                print(goal_cost)
                                extra_n=0
                                no_prints = 0
                                goal_reached = True

        # if n==1000:
        #     break
        # n+=1

# _____________________ End of RRT* Algorithm __________________________


# ____________________ RRT* Algorithm _______________________
path = rrt_star(start, goal)
# rrt_star(start, goal)

# ____ Draw the explored Graph ______
# for i in graph[1:]:             # skipping the start node, it has no parent
#     pygame.draw.line(window, (0, 0, 255), i.state, i.parent)
#     pygame.display.flip()
    # time.sleep(0.1)

# ____ Draw the path ______

# ____________________ End of RRT* Algorithm _______________________


#______________________ saving node_dict   _______________________
# get the index for which the query_trees is empty
query_id = np.where(query_trees == None)[0][0]
query_trees[query_id] = node_dict
print(query_id)
# save query_trees
np.save('query_trees.npy', query_trees)

# update flow_matrix with local_matrix
# global_matrix = np.load('flow_matrix.npy')
contributions = 0

for i in range(width):
    for j in range(height):
        if len(local_matrix[i,j]) !=0 : # if the local matrix is not empty
            contributions += 1
            k = local_matrix[i,j][0]//15 # quotient of the flow value
            global_matrix[i,j,k] = [query_id, local_matrix[i,j][1]] # [query_id, sub_tree_size]
# save the global_matrix
np.save('flow_matrix.npy', global_matrix)

print(contributions)



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

