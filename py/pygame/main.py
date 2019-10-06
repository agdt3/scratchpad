import sys, pygame, queue
from hex import HexTiles, SelectType


pygame.init()
pygame.font.init()


class World:
    def __init__(self, size=None, debug=False):
        self.debug = debug
        self.width = 1024
        self.height = 768
        self.size = size if size is not None else (self.width, self.height)
        #flags = pygame.DOUBLEBUF | pygame.FULLSCREEN
        flags = pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(self.size, flags)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 32)
        self.click_events = queue.Queue(maxsize=3)

        self.tiles = HexTiles(
            #size=(100, 100),
            rows=8,
            columns=10,
            spacing=2,
            color=(0, 0, 255),
            select_color=(100, 100, 255),
            select_type=SelectType.FACE,
            area=(1024, 768)
        )

        #self.background = pygame.Surface((self.width, self.height))
        #self.background.fill((255,255,255))
        #self.screen.fill((255,255,255))
        self.screen.fill((0,0,0))

        self.loop()

    def check_events(self):
        self.events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.click_events.full():
                    self.click_events.put(pygame.mouse.get_pos())

    def check_colissions(self):
        while not self.click_events.empty():
            pos = self.click_events.get()
            self.tiles.check_colissions(pos)

    def update(self):
        self.tiles.update()

    def draw(self):
        to_erase = []

        if self.debug:
            pygame.display.set_caption("FPS: " + str(self.clock.get_fps()))
            '''
            text = self.font.render("FPS: " + str(self.clock.get_fps()), False, (255, 255, 255))
            text_rect = text.get_rect()
            to_erase.append((self.background, text_rect, text_rect))
            '''

        """"
        for sprite in self.balls.sprites():
            to_erase.append((self.background, sprite.old_rect, sprite.old_rect))

        self.screen.blits(to_erase)
        """
        self.tiles.draw(self.screen)

        '''
        if self.debug:
            self.screen.blit(text, text_rect)
        '''

        pygame.display.update(self.tiles.sprites())

    def loop(self):
        while 1:
            self.clock.tick(60)
            #self.clock.tick_busy_loop(60)
            self.check_events()
            self.check_colissions()
            self.update()
            self.draw()

world = World(debug=True)
