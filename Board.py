import pygame
from config import config

class Board:
    def __init__(self, screen, boardSize, screenHeight, screenWidth):
        self.boardSize = boardSize
        self.loss = False
        self.screen = screen
        self.tiles = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        self.image = pygame.image.load('gameboard.png')
        self.tileimage = pygame.image.load('tile.png')
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.pos = {
            'x': screenWidth / 2 - (config['widthMagicNumber'] / 2),
            'y': screenHeight / 2 - (config['widthMagicNumber'] / 2)
        }


    def render_board(self):
        self.render_loss_font()
        self.render_tiles()
        self.render_board_background()
        pygame.display.update()

    def render_board_background(self):
        # Board background
        self.screen.blit(self.image, (self.pos['x'], self.pos['y']))

    def render_tiles(self):
        # Render all the tiles
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                tileValue = self.tiles[i][j]
                if (tileValue != 0):
                    tileFontSize = self.get_font_size(tileValue)
                    tfont = pygame.font.SysFont("ClearSans-Regular.ttf", tileFontSize)
                    tx = i * 48 + 5 * (i + 1) + self.pos['x']
                    ty = j * 48 + 5 * (j + 1) + self.pos['y']
                    self.screen.blit(self.tileimage, (tx, ty))
                    text = tfont.render(str(2 ** tileValue), 1, (0, 0, 0))
                    self.screen.blit(text, (tx + tileValue + 15 - (8 * (len(str(2 ** tileValue)) - 1)), ty + 14))

    def render_loss_font(self):
        if (self.loss):
            lossfont = pygame.font.SysFont("ClearSans-Regular.ttf", 68)
            text = lossfont.render("YOU LOST!", 1, (255, 255, 255))
            self.screen.blit(text, (22, 0))

    def get_font_size(self, tile):
        fontSize = 32
        if (tile > 6):
            fontSize = 30
        if (tile > 9):
            fontSize = 25
        return fontSize
