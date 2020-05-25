import pygame, os
from math import sin, radians, degrees, copysign
from random import randint, uniform
from pygame.math import Vector2 as vec
from tilemap import *
from math import sin, radians, degrees, copysign
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
signal_list = ["red.png","green.png", "yellow.png"]

class Traffic_Light(pygame.sprite.Sprite):
    def __init__(self, game, lista):
        self.groups = game.trfl
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.init(lista)
        self.image = pygame.image.load(os.path.join(game.img_folder, "red.png"))
        self.image = pygame.transform.scale(self.image, (31, 81)).convert_alpha()
        self.rect = self.image.get_bounding_rect()
        self.rect.center = self.pos
        self.color = 'red'
        self.index = 0
        self.active = False 
        
    
    def init(self, coordinate):
        for tile_object in coordinate:
            if tile_object.name == 'linea':
                self.rect_linea = pygame.Rect(tile_object.x / 2,tile_object.y / 2, tile_object.width / 2, tile_object.height / 2)
            elif tile_object.name == 'punto':
                self.pos = (tile_object.x / 2,tile_object.y / 2)
            else:   
                self.rect_lane = pygame.Rect(tile_object.x / 2,tile_object.y / 2, tile_object.width / 2, tile_object.height / 2)
        self.timer_event = pygame.USEREVENT + len(self.groups)
        self.event_time = 3000
        pygame.time.set_timer((pygame.USEREVENT + len(self.groups)), self.event_time)

    def traffic_detector(self):
        listcar = self.game.all_sprites.sprites()
        a = self.rect_lane.collidelistall(listcar)
        #print(len(a))
        return len(a)

    def change_sign(self):
        #self.traffic_detector()
        self.contatore()
        color = signal_list[self.index]
        self.image = pygame.image.load(os.path.join(self.game.img_folder,color))
        self.image = pygame.transform.scale(self.image, (31, 81)).convert_alpha()
        if self.index == 0:
            self.color = 'red'
            self.game.signal_counter += 1
        elif self.index == 1:
            self.color = 'green'
        elif self.index == 2:
            self.color = 'yellow'  
            

    def time_setter(self,seconds):
        self.event_time = seconds
        pygame.time.set_timer(self.timer_event,self.event_time)
    
    def update(self,events):
        if self.active:      
            for event in events:
                if event.type == self.timer_event:
                    self.change_sign()
                self.active = False 

    def contatore(self):
         self.index += 1
         if self.index > 2:
            self.index = 0
         

    def draw_rect(self):
        pygame.draw.rect(self.game.screen, WHITE, self.rect)



class Car(pygame.sprite.Sprite):
    def __init__(self,game, coordinate):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.car_image
        self.rect = self.image.get_bounding_rect()
        self.lista = self.initcoord(coordinate)
        self.pos = self.lista[0]
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.index = 0
        self.vision_rect = None
        self.start_time = pygame.time.get_ticks()
        

 

    def initcoord(self, coordinate):
        lista = []
        for tile_object in coordinate:
            #/2 perchè la mappa è stata generata al doppio della risoluzione
            #schermo e poi ridotta
            lista.append(vec(tile_object.x / 2, tile_object.y / 2))
        return lista

    def controllosemaforo(self, listasemafori):
        for s in listasemafori:
            if self.vision_rect != None:
                 if s.color == 'red':
                     if self.vision_rect.colliderect(s.rect_linea):
                         self.vel = vec(0,0)
                         self.acc = vec(0,0)
                         break
                 elif s.color == 'yellow':
                     if self.vision_rect.colliderect(s.rect_linea):
                         if self.car_incrocio >= 2:
                            self.vel = vec(0,0)
                            self.acc = vec(0,0)
                         else:
                             self.vision_rect = self.creavisione(36,1)
                             self.anticollisione()
                         break
                 elif s.color == 'green':
                     if self.vision_rect.colliderect(s.rect_linea):
                        if  self.car_incrocio >= 3:
                            self.vel = vec(0,0)
                            self.acc = vec(0,0)
                        else:
                            self.vision_rect = self.creavisione(36,1)
                            self.anticollisione()
                        break

    def controlloincrocio(self):
        listcar = self.groups.sprites()
        a = self.game.centro_rect.collidelistall(listcar)
        #print(len(a))
        return len(a)


    def seek_with_approach(self, target):
        target1 = target[self.index]
        self.desired = (target1 - self.pos)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * MAX_SPEED
            self.index += 1
            if self.index == len(target):
                self.time_since_enter = pygame.time.get_ticks() - self.start_time
                self.game.time.append(pygame.time.get_ticks()/1000)
                self.game.life.append(self.time_since_enter/1000) #conversione a secondi 
                self.kill()
        else:
            self.desired *= MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        self.rot = round(int(self.desired.angle_to(vec(1,0))))
        return steer

    def update(self):
        
        self.acc = self.seek_with_approach(self.lista[1:])
        self.image = pygame.transform.rotate(self.game.car_image, self.rot).convert_alpha()
        self.image90 = pygame.transform.rotate(self.image, 90).convert_alpha()
        self.rect = self.image.get_bounding_rect()
        self.x = (self.game.centro_pos - self.pos)
        if self.x.length() < 40:
            self.vision_rect = self.creavisione(25,1.2)
        else:
            self.vision_rect = self.creavisione(15,2)
        self.anticollisione()
        self.car_incrocio = self.controlloincrocio()
        self.controllosemaforo(self.game.trfl)
        self.vel += self.acc 
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos
        
        
        
    def anticollisione(self):
            for car in self.groups:
                if car != self and car.vision_rect != None:
                     if self.vision_rect.colliderect(car.rect):
                         self.vel = vec(0,0)
                         self.acc = vec(0,0)
                         break
                     elif self.vision_rect.colliderect(car.vision_rect):
                         a = self.left_right(self.desired, car.desired)
                         if a > 0:
                            self.vel = vec(0,0)
                            #self.acc = vec(0,0)



    def left_right(self, A, B):
        return -A.x * B.y + A.y * B.x
        #    if return a > 0
        #    "b on the right of a"
        #    if return a < 0
        #    "b on the left of a"
        #    if a == 0
        #    b parallel/antiparallel to a



    def creavisione(self,x, y):
        value = [x / y for x in self.image90.get_size()]
        a = pygame.Rect((self.pos + self.desired), value)
        a.center = self.pos + self.desired * x
        return a

    def draw_vectors(self):
        scale = 25
        pygame.draw.line(self.game.screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pygame.draw.line(self.game.screen, RED, self.pos, (self.pos + self.desired * scale), 5)
        # approach radius
        pygame.draw.circle(self.game.screen, WHITE, pygame.mouse.get_pos(), APPROACH_RADIUS, 1)
    
    def draw_rect(self):

        #pygame.draw.rect(self.game.screen, WHITE, self.game.centro_rect)
        pygame.draw.rect(self.game.screen, WHITE, self.rect)
        if self.vision_rect != None:
            pygame.draw.rect(self.game.screen, RED, self.vision_rect)