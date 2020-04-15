import pygame
from math import sin, radians, degrees, copysign
from random import randint, uniform
from pygame.math import Vector2 as vec
from tilemap import *
from math import sin, radians, degrees, copysign
#from tilemap import collide_hit_rect
################
MAX_SPEED = 2
MAX_FORCE = 0.5
APPROACH_RADIUS = 5
#################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

class Car(pygame.sprite.Sprite):
    def __init__(self,game, coordinate):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.car_image
        self.rect = self.image.get_rect()
        self.lista = self.initcoord(coordinate)
        self.pos = self.lista[0]
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.index = 0
        
        

    def initcoord(self, coordinate):
        lista = []
        for tile_object in coordinate:
            #/2 perchè la mappa è stata generata al doppio della risoluzione
            #schermo e poi ridotta
            lista.append(vec(tile_object.x / 2, tile_object.y / 2))
        return lista

    
    def seek_with_approach(self, target):
        target1 = target[self.index]
        self.desired = (target1 - self.pos)
        dist = self.desired.length()
        if dist < APPROACH_RADIUS:
            self.index += 1
            if self.index == len(target):
                self.kill()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        self.rot = round(self.desired.angle_to(vec(1,0)))
        return steer

    def update(self):
        
        self.acc = self.seek_with_approach(self.lista[1:])
        self.image = pygame.transform.rotate(self.game.car_image, self.rot)
        self.image90 = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.vel += self.acc 
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos
        self.get_direction()
        self.vision_rect = self.creavisione()
        

    def get_direction(self):
        
        if self.rot in range(-3,3):
           self.direzione = "EST"
        elif self.rot in range(88,92):
           self.direzione = "NORD"
        elif self.rot in range(-92,-88):
           self.direzione = "SUD"
        elif abs(self.rot) in range(178,182):
           self.direzione = "OVEST"

    def creavisione(self):

        if self.direzione == 'EST':
            return pygame.Rect((self.rect.topright[0], self.rect.topright[1] - 14), self.image90.get_size())
        elif self.direzione == 'OVEST':
            return pygame.Rect((self.rect.topleft[0] - (self.image.get_size())[1], self.rect.topleft[1] - 14), self.image90.get_size())
        elif self.direzione == 'NORD': 
            return pygame.Rect((self.rect.topleft[0] - 20, self.rect.topleft[1] - (self.image.get_size())[0]), self.image90.get_size())
        elif self.direzione == 'SUD':
            return pygame.Rect((self.rect.bottomleft[0] - 20, self.rect.bottomleft[1]), self.image90.get_size())
        
    def draw_vectors(self):
        scale = 25
        # vel
        pygame.draw.line(self.game.screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pygame.draw.line(self.game.screen, RED, self.pos, (self.pos + self.desired * scale), 5)
        # approach radius
        pygame.draw.circle(self.game.screen, WHITE, pygame.mouse.get_pos(), APPROACH_RADIUS, 1)
    
    def draw_rect(self):

        pygame.draw.rect(self.game.screen, WHITE, self.rect)
        pygame.draw.rect(self.game.screen, RED, self.vision_rect)