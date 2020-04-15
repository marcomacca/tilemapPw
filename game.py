import os
import pygame , pytmx
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from tilemap import *
from sprites import *




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Trafic Simulator")
        self.screen = pygame.display.set_mode((0, 0) ,pygame.FULLSCREEN) #,pygame.FULLSCREEN
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.load_data()

    def load_data(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_folder = os.path.join(current_dir, 'img')
        map_folder = os.path.join(current_dir, 'map')
        image_path = os.path.join(img_folder, "car.png")
        map_path = os.path.join(map_folder, "dc.tmx")
        self.map = TiledMap(map_path)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.car_image = pygame.image.load(image_path).convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (64, 32))
        self.lista = []

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.listacord = self.map.tmxdata.objectgroups
        for tile_object in self.map.tmxdata.objectgroups:
            self.lista.append(tile_object)
        for x in self.lista:
            Car(self, x)  
            #self.listaPath.append(tile_object)
        #filtered_numbers = [item for item in self.listaPath if 'A' in item.name ] 
        #for x in filtered_numbers:
        #    print(x)
            #if tile_object.name == 'car':
            #    Car(self, tile_object.x/2 , tile_object.y/2 )
            ##elif tile_object.name == 'car2':
            ##    self.car = Car(self, tile_object.x/2 , tile_object.y/2 )
            ##elif tile_object.name != None:
            ##    if "point" in tile_object.name:
            ##        self.lista.append(Vector2(tile_object.x, tile_object.y))            
            #elif tile_object.name == None:
            #        self.lista.append(Vector2(tile_object.x/2, tile_object.y/2))



    def run(self):
        # game loop - set self.playing = False to end the game
        while not self.exit:
            self.dt = self.clock.tick(self.ticks)/ 500.0  # fix for Python 2.x
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
        #self.screen.fill((0, 0, 0))
        a = pygame.transform.scale(self.map_img, (1920, 1088))
        self.screen.blit(a, (0,0))
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            #per problema tra float e int
            #pos = (sprite.pos - (sprite.rect.width / 2, sprite.rect.height / 2))
            #self.screen.blit(sprite.image, (int(pos.x),int(pos.y)))
            sprite.draw_vectors()
        #    if self.draw_debug:
        #        pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        #if self.draw_debug:
        #    for wall in self.walls:
        #        pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        pygame.display.update()
        pygame.display.flip()         

    def events(self):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                #elif event.type == pygame.MOUSEBUTTONUP:
                #    pos = pygame.mouse.get_pos()
                #    Car(self, pos[0] , pos[1] )
                elif  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit = True

      
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
            ## Logic
            #self.car.update(self.dt)
            #self.clock.tick(self.ticks)



if __name__ == '__main__':
    game = Game()
    game.new()
    game.run()
