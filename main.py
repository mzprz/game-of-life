import pygame
import sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
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
    grid = [[0 for x in range(GRID_NO)] for y in range(GRID_NO)]  # use array for grid: 0=white, 1=black
    basicX = WINDOW_WIDTH / GRID_NO
    basicY = WINDOW_HEIGHT / GRID_NO

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
                pygame.draw.rect(SCREEN, color, (xInGrid * basicX+1, yInGrid * basicY+1, basicX-2, basicY-2))  # draw rectangle
                pygame.display.flip()  # update screen
                # print("CLICK")


            if event.type == pygame.MOUSEBUTTONUP:
                clicking = 0
                # print("NOT CLICK")

            if event.type = pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = 1 - start
                    

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
