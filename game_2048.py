import os, sys, pygame, random, copy
from MinMaxTree import MinMaxTree
from Game import Game
from pygame.locals import *
from config import config

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


class Main:
    def __init__(self, width, height):
        # Initialize PyGame
        pygame.init()
        random.seed
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Set a plain background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        # Create a game object
        self.game = Game(config.screenHeight, config.screenWidth, self.screen, 1)

    # This is the constant running game loop.
    def main_loop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.game.key_move("right")
                    if event.key == pygame.K_LEFT:
                        self.game.key_move("left")
                    if event.key == pygame.K_DOWN:
                        self.game.key_move("down")
                    if event.key == pygame.K_UP:
                        self.game.key_move("up")

            self.game.render_game()



if __name__ == "__main__":
    MainWindow = Main(config.screenWidth, config.screenHeight)
    MainWindow.main_loop()
