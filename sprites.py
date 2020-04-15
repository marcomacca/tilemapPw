import pygame
from math import sin, radians, degrees, copysign
from random import randint, uniform
from pygame.math import Vector2 as vec
from tilemap import *
from math import sin, radians, degrees, copysign
#from tilemap import collide_hit_rect
################
MAX_SPEED = 5
MAX_FORCE = 1
APPROACH_RADIUS = 10
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
            #/2 perchè la mappa è stata generata al doppio della risoluzione schermo e poi ridotta
            lista.append(vec(tile_object.x/2, tile_object.y/2))
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
        self.rot = self.desired.angle_to(vec(1,0))
        return steer

    def update(self):
        
        self.acc = self.seek_with_approach(self.lista[1:])
        self.image = pygame.transform.rotate(self.game.car_image, self.rot)
        self.rect = self.image.get_rect()
        # equations of motion
        self.vel += self.acc 
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos

    def draw_vectors(self):
        scale = 25
        # vel
        pygame.draw.line(self.game.screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pygame.draw.line(self.game.screen, RED, self.pos, (self.pos + self.desired * scale), 5)
        # approach radius
        pygame.draw.circle(self.game.screen, WHITE, pygame.mouse.get_pos(), APPROACH_RADIUS, 1)

    #def get_keys(self):
    #  # User input
    #   pressed = pygame.key.get_pressed()
    #   if self.position.x * 32 < self.obj.x:
    #       if self.velocity.x < 0:
    #           self.acceleration = self.brake_deceleration
    #       else:
    #           self.acceleration += 1 * self.game.dt
    #   elif self.position.x * 32 > self.obj.x:
    #       if self.velocity.x > 0:
    #           self.acceleration = -self.brake_deceleration
    #       else:
    #           self.acceleration -= 1 * self.game.dt
    #   elif pressed[pygame.K_SPACE]:
    #       if abs(self.velocity.x) > self.game.dt * self.brake_deceleration:
    #           self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
    #       else:
    #           self.acceleration = -self.velocity.x / self.game.dt
    #   else:
    #       if abs(self.velocity.x) > self.game.dt * self.free_deceleration:
    #           self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
    #       else:
    #           if self.game.dt != 0:
    #               self.acceleration = -self.velocity.x / self.game.dt
    #   self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    #   if pressed[pygame.K_RIGHT]:
    #       self.steering -= 30 * self.game.dt
    #   elif pressed[pygame.K_LEFT]:
    #       self.steering += 30 * self.game.dt
    #   else:
    #       self.steering = 0
    #   self.steering = max(-self.max_steering, min(self.steering, self.max_steering))    
