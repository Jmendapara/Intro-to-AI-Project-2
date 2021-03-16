import pygame
import time
'''
The pygame GUI that does not allow for user inputs
**inputs:
size = size of the grid
grid_main = the main grid to check against
grid = the grid to be updated and displayed
moveOrder = the order of moves that the AI solved our maze with
**returns:
Nothing (just visuals)
'''

#Some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (200,200,200)
YELLOW = (255,255,0)

#Set the Height and Width of our grid cells
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


def drawGrid():

    for x in range(WINDOW_WIDTH):
        for y in range(WINDOW_HEIGHT):
            rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE,
                               BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

def game(size, grid_main, grid, moveOrder):


    global SCREEN, CLOCK, SIZE, BLOCK_SIZE
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()
    SIZE = size
    BLOCK_SIZE = WINDOW_HEIGHT/SIZE
    SCREEN.fill(BLACK)


    #Set our font
    font = pygame.font.SysFont("comicsansms", 20)

    #load in our images
    flag_img = pygame.image.load("Flag.png")
    flag_img = pygame.transform.scale(flag_img, (int(BLOCK_SIZE),int(BLOCK_SIZE)))
    bomb_img = pygame.image.load("bomb.png")
    bomb_img = pygame.transform.scale(bomb_img, (int(BLOCK_SIZE),int(BLOCK_SIZE)))

    update = []

    while (len(moveOrder) > 0):

        drawGrid()

        coor = moveOrder.pop(0)

        x, y = coor[0], coor[1]


        if grid[x][y] == -1:

            rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, YELLOW, rect)

            text = font.render("flag", True, (0,0,0))
            update.append((flag_img, x*BLOCK_SIZE, y*BLOCK_SIZE))

        elif grid[x][y] == -2:

            rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, RED, rect)

            text = font.render("bomb", True, (0,0,0))
            update.append((bomb_img, x*BLOCK_SIZE, y*BLOCK_SIZE))

        else:

            rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect)

            text = font.render(str(int(grid[x][y])), True, (0,0,0))
            update.append((text, x*BLOCK_SIZE, y*BLOCK_SIZE))


        #for event in pygame.event.get():



            #if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()

            
        for item in update:
            SCREEN.blit(item[0], (item[1], item[2]))
            pygame.display.flip()
            

        pygame.display.update()

