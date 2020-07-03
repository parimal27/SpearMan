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
RESTART = pygame.image.load('./images/restart.png')
START = pygame.image.load('./images/start.png')
HEART_SMALL = pygame.image.load('./images/heartsmall.png')
LIFE_IMAGE = pygame.image.load('./images/heart.png')
SPEARMAN_RIGHT = pygame.image.load('./images/spearman11.png')
SPEAR = pygame.image.load('./images/ss.png')
BACKGROUND = pygame.image.load('./images/bg.png')
POINTER = pygame.image.load('./images/pointer.png')
LIFE = 3
HIT = 2