import pygame
import random
import time
import Spearmen 
import math
import queue
import threading
pygame.init()
BG_WIDTH = 1104
BG_HEIGHT = 600
SPEARMAN_WIDTH = 85
SPEARMAN_HEIGHT = 100
USER_SPACE = 1104 // 3
screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))
SPEARMAN_LEFT = pygame.image.load('./images/spearman12.png')
HEART_SMALL = pygame.image.load('./images/heartsmall.png')
LIFE_IMAGE = pygame.image.load('./images/heart.png')
SPEARMAN_RIGHT = pygame.image.load('./images/spearman11.png')
SPEAR = pygame.image.load('./images/ss.png')
BACKGROUND = pygame.image.load('./images/bg.png')
POINTER = pygame.image.load('./images/pointer.png')
LIFE = 3
HIT = 2
(x, y) = random.randint(USER_SPACE, USER_SPACE+USER_SPACE),random.randint(USER_SPACE, USER_SPACE+USER_SPACE)
q = queue.Queue()
def main():
    CHECKCOLIDE = pygame.USEREVENT + 1
    pygame.time.set_timer(CHECKCOLIDE, 3)
    LEVEL1 = pygame.USEREVENT + 2
    pygame.time.set_timer(LEVEL1, 5500)
    LIFE_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(LIFE_EVENT, 6000)
    run = True
    main_object =  Spearmen.Main()
    spear1 = Spearmen.Spear(0, 0, SPEAR)
    spear2 = Spearmen.Spear(0, 0, SPEAR)
    user_x = random.randrange(30, USER_SPACE-170)
    user_y = random.randrange(20, BG_HEIGHT-180)
    user_spearman = Spearmen.UserSpearMan(user_x, user_y, LIFE, spear1, SPEARMAN_LEFT, 0)


    sys_x = random.randrange(USER_SPACE*2, BG_WIDTH-140)
    sys_y = random.randrange(20, BG_HEIGHT-180)
    system_spearman = Spearmen.SystemSpearMan(sys_x, sys_y, HIT, spear2, SPEARMAN_RIGHT)

    start_pointer_location = user_y + SPEARMAN_HEIGHT + 10

    cordinates = []
    R = 80 # Radius of circle
    (user_mid_x,user_mid_y) = (user_x + SPEARMAN_WIDTH // 2, user_y + SPEARMAN_HEIGHT // 2)
    (x, y) = (user_mid_x, user_mid_y)
    
    for i in range(-90,90,3):
        (x_new, y_new) = (x + R * math.cos(math.radians(i)), y + R * math.sin(math.radians(i)))
        cordinates.append((x_new, y_new))

    count = 0
    clock = pygame.time.Clock()
    # thread_for_life = threading.Thread(target=main_object.add_life_random, args=(screen, LIFE_IMAGE, USER_SPACE,))
    # thread_for_life.start()
    system_spearman.calculate_spear_direction(SPEARMAN_WIDTH, SPEARMAN_HEIGHT, user_mid_x, user_mid_y, SPEAR,screen,)
    display_life = False
    while run:
        screen.fill((255, 255, 255))
        screen.blit(BACKGROUND,(0,0))
        screen.blit(SPEARMAN_LEFT, (user_spearman.x, user_spearman.y))
        screen.blit(SPEARMAN_RIGHT, (system_spearman.x, system_spearman.y))
        screen.blit(POINTER, cordinates[count])
        user_spearman.display_life(screen, HEART_SMALL)
        fonts = pygame.font.Font('./images/CourierPrime-Bold.ttf', 32) 
        fonts = fonts.render("Score:"+str(user_spearman.score), True, (0, 0, 0))
        screen.blit(fonts, fonts.get_rect())
        if display_life:
            screen.blit(LIFE_IMAGE, (x, y))
        # time.sleep(0.01)
        count += 1
       
        if count == len(cordinates):
            count = 0
            cordinates.reverse()
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                run = False
            elif event.type == CHECKCOLIDE:
                if Spearmen.Main().check_spearmen_hit(system_spearman, user_spearman):
                    if system_spearman.hit == 0:
                        sys_x = random.randrange(USER_SPACE*2, BG_WIDTH-140)
                        sys_y = random.randrange(20, BG_HEIGHT-180)
                        system_spearman.hit = 2
                        system_spearman.x = sys_x
                        system_spearman.y = sys_y
                        system_spearman.calculate_spear_direction(SPEARMAN_WIDTH, SPEARMAN_HEIGHT, user_mid_x, user_mid_y, SPEAR,screen,)
                    elif user_spearman.life == 0:
                            screen.fill((255,255,255))
                            screen.blit(BACKGROUND,(0,0))
                            screen.blit(SPEARMAN_LEFT, (user_spearman.x, user_spearman.y))
                            screen.blit(SPEARMAN_RIGHT, (system_spearman.x, system_spearman.y))
                            fonts = pygame.font.Font('./images/CourierPrime-Bold.ttf', 60) 
                            fonts = fonts.render("Game Over", True, (0, 0, 0))
                            screen.blit(fonts, fonts.get_rect())
                            pygame.display.update()
                            run = False
                            pygame.time.wait(1000)
            elif event.type == LIFE_EVENT:
                # if random.randint(0,1):
                if display_life:
                    display_life = False
                else:
                    display_life = True
                    (x, y) = random.randint(USER_SPACE, USER_SPACE+USER_SPACE),random.randint(USER_SPACE, USER_SPACE+USER_SPACE)
            elif event.type == LEVEL1:
                th = threading.Thread(target = system_spearman.throw_spear, args=(screen,))
                th.start()
                q.put(th)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # x_cor = cordinates[count][0]
                    # y_cor = cordinates[count][1]
                    # rad = math.atan2((user_y + SPEARMAN_HEIGHT // 2) - y_cor, (user_x + SPEARMAN_WIDTH // 2) - x_cor)
                    # print((SPEARMAN_WIDTH // 2, SPEARMAN_HEIGHT // 2), (user_x, user_y), (user_x + SPEARMAN_WIDTH // 2,user_y + SPEARMAN_HEIGHT // 2),(cordinates[count]))
                    (X, Y) = cordinates[count]
                    (X, Y) = (X, Y)
                    rad = math.atan2(Y - user_mid_y, X - user_mid_x)
                    # mydegrees = math.degrees(rad)
                    print("angle:", math.degrees(rad))
                    H = 20 # Hypotenuse length
                    (x_new, y_new) = (X, Y)
                    spear_cor = []
                    for _ in range(80):
                        (x_new,y_new) = (int(x_new + H * math.cos(rad)), int(y_new + H * math.sin(rad)))
                        if x_new > BG_WIDTH or y_new > BG_HEIGHT:
                            break
                        spear_cor.append((x_new, y_new))
                    # print(spear_cor)
                    deg = math.degrees(rad)
                    s = pygame.transform.rotate(SPEAR, -1*deg)
                    th = threading.Thread(target=user_spearman.throw_spear, args=(screen, s, spear_cor,))
                    th.start()
                    q.put(th)
                    
        pygame.display.update()
        if not q.empty():
            q.get().join(0.0000002)
        pygame.time.wait(60)
        clock.tick(100)
    pygame.quit()

main()
