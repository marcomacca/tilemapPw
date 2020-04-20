import os
import pygame
import pytmx
import random
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from tilemap import *
from sprites import *




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Trafic Simulator")
        self.screen = pygame.display.set_mode((0, 0)) #,pygame.FULLSCREEN
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.load_data()

    def load_data(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_folder = os.path.join(current_dir, 'img')
        map_folder = os.path.join(current_dir, 'map')
        car_path = os.path.join(self.img_folder, "car.png")
        map_path = os.path.join(map_folder, "dc.tmx")
        self.map = TiledMap(map_path)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.car_image = pygame.image.load(car_path).convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (64, 32))
        self.lista = []


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.trfl = pygame.sprite.Group()
        self.listacord = self.map.tmxdata.objectgroups
        for tile_object in self.map.tmxdata.objectgroups:
            if 'traffic' in tile_object.name:
                Traffic_Light(self, tile_object)  
            elif 'shape' in tile_object.name:
                a = tile_object
            else:
                self.lista.append(tile_object)

        #for x in self.lista :
        #    Car(self, random.choice(self.lista))
            #self.listaPath.append(tile_object)
        #filtered_numbers = [item for item in self.listaPath if 'A' in
        #item.name ]
        #for x in filtered_numbers:
        #    print(x)



    def run(self):
        # game loop - set self.playing = False to end the game
        self.i = 0
        while not self.exit:
            self.dt = self.clock.tick(self.ticks) / 500.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw() 
            
        pygame.quit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill((0, 0, 0))
        a = pygame.transform.scale(self.map_img, (1920, 1088))
        self.screen.blit(a, (0,0))
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.trfl.draw(self.screen)
        #for l in self.trfl:
        #    l.draw_rect()
        for sprite in self.all_sprites:
            sprite.draw_vectors()
            sprite.draw_rect()
        pygame.display.flip()         


        
   
    def events(self):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == pygame.MOUSEBUTTONUP:
                     Car(self, random.choice(self.lista))
                     if self.i >= 2:
                         self.i = 0
                     else :
                        self.i += 1
                     for a in self.trfl:
                         a.change_sign(self.i)
                #    pos = pygame.mouse.get_pos()
                #    Car(self, pos[0] , pos[1] )
                elif  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit = True

      
    def update(self):
        self.all_sprites.update()
        #for sprite in self.trfl:
        #    a = pygame.sprite.spritecollide(sprite, self.all_sprites,False)
        #    print(a)
        #for sprite in self.all_sprites:
        ##    pygame.sprite.groupcollide(self.all_sprites,self.all_sprites,
        ##    True, False)
        #    for a in pygame.sprite.spritecollide(sprite, self.all_sprites,False,pygame.sprite.collide_circle):  
        #        if a != sprite:
        #            c = a.left_right(a.pos, sprite.pos)
        #            if c > 0:
        #               a.vel = vec(0,0)
        #               a.acc = vec(0,0)
        #            #elif c < 0:
        #            #   a.vel = vec(0,0)
                    
            #hits = pygame.sprite.groupcollide(sprite, zy_enemies, True, False, pygame.sprite.collide_circle)




if __name__ == '__main__':
    game = Game()
    game.new()
    game.run()
