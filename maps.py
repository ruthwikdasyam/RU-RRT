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
window = pygame.display.set_mode((1200,800)) # window size
window.fill(white) # filling it with color


# LOOP to transform matrix into this window
for i in range(1200):
    for j in range(800):
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
