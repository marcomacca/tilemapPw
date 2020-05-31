import os ,statistics, pygame, pytmx ,random, pygame_menu
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from tilemap import *
from sprites import *
from menu import *




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
        car_path = os.path.join(self.img_folder, "carx.png")
        map_path = os.path.join(map_folder, "testmap.tmx")
        self.map = TiledMap(map_path)
        self.map_img = pygame.transform.scale(self.map.make_map(), (1920, 1088)).convert()
        self.map_rect = self.map_img.get_rect()
        self.car_image = pygame.image.load(car_path).convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (48, 24))
        self.lista = []
        self.centro = []
        self.time = []
        self.life = []
        self.debug , self.smart_traffic = False, False
    
    def convert(self,seconds):
         min, sec = divmod(seconds, 60)
         hour, min = divmod(min, 60)
         if hour == 24:
             hour = 0
         #return "%02d:%02d" % (hour, min)
         return (hour, min)

    def trafficSet(self,timesimulator):
         ora = int(self.convert(timesimulator)[0])
         if ora < 8 or ora > 21:
             return 4
         elif ora in range(8,11) or ora in range(14,18):
             return 8
         else:
             return 12     


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.trfl = pygame.sprite.Group()
        self.listacord = self.map.tmxdata.objectgroups
        for tile_object in self.map.tmxdata.objectgroups:
            if 'traffic' in tile_object.name:
                Traffic_Light(self, tile_object)  
            elif 'Centro' in tile_object.name:
                self.centro = tile_object
            else:
                self.lista.append(tile_object)
        for tile_object in self.centro:
            if tile_object.name == 'rect':
                self.centro_rect = pygame.Rect(tile_object.x / 2,tile_object.y / 2, tile_object.width / 2, tile_object.height / 2)
            else:
                self.centro_pos = vec(tile_object.x / 2,tile_object.y / 2)
        self.trfl_list = self.trfl.sprites()
        #evento per creazione auto
        self.spawntimer = pygame.USEREVENT + 6
        pygame.time.set_timer(self.spawntimer, 3000)
        self.signal_counter = 0
        self.s1 = 0
        Menu(self)
        
        #for x in self.lista :
        #    Car(self, random.choice(self.lista))
            #self.listaPath.append(tile_object)
        #filtered_numbers = [item for item in self.listaPath if 'A' in
        #item.name ]
        #for x in filtered_numbers:
        #    print(x)



    def run(self):

        while not self.exit:
            self.traffic = self.trafficSet(self.s1 * 30)
            self.dt = self.clock.tick(self.ticks) / 500.0  
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
        self.screen.blit(self.map_img, (0,0))
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.trfl.draw(self.screen)
        if self.debug:
            for sprite in self.all_sprites:
                sprite.draw_vectors()
                sprite.draw_rect()
        if self.menu.is_enabled():
            self.menu.draw(self.screen)
        pygame.display.flip()         


   
    def events(self):

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == self.spawntimer:
                    if self.menu._current._menubar._title == 'Overview': #se ho l'overview aperta richiamo la creazione del menu per aggiornare i campi
                        self.menu._widgets[3].apply()             
                    for a in range(self.traffic):
                        Car(self, random.choice(self.lista))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.menu.is_enabled():
                            self.menu.disable()
                            self.menu.reset(1)
                        else:
                            self.menu.enable()
                    elif self.menu.is_enabled():
                        self.menu.update(events)
                elif self.menu.is_enabled():  #per gestione con mouse
                        self.menu.update(events)
            self.trfl.update(events)
            if self.signal_counter == 4:
                self.signal_counter = 0
                self.trfl_list[0].reset()
                self.trfl_list[2].reset()
            elif self.signal_counter == 2:
                self.trfl_list[3].reset()
                self.trfl_list[1].reset()
                #for index, trfl in enumerate(self.trfl_list):
                ##carInLane = trfl.traffic_detector()
                #    trfl.check()
               
                #elif event.type == pygame.MOUSEBUTTONUP:
                #    if self.debug:
                #        self.debug = False
                #    else:
                #        self.debug = True
                #         Car(self, random.choice(self.lista))
                #         if self.i >= 2:
                #         self.i = 0
                #     else :
                #        self.i += 1
                #     for a in self.trfl:
                #         a.change_sign(self.i)
                ##    pos = pygame.mouse.get_pos()
                ##    Car(self, pos[0] , pos[1] )
                #elif  event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_ESCAPE:
                #        self.exit = True
 
      
    def update(self):
        self.all_sprites.update()
        #self.trfl.update()
        #carInLane = []
        if self.signal_counter < 2 :
            self.trfl_list[0].active = True
            self.trfl_list[2].active = True
        else :
            self.trfl_list[3].active = True
            self.trfl_list[1].active = True


        #if len(self.life) != 0:
        ##    print(round(statistics.mean(self.life),2))



        # Kill sprite spowned in the same position  
        for sprite in self.all_sprites:
            a = pygame.sprite.spritecollide(sprite,self.all_sprites,False)
            for x in a:
                if x != sprite and sprite.index == 0:
                    sprite.kill()






if __name__ == '__main__':
    game = Game()
    game.new()
    game.run()
