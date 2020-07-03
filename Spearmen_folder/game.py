"""
Spearmen game.

Handling the display screen and all functions of game.
"""

import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame'])
import pygame

try:
    from constants import *
    
except pygame.error as er:
    print("Image may not able to load: ",er)
    sys.exit(0)

# Thread queue.
q = queue.Queue()


def main():
    """
     Handlilng game functionalites like display screen handling other feature thread.
     :param: None
     :return: None
    """
    try:
        # Setting screen caption.
        pygame.display.set_caption('Spearmen')

        # Generate cordinates for random life.
        (life_x, life_y) = random.randrange(USER_SPACE, USER_SPACE +
                                            USER_SPACE), random.randrange(100, BG_HEIGHT-100)

        # Initialize Check Collide class
        check_collide = Spearmen.CheckCollide()

        # Custom events.

        # Event that check for colision of spear and spearman.
        CHECKCOLLIDE = pygame.USEREVENT + 1
        pygame.time.set_timer(CHECKCOLLIDE, 1)

        # Event that maintain levels.
        LEVEL = pygame.USEREVENT + 2
        pygame.time.set_timer(LEVEL, 5500)

        # Event for random life.
        LIFE_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(LIFE_EVENT, 10000)

        # Run game.
        run = True

        # Initialize cordinates of spear and spearman.
        spear1 = Spearmen.Spear(0, 0, SPEAR)
        spear2 = Spearmen.Spear(0, 0, SPEAR)
        user_x = random.randrange(30, USER_SPACE-170)
        user_y = random.randrange(20, BG_HEIGHT-180)
        user_spearman = Spearmen.UserSpearMan(
            user_x, user_y, LIFE, spear1, SPEARMAN_LEFT, 0)
        sys_x = random.randrange(USER_SPACE*2, BG_WIDTH-140)
        sys_y = random.randrange(20, BG_HEIGHT-180)
        system_spearman = Spearmen.SystemSpearMan(
            sys_x, sys_y, HIT, spear2, SPEARMAN_RIGHT)

        # Find middle point of system spear man.
        (sys_mid_x, sys_mid_y) = (system_spearman.x + SPEARMAN_WIDTH //
                                2 - 100, system_spearman.y + SPEARMAN_HEIGHT // 2)  # 100 (Trial and Error)

        # Initialize Spear pointer location.
        start_pointer_location = user_y + SPEARMAN_HEIGHT + 10

        # Find spear hit cordinates.
        cordinates = []
        R = 80  # Radius of circle
        (user_mid_x, user_mid_y) = (user_x +
                                    SPEARMAN_WIDTH // 2, user_y + SPEARMAN_HEIGHT // 2)
        (x, y) = (user_mid_x, user_mid_y)
        for i in range(-90, 90, 3):
            (x_new, y_new) = (x + R * math.cos(math.radians(i)),
                            y + R * math.sin(math.radians(i)))
            cordinates.append((x_new, y_new))
        iter_cordinate = 0

        # Calculate system spear man spear cordinates.
        system_spearman.calculate_spear_direction(
            SPEARMAN_WIDTH, SPEARMAN_HEIGHT, user_mid_x, user_mid_y, SPEAR, screen,)
        random_spear_index = 0

        # Display random life.
        display_life = False
        wait = False
        while run:
            # Display screen.
            screen.fill((255, 255, 255))
            screen.blit(BACKGROUND, (0, 0))
            # Restart game window.
            while wait:
                screen.fill((255, 255, 255))
                screen.blit(BACKGROUND, (0, 0))
                fonts = pygame.font.Font(
                                './images/CourierPrime-Bold.ttf', 60)
                fonts = fonts.render("Your Score: "+str(user_spearman.score), True, (177, 53, 53))
                screen.blit(fonts, fonts.get_rect(topleft=(300, 150)))
                screen.blit(RESTART, (360, 233))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RESTART.get_rect(topleft=(425, 233)).collidepoint(pygame.mouse.get_pos()):
                            wait = False
                            main()
                        
                
            screen.blit(SPEARMAN_LEFT, (user_spearman.x, user_spearman.y))
            screen.blit(SPEARMAN_RIGHT, (system_spearman.x, system_spearman.y))
            screen.blit(POINTER, cordinates[iter_cordinate])

            # Display user spear man life bar.
            user_spearman.display_life(screen, HEART_SMALL)

            # Setting font to display.
            fonts = pygame.font.Font('./images/CourierPrime-Bold.ttf', 32)
            fonts = fonts.render(
                "Score:"+str(user_spearman.score), True, (0, 0, 0))
            screen.blit(fonts, fonts.get_rect())

            # Display life according to display_life (random).
            if display_life:
                screen.blit(LIFE_IMAGE, (life_x, life_y))
                if user_spearman.spear.img.get_rect(topleft=(user_spearman.spear.x, user_spearman.spear.y)
                                                    ).colliderect(LIFE_IMAGE.get_rect(topleft=(life_x, life_y))):
                    user_spearman.life_increment()
                    pygame.mixer.music.load('./images/life.wav')
                    pygame.mixer.music.play(1)
                    display_life = False
                    pygame.time.set_timer(LIFE_EVENT, 20000)

            # Manage spear pointer of user.
            iter_cordinate += 1
            if iter_cordinate == len(cordinates):
                iter_cordinate = 0
                cordinates.reverse()

            # Handle events.
            for event in pygame.event.get():
                if pygame.QUIT == event.type:
                    run = False
                if event.type == CHECKCOLLIDE:
                    # Check for collide.
                    if check_collide.check_spearmen_hit(system_spearman, user_spearman):
                        # If max hit exceeded than again setting random position of system spearman.
                        if system_spearman.hit == 0:

                            # Generate random system spearman and initalize it.
                            sys_x = random.randrange(USER_SPACE*2, BG_WIDTH-140)
                            sys_y = random.randrange(20, BG_HEIGHT-180)

                            system_spearman.hit = 2
                            system_spearman.x = sys_x
                            system_spearman.y = sys_y

                            # Calculte cordinates to hit random.
                            (sys_mid_x, sys_mid_y) = (system_spearman.x + SPEARMAN_WIDTH //
                                                    2 - 100, system_spearman.y + SPEARMAN_HEIGHT // 2)
                            system_spearman.calculate_spear_direction(
                                SPEARMAN_WIDTH, SPEARMAN_HEIGHT, user_mid_x, user_mid_y, SPEAR, screen,)

                        # If user life exceeded than game over.
                        if user_spearman.life == 0:
                            wait = True
                            # pygame.time.wait(1000)

                # Display random life.
                if event.type == LIFE_EVENT:
                    if display_life:
                        display_life = False
                    else:
                        display_life = True
                        (life_x, life_y) = random.randrange(
                            user_mid_x + 50, sys_mid_x - 50), random.randrange(50, BG_HEIGHT - 50)

                # Setting level.
                if event.type == LEVEL:
                    if random_spear_index == 0 or user_spearman.score > 10 or user_spearman.score > 20:
                        level = Spearmen.Level.get_level_list(user_spearman.score)
                        random.shuffle(level)
                        print(level)
                    if random_spear_index != len(level):
                        if level[random_spear_index] == 0:
                            system_spearman.calculate_spear_direction(SPEARMAN_WIDTH, SPEARMAN_HEIGHT, random.randrange(
                                user_mid_x + 50, sys_mid_x - 50), random.randrange(50, BG_HEIGHT - 50), SPEAR, screen,)
                        else:
                            system_spearman.calculate_spear_direction(
                                SPEARMAN_WIDTH, SPEARMAN_HEIGHT, user_mid_x, user_mid_y, SPEAR, screen,)
                        random_spear_index += 1
                    else:
                        random.shuffle(level)
                        random_spear_index = 0
                    # Start thread for system spearman.
                    th = threading.Thread(
                        target=system_spearman.throw_spear, args=(screen,))
                    th.start()
                    q.put(th)

                # If space is click it will fire event for user spearman.
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:

                        (X, Y) = cordinates[iter_cordinate]
                        rad = math.atan2(Y - user_mid_y, X - user_mid_x)
                        H = 20  # Hypotenuse length
                        (x_new, y_new) = (X, Y)

                        spear_cor = []
                        # Generate cordinates for user spear.
                        for _ in range(80):
                            (x_new, y_new) = (int(x_new + H * math.cos(rad)),
                                            int(y_new + H * math.sin(rad)))
                            if x_new > BG_WIDTH or y_new > BG_HEIGHT:
                                break
                            spear_cor.append((x_new, y_new))
                        deg = math.degrees(rad)

                        # Rotate spear image according degree.
                        s = pygame.transform.rotate(SPEAR, -1*deg)

                        # After throw spear handling display spear at every cordinate.
                        th = threading.Thread(
                            target=user_spearman.throw_spear, args=(screen, s, spear_cor,))
                        th.start()
                        q.put(th)

            # Update display.
            pygame.display.update()

            # Join thread.
            if not q.empty():
                q.get().join(0.0000002)

            pygame.time.wait(5)

        pygame.quit()

    except IndexError as err:
        print("Exception: ", err)
        sys.exit(0)
    except OSError as err:
        print("Exception: [Some files not found]", err)
        sys.exit(0)
    except pygame.error as err:
        print("Exception: ", err)
        sys.exit(0)
    except Exception as err:
        print("Exception: ", err)
        sys.exit(0)


if __name__ == "__main__":
    run = True
    while run:
        screen.fill((255, 255, 255))
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(START, (425, 233))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START.get_rect(topleft=(425, 233)).collidepoint(pygame.mouse.get_pos()):
                    run  = False
        pygame.time.wait(40)
    main()
