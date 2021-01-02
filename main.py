import pygame
import sys
import numpy as np
import time
import copy

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = 600
WINDOW_HEIGHT = WINDOW_SIZE
WINDOW_WIDTH = WINDOW_SIZE
GRID_NO = 30
BLOCK_SIZE = WINDOW_WIDTH/GRID_NO

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()

    pygame.display.set_caption("Conway's Game Of Life")

    SCREEN.fill(WHITE)

    #Grid Creator
    null_state = [[0 for x in range(GRID_NO)] for y in range(GRID_NO)]
    grid = [[0 for x in range(GRID_NO)] for y in range(GRID_NO)]  # use array for grid: 0=white, 1=black
    basicX = WINDOW_WIDTH / GRID_NO
    basicY = WINDOW_HEIGHT / GRID_NO
    saved_state = [[0 for x in range(GRID_NO)] for y in range(GRID_NO)]
    newgrid = [[0 for x in range(GRID_NO)] for y in range(GRID_NO)]

    rects = []
    for y in range(WINDOW_HEIGHT):
        row = []
        for x in range(WINDOW_WIDTH):
            row.append(pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(SCREEN, BLACK, row[x], 1)
        rects.append(row)

    clicking = 0
    start = 0

    while True:
        for event in pygame.event.get():
            if not start:
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION and clicking:
                    x, y = pygame.mouse.get_pos()
                    xInGrid = int(x / basicX)
                    yInGrid = int(y / basicY)
                    if color == BLACK:
                        grid[yInGrid][xInGrid] = 1  # save this point = 1, for screen redraw (if resize)
                    else:
                        grid[yInGrid][xInGrid] = 0

                    # print(xInGrid, yInGrid, grid[yInGrid][xInGrid])
                    pygame.draw.rect(SCREEN, color, (xInGrid * basicX+1, yInGrid * basicY+1, basicX-2, basicY-2))  # draw rectangle
                    pygame.display.flip()
                    # print("CLICK N DRAG")

                elif event.type == pygame.MOUSEBUTTONDOWN:# mouse button down
                    clicking = 1
                    x, y = pygame.mouse.get_pos()
                    xInGrid = int(x / basicX)
                    yInGrid = int(y / basicY)
                    grid[yInGrid][xInGrid] = 1-grid[yInGrid][xInGrid]  # save this point = 1, for screen redraw (if resize)
                    if grid[yInGrid][xInGrid] == 1:
                        color = BLACK
                    else:
                        color = WHITE
                    # print(xInGrid, yInGrid, grid[yInGrid][xInGrid])
                    pygame.draw.rect(SCREEN, color, (xInGrid * basicX+1, yInGrid * basicY+1, basicX-2, basicY-2))  # draw rectangle
                    pygame.display.flip()  # update screen
                    # print("CLICK")


                if event.type == pygame.MOUSEBUTTONUP:
                    clicking = 0
                    saved_state = copy.copy(grid)
                    # print(saved_state)
                    # print("NOT CLICK")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = 1 - start
                    if start:
                        # print(grid[28][28])
                        # print("START")
                        pass
                    else:
                        grid = copy.copy(saved_state)
                        for y in range(len(grid)):
                            for x in range(len(grid[y])):
                                if grid[y][x] == 1:
                                    color = BLACK
                                else:
                                    color = WHITE
                                pygame.draw.rect(SCREEN, color, (x * basicX+1, y * basicY+1, basicX-2, basicY-2))  # draw rectangle
                        pygame.display.flip()  # update screen
                        # print("STOP")

        if start:
            newgrid = copy.deepcopy(null_state)
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    #Rules
                    # print(len(grid), len(grid[y]))
                    sum_1 = 0
                    if x == 0 and y == 0:
                        sum_1 = sum([grid[y][x+1], grid[y+1][x], grid[y+1][x+1]])
                    elif x == 0 and y == len(grid)-1:
                        sum_1 = sum([grid[y-1][x], grid[y][x+1], grid[y-1][x+1]])
                    elif x == len(grid[y])-1 and y == 0:
                        sum_1 = sum([grid[y+1][x], grid[y][x-1], grid[y+1][x-1]])
                    elif x == len(grid[y])-1 and y == len(grid)-1:
                        sum_1 = sum([grid[y-1][x], grid[y][x-1], grid[y-1][x-1]])
                    else:
                        if x == 0:
                            sum_1 = sum([grid[y][x+1], grid[y+1][x], grid[y+1][x+1]])
                            sum_1 += sum([grid[y-1][x]])
                            sum_1 += sum([grid[y-1][x+1]])
                        elif x == len(grid[y])-1:
                            sum_1 = sum([grid[y+1][x]])
                            sum_1 += sum([grid[y][x-1], grid[y-1][x], grid[y-1][x-1]])
                            sum_1 += sum([grid[y+1][x-1]])
                            # print([(x,y+1,grid[y+1][x]),(x-1,y,grid[y][x-1]), (x,y-1,grid[y-1][x]), (x-1,y-1,grid[y-1][x-1]),(x-1,y+1,grid[y+1][x-1])])
                        elif y == 0:
                            sum_1 = sum([grid[y][x+1], grid[y+1][x], grid[y+1][x+1]])
                            sum_1 += sum([grid[y][x-1]])
                            sum_1 += sum([grid[y+1][x-1]])
                        elif y == len(grid)-1:
                            sum_1 = sum([grid[y][x+1]])
                            sum_1 += sum([grid[y][x-1], grid[y-1][x], grid[y-1][x-1]])
                            sum_1 += sum([grid[y-1][x+1]])
                        else:
                            sum_1 = sum([grid[y][x+1], grid[y+1][x], grid[y+1][x+1]])
                            sum_1 += sum([grid[y][x-1], grid[y-1][x], grid[y-1][x-1]])
                            sum_1 += sum([grid[y+1][x-1], grid[y-1][x+1]])

                    if grid[y][x] == 1:
                        rule = 1 if (sum_1==2 or sum_1 ==3) else 0
                    else:
                        rule = 1 if (sum_1==3) else 0

                    newgrid[y][x] = rule

                    if newgrid[y][x] == 1:
                        color = BLACK
                    else:
                        color = WHITE
                    pygame.draw.rect(SCREEN, color, (x * basicX+1, y * basicY+1, basicX-2, basicY-2))  # draw rectangle

            pygame.display.flip()  # update screen
            time.sleep(.3)
            grid = copy.deepcopy(newgrid)


            # if event.type == pygame.VIDEORESIZE:  # screen resized, must adjust grid height, width
            #     width = event.w
            #     height = event.h
            #     basicX = width / numberOfColumns
            #     basicY = height / numberOfRows
            #     #print(width, height)
            #     screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # reset screen with new height, width
            #     screen.fill((255, 255, 255))  # clear screen
            #     drawScreen(screen, grid, basicX, basicY)  # redraw rectangles
            #     pygame.display.flip()  # update screen

        pygame.display.update()

def drawGrid(rects):
    for x in range(WINDOW_WIDTH):
        for y in range(WINDOW_HEIGHT):
            pygame.draw.rect(SCREEN, WHITE, rects[x][y], 1)

if __name__ == '__main__':
    main()
