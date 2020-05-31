import pygame_menu,pygame,statistics
import plotly.graph_objects as go
#import plotly.express as px


class Menu:

    def __init__(self, game):

        self.game = game
        self.menu = pygame_menu.Menu(height=450,
                             width=400,
                             theme=pygame_menu.themes.THEME_DARK,
                             onclose=pygame_menu.events.CLOSE,enabled=False,
                             title='Traffic Simulator')
        #self.menu.add_text_input('Name: ', default='John Doe')
        #self.menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)],)
        self.menu.add_button('Play' ,pygame_menu.events.CLOSE)
        self.menu.add_button('Reset', self.reset)
        self.menu.add_button('Graph', self.create_graph)
        self.menu.add_button('Overview', self.create_submenu)
        self.menu.add_selector('Smart Traffic: ',
                           [('ON',True),
                            ('OFF',False)],
                           onchange=self.smart_traffic_controller,default=1)
        self.menu.add_selector('Debug: ',
                           [('ON',True),
                            ('OFF',False)],default=1,
                           onchange=self.debug)
        self.menu.add_button('Quit', self.close)
        #self.menu.add_image(self.game.car_path)
        self.menu.set_relative_position(10, 5)
        game.menu = self.menu

    def create_submenu(self):
        self.submenu = pygame_menu.Menu(height=400,
             theme=pygame_menu.themes.THEME_DARK,
             title='Overview',
             width=400,)
        TEXT = ['Numero Auto: {0}'.format(len(self.game.all_sprites.sprites())),
         'Totale auto transitate: {0}'.format(len(self.game.life)),
         'Tempo trascorso: {0}'.format(round(pygame.time.get_ticks()/1000),2),
         'Media percorrenza: {0}'.format(round(statistics.mean(self.game.life),2) if len(self.game.life) != 0 else 0),'', ]
        for m in TEXT:
            self.submenu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=30)
        self.submenu.add_button('Return to main menu', pygame_menu.events.RESET)
        self.submenu.set_relative_position(20, 10)
        self.menu._open(self.submenu)
            
     
    def close(self):
        self.menu._close()
        self.game.exit = True

    def reset(self):
        self.menu._close()
        #self.game.all_sprites = pygame.sprite.Group()
        #self.game.time = []
        #self.game.life = []
        self.game.new() #Per poter resettare totalmente anche i semafori

    def debug(self,value,status):    
        self.game.debug = status

    def smart_traffic_controller(self,value,status):    
        name, index = value
        #self.menu._close()
        self.game.smart_traffic = status


    def create_graph(self):
        self.menu._close()
        #fig = go.Figure(data=go.Scatter(x=self.game.time, y=self.game.life))
        #fig.show()
        fig = go.Figure(data=[go.Histogram(x=self.game.life)])
        fig.write_html('tmp.html', auto_open=True) #alternative if stuck on loading page
        #fig = px.histogram(x=self.game.time, y=self.game.life, histfunc='avg')
        #fig.show()

    #def submenu(self):

    #     submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    #     submenu_theme.widget_font_size = 15
    #     play_submenu = pygame_menu.Menu(height=400,
    #         theme=submenu_theme,
    #         title='Submenu',
    #         width=400,)
    #     for i in range(30):
    #         play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
    #     play_submenu.add_button('Return to main menu', pygame_menu.events.RESET)

    #     play_menu.add_button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
    #                          pygame_menu.events.CLOSE,
    #                          pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    #     #play_menu.add_selector('Select difficulty ',
    #     #                       [('1 - Easy', 'EASY'),
    #     #                        ('2 - Medium', 'MEDIUM'),
    #     #                        ('3 - Hard', 'HARD')],
    #     #                       onchange=change_difficulty,
    #     #                       selector_id='select_difficulty')
    #     #play_menu.add_button('Another menu', play_submenu)
    #     play_menu.add_button('Return to main menu', pygame_menu.events.BACK)
