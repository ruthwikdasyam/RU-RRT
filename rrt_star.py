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
            # for k in range(12):
                matrix[i,j]=1         # 1 means obstacle

# _____________________ End of Defining Obstacle Space __________________________



# def rrt_star(start, goal):
#     pass

start_node = []
goal_node = []









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
                window.set_at((i,199-j),red)
            elif matrix[i,j]==2: # 2-> black showing bloating part
                window.set_at((i,199-j),black)
            elif matrix[i,j]==5:
                window.set_at((i,199-j),grey)

pygame.display.flip() #updating window
# ____________________ End of Display Pygame Window _______________________



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