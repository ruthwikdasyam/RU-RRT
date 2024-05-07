import pygame
import numpy as np


# _____________________ Defining Obstacle Space __________________________
print("\n****************** Map *****************")

# print("Input Clearence Value ---")
# clearence = int(input(" "))
clearence = 5


print(" Please wait, Preparing Map ..... ")

# -- Returns value >= 1, if a point is in obstacle space
def obstacle(x,y):
    # y=199-y 
    if x>=60 and x<=90 and y>=230 and y<=260:   # box1
        return True
    if x>=150 and x<=152 and y>=0 and y<=180:    # line1
        return True
    if x>=210 and x<=240 and y>=60 and y<=90:   # box2.1
        return True
    if x>=210 and x<=240 and y>=230 and y<=260: # box2.2
        return True       
    if x>=300 and x<=302 and y>=120 and y<=400: # line2
        return True
    if x>=360 and x<=390 and y>=60 and y<=90:   # box3.1
        return True
    if x>=360 and x<=390 and y>=230 and y<=260: # box3.2
        return True
    if x>=450 and x<=452 and y>=0 and y<=180:    # line3
        return True
    if x>=510 and x<=540 and y>=60 and y<=90:   # box4.1
        return True
    if x>=510 and x<=540 and y>=230 and y<=260: # box4.2
        return True

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
