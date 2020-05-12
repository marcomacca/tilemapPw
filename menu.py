import pygame_menu, pygame



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
        self.menu.set_relative_position(10, 10)
        self.menu.disable()
        game.menu = self.menu


    def reset(self):
        self.menu._close()
        self.game.all_sprites = pygame.sprite.Group()
        self.game.timers = []

    def debug(self):    
        self.menu._close()
        if self.game.debug:
            self.game.debug = False
        else:
            self.game.debug = True
