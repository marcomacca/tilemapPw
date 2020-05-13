import pygame_menu, pygame
import matplotlib.pyplot as plt
from graph import *


class Menu:

    def __init__(self, game):

        self.game = game
        self.menu = pygame_menu.Menu(height=300,
                             width=400,
                             theme=pygame_menu.themes.THEME_DARK,
                             onclose=pygame_menu.events.CLOSE,
                            
                             title='Traffic Simulator')
     
        #self.menu.add_text_input('Name: ', default='John Doe')
        #self.menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)],)
        self.menu.add_button('Play' ,pygame_menu.events.CLOSE)
        self.menu.add_button('Debug' ,self.debug)
        self.menu.add_button('Reset', self.reset)
        self.menu.add_button('Graph', self.create_graph)
        self.menu.set_relative_position(10, 10)
        self.menu.disable()
        game.menu = self.menu


    def reset(self):
        self.menu._close()
        self.game.all_sprites = pygame.sprite.Group()
        self.game.time = []
        self.life = []

    def debug(self):    
        self.menu._close()
        if self.game.debug:
            self.game.debug = False
        else:
            self.game.debug = True


    def create_graph(self):
        self.menu._close()
        #fig, ax = plt.subplots()  # Create a figure containing a single axes.
        #ax.plot(self.game.time, self.game.life)  # Plot some data on the axes.
        #ax.set_xlabel('x Time ')  # Add an x-label to the axes.
        #ax.set_ylabel('y Car life time')  # Add a y-label to the axes.
        #ax.set_title("Simple Plot")  # Add a title to the axes.
        #ax.grid()
        #plt.show(block=False)
        #plt.ion()
        #plt.draw()
        #print("---Plot graph finish---")
        #plt.show()
    
    def mult_p(self):
        mp.set_start_method('spawn') 
        self.plot_process = mp.Process(
            target=Graph(), args=(), daemon=True)
        self.plot_process.start()
        
