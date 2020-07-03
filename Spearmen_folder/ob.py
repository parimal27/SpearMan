import pygame
import random
import time
pygame.init()
BG_X = 1104
BG_Y = 600
SPEARMAN_WIDTH = 128
SPEARMAN_HEIGHT = 150
USER_SPACE = 1104 // 3
screen = pygame.display.set_mode((BG_X, BG_Y))
run = True
SPEARMAN_LEFT = pygame.image.load('./images/spearman11.png')
SPEARMAN_RIGHT = pygame.image.load('./images/spearman12.png')
BACKGROUND = pygame.image.load('./images/bg.png')
POINTER = pygame.image.load('./images/pointer.png')
user_x = random.randrange(30, USER_SPACE-170)
user_y = random.randrange(20, BG_Y-180)
temp = user_y + SPEARMAN_HEIGHT
cordinates = []
for i in range(0, SPEARMAN_HEIGHT, 6):
    size = (user_x + SPEARMAN_WIDTH + 7, temp)
    temp -= 6
    cordinates.append(size)
sys_x = random.randrange(USER_SPACE*2, BG_X-140)
sys_y = random.randrange(20, BG_Y-180)
pygame.display.update()
while run:
    
    screen.fill((255, 255, 255))
    screen.blit(BACKGROUND,(0,0))
    screen.blit(SPEARMAN_LEFT, (user_x,user_y))
    screen.blit(SPEARMAN_RIGHT, (sys_x,sys_y))
    rect = pygame.draw.rect(screen, (0, 0, 0), (cordinates[0][0], cordinates[0][1], 10, 10), 0)
    for i in cordinates:
        # screen.blit(POINTER, i)
        rect.move_ip(i)
        pygame.display.update()
        time.sleep(0.5)
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            run = False
        if event.type == pygame.KEYUP:
                print(event.key)
    pygame.display.update()
pygame.quit()