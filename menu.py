import pygame_menu, pygame
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


class Menu:

    def __init__(self, game):

        self.game = game
        self.menu = pygame_menu.Menu(height=400,
                             width=400,
                             theme=pygame_menu.themes.THEME_DARK,
                             onclose=pygame_menu.events.CLOSE,
                            
                             title='Traffic Simulator')
        #self.menu.add_text_input('Name: ', default='John Doe')
        #self.menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)],)
        self.menu.add_button('Play' ,pygame_menu.events.CLOSE)
        
        self.menu.add_button('Reset', self.reset)
        self.menu.add_button('Graph', self.create_graph)
        self.menu.add_button('Quit', self.close)
        self.menu.set_relative_position(10, 10)
        self.menu.disable()
        game.menu = self.menu
        submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        submenu_theme.widget_font_size = 15
        play_submenu = pygame_menu.Menu(
             height=400,
             theme=submenu_theme,
             title='Submenu',
             width=400,
         )
        for i in range(30):
             play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
        play_submenu.add_button('Return to main menu', pygame_menu.events.RESET)
        self.menu.add_button('Debug' ,play_submenu)
        #https://github.com/ppizarror/pygame-menu/blob/master/pygame_menu/examples/game_selector.py
    def close(self):
        self.menu._close()
        self.game.exit = True

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
        #fig = go.Figure(data=go.Scatter(x=self.game.time, y=self.game.life))
        #fig.show()
        fig = go.Figure(data=[go.Histogram(x=self.game.life)])
        #fig = px.histogram(x=self.game.time, y=self.game.life, histfunc='avg')
        fig.show()

    def submenu(self):

         submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
         submenu_theme.widget_font_size = 15
         play_submenu = pygame_menu.Menu(
             height=400,
             theme=submenu_theme,
             title='Submenu',
             width=400,
         )
         for i in range(30):
             play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
         play_submenu.add_button('Return to main menu', pygame_menu.events.RESET)

         play_menu.add_button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                              pygame_menu.events.CLOSE,
                              pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
         #play_menu.add_selector('Select difficulty ',
         #                       [('1 - Easy', 'EASY'),
         #                        ('2 - Medium', 'MEDIUM'),
         #                        ('3 - Hard', 'HARD')],
         #                       onchange=change_difficulty,
         #                       selector_id='select_difficulty')
         #play_menu.add_button('Another menu', play_submenu)
         play_menu.add_button('Return to main menu', pygame_menu.events.BACK)
