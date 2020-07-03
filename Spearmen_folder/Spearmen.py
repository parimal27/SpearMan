"""Spearmen classes."""
import time
import pygame
import threading
import math
import random


class Spear:
    """
    Represent Spear.
    """

    def __init__(self, x, y, img):
        """
        Initialize cordinate and spear image.
        :param x: x cordinate.
        :param y: y cordinate.
        :param img: Spear image.
        :return: None.
        """
        self.x = x
        self.y = y
        self.img = img
        self.colide = False


class SpearMan:
    """
    Represent spearman properties and functions.
    """

    def __init__(self, x, y, spear, img):
        """
        Initialize cordinate and spear object.
        :param x: x cordinate.
        :param y: y cordinate.
        :param spear: Spear object.
        :param img: spaerman image.
        :return: None.
        """
        self.x = x
        self.y = y
        self.spear = spear
        self.img = img

    def throw_spear(self):
        pass


class SystemSpearMan(SpearMan):
    """
    Represent system spearman inherited from spearman.
    """

    def __init__(self, x, y, hit, spear, img):
        """
        Initialize cordinate and spear object.
        :param x: x cordinate.
        :param y: y cordinate.
        :param spear: Spear object.
        :param img: spaerman image.
        :param hit: maintain number of hit.
        :return: None.
        """
        super().__init__(x, y, spear, img)
        self.hit = hit
        self.cordinates = []

    def calculate_spear_direction(self, s_width, s_height, user_mid_x, user_mid_y, img, screen):
        """
        Calculate spear direcction and cordinate list.
        :param s_width: spear man width.
        :param s_height: spear man height.
        :param user_mid_x: mid point of user spearman x.
        :param user_mid_y: mid point of user spearman y.
        :param img: image of spear.
        :param screen: screen object.
        :return: None.
        """
        (sys_mid_x, sys_mid_y) = (self.x +
                                  s_width // 2 - 100, self.y + s_height // 2)
        (X, Y) = (user_mid_x, user_mid_y - 15)
        rad = math.atan2(sys_mid_y - Y, sys_mid_x - X)
        H = 20  # Hypotenuse length
        (x_new, y_new) = (sys_mid_x, sys_mid_y)
        sys_spear_cordinates = []
        for _ in range(50):
            (x_new, y_new) = (float(x_new - H * math.cos(rad)),
                              float(y_new - H * math.sin(rad)))
            if x_new <= 0 or y_new <= 0:
                break
            sys_spear_cordinates.append((x_new, y_new))
        deg = math.degrees(rad)
        s = pygame.transform.rotate(img, 180-(deg))
        self.spear.img = s
        self.cordinates = sys_spear_cordinates

    def hit_decrement(self):
        """
        Decrement hit of system spearman.
        """
        self.hit -= 1

    def throw_spear(self, screen):
        """
        Manage motion of spear.
        :param screen: screen object.
        :return: None.
        """
        pygame.mixer.music.load('./images/spear.wav')
        pygame.mixer.music.play(1)
        for i in self.cordinates:
            (self.spear.x, self.spear.y) = i
            screen.blit(self.spear.img, i)
            if self.spear.colide == True:
                self.spear.colide = False
                self.spear.x = 0
                self.spear.y = 0
                break
            time.sleep(0.013)


class UserSpearMan(SpearMan):
    """
    Represent user spearman.
    """

    def __init__(self, x, y, life, spear, img, score):
        """
        Initialize cordinate, spear object and score.
        :param x: x cordinate.
        :param y: y cordinate.
        :param spear: Spear object.
        :param img: spaerman image.
        :param score: score of user.
        :param life: manage life of user spearman.
        :return: None.
        """
        super().__init__(x, y, spear, img)
        self.life = life
        self.score = score

    def display_life(self, screen, life_img):
        """
        Display life bar for user spearman.
        :param screen: screen object.
        :param life_img: life image.
        :return: None.
        """
        distance = 190
        for i in range(self.life):
            screen.blit(life_img, (distance, 0))
            distance += 60

    def life_increment(self):
        """
        Increment life of user spearman by 1.
        :param: None.
        :return: None.
        """
        self.life += 1

    def life_decrement(self):
        """
        Decrement life of user spearman by 1.
        :param: None.
        :return: None.
        """
        self.life -= 1

    def throw_spear(self, screen, spear_img, cordinates):
        """
        Manage motion of system spear.
        :param screen: screen object.
        :param spear_img: image of spear.
        :param cordinates: cordinate list to move spear on.
        :return: None.
        """
        pygame.mixer.music.load('./images/spear.wav')
        pygame.mixer.music.play(1)
        for i in cordinates:
            (self.spear.x, self.spear.y) = i
            self.spear.img = spear_img
            screen.blit(spear_img, i)
            if self.spear.colide == True:
                self.spear.colide = False
                self.spear.x = 0
                self.spear.y = 0
                break
            time.sleep(0.013)

    def increment_score(self):
        """
        Increment score of user spearman by 1.
        :param: None.
        :return: None.
        """
        self.score += 1


class Level:
    """
    Represent levels of game.
    """
    levels = {'1': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], '2': [
        1, 1, 1, 0, 0, 0, 0, 0, 0, 0], '3': [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]}

    @classmethod
    def get_level_list(cls, score):
        """
        Based on score return level dictionary.
        :param cls: class.
        :param score: user spearman score.
        :return: None.
        """
        if 0 <= score <= 10:
            return cls.levels.get('1')
        elif 10 < score <= 20:
            return cls.levels.get('2')
        return cls.levels.get('3')


class CheckCollide:
    """
    Check collide of spear and spearman.
    """
    def check_spearmen_hit(self, system_spearman, user_spearman):
        """
        Check that any spearman hit by spear.
        :param system_spearman: system spearman object..
        :param user_spearman: user spearman object..
        :return: None.
        """
        if system_spearman.img.get_rect(topleft=(system_spearman.x, system_spearman.y)).colliderect(user_spearman.spear.img.get_rect(topleft=(user_spearman.spear.x, user_spearman.spear.y))):
            user_spearman.spear.x = 0
            user_spearman.spear.y = 0
            user_spearman.spear.colide = True
            user_spearman.increment_score()
            system_spearman.hit_decrement()
            pygame.mixer.music.load('./images/pain.wav')
            pygame.mixer.music.play(1)
            return True
        elif user_spearman.img.get_rect(topleft=(user_spearman.x, user_spearman.y)).colliderect(system_spearman.spear.img.get_rect(topleft=(system_spearman.spear.x, system_spearman.spear.y))):
            system_spearman.spear.x = 0
            system_spearman.spear.y = 0
            system_spearman.spear.colide = True
            # system_spearman.increment_score()
            pygame.mixer.music.load('./images/pain.wav')
            pygame.mixer.music.play(1)
            user_spearman.life_decrement()
            # print(user_spearman.hit)
            return True
        return False
