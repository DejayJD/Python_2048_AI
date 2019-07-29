import pygame
import random
import config
from Board import Board
from AIPlayer import AIPlayer


# The game class controls all of the game data
# Currently it's not very different from the Main class,
# But in the future when I want to add starting a new game, it will be much easier
class Game(pygame.sprite.Sprite):


    def __init__(self, screenHeight, screenWidth, screen):
        self.screen = screen
        self.AIPlayer = None

        pygame.sprite.Sprite.__init__(self)

        self.loss = False
        self.board = Board(self.screen, config.tileGridSize, config.screenHeight, config.screenWidth)
        self.board.set_random_tile(1)

    def addAIPlayer(self, mDeep):
        self.AIPlayer = AIPlayer(mDeep)  # m layers tree depth

    def render_game(self):
        if self.AIPlayer is not None:
            aiMove = self.AIPlayer.getMove(self.board)
            if (aiMove is not None):
                self.key_move(aiMove)
        # This is the endless rendering loop (called in mainloop)
        self.board.render_board()

    def key_move(self, key):
        # check for Key Presses
        ydir = 0
        xdir = 0
        if key == "left":
            xdir = -1
        if key == "right":
            xdir = 1
        if key == "up":
            ydir = -1
        if key == "down":
            ydir = 1
        # move tiles accordingly
        self.board.player_move(xdir, ydir)


