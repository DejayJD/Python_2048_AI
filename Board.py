import pygame
import config
import random


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
            'x': screenWidth / 2 - (config.widthMagicNumber / 2),
            'y': screenHeight / 2 - (config.widthMagicNumber / 2)
        }

    def player_move(self, xDir, yDir):
        # move tiles around
        self.move_tiles(xDir, yDir)

        # add a new tile
        self.set_random_tile(1)

        # check if the player has lost yet
        self.check_win_loss()

    def render_board(self):
        self.render_board_background()
        self.render_tiles()
        self.render_loss_font()
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
            fontSize = 24
        return fontSize

    # this moves tiles across a row/column
    # -- PARAMS:
    # @newTileDestination = the position on the board where the new tile will move
    # @direction = "x" or "y"
    # @tdir = ""
    # @far =
    # @colrow =
    # @currentTileLoc = position of the current tile before moving it
    # @move =
    def move_tile(self, tiles, direction, tdir, far, colrow, currentTileLoc, updateBoard):
        newTileDestination = currentTileLoc + tdir
        if (0 <= newTileDestination < 4):
            if (direction == "x"):
                tile = tiles[currentTileLoc][colrow]
                newTile = tiles[newTileDestination][colrow]
            elif (direction == "y"):
                tile = tiles[colrow][currentTileLoc]
                newTile = tiles[colrow][newTileDestination]
            if (newTile == 0):
                if (updateBoard == True):
                    if (direction == "x"):
                        tiles[currentTileLoc][colrow], tiles[newTileDestination][colrow] = \
                            tiles[newTileDestination][colrow], tiles[currentTileLoc][colrow]
                    if (direction == "y"):
                        tiles[colrow][currentTileLoc], tiles[colrow][newTileDestination] = tiles[colrow][
                                                                                               newTileDestination], \
                                                                                           tiles[colrow][
                                                                                               currentTileLoc]
                self.move_tile(tiles, direction, tdir, far, colrow, newTileDestination, updateBoard)
                return 1
            elif (newTile == tile):
                if (updateBoard):
                    if (direction == "x"):
                        tiles[newTileDestination][colrow] += 1
                        tiles[currentTileLoc][colrow] = 0
                    if (direction == "y"):
                        tiles[colrow][newTileDestination] += 1
                        tiles[colrow][currentTileLoc] = 0
                return 1
        return 0

    # This function iterates over the tiles using the key inputs
    def move_tiles(self, xdir, ydir):
        # move tiles based on a keystroke
        # I tried to use a simple math equations to find my numbers for the loops in order to save code
        yFar = 0
        xFar = 0
        if (xdir != 0):
            xFar = 3 * (1 + xdir) / 2  # Is 0 when xdir = -1 and 3 when xdir = 1
            xDist = 4 - xFar - (1 + xdir)  # Is 4 when xdir = -1, is -1 when xdir = 1
            yDist = 4
            xr = xdir * -1
            yr = 1
        if (ydir != 0):
            yFar = 3 * (1 + ydir) / 2  # Is 0 when ydir = -1 and 3 when ydir = 1
            yDist = 4 - yFar - (1 + ydir)  # Is 4 when ydir = -1, is -1 when ydir = 1
            xDist = 4
            yr = ydir * -1
            xr = 1
        for i in range(xFar, xDist, xr):
            for j in range(yFar, yDist, yr):
                if (self.tiles[i][j] != 0):
                    if (xdir != 0):
                        self.move_tile(self.tiles, "x", xdir, xFar, j, i, True)
                    if (ydir != 0):
                        self.move_tile(self.tiles, "y", ydir, yFar, i, j, True)
        return

    # uses the existing move tile function to check for losing
    def check_win_loss(self):
        self.loss = True
        for i in range(0, 4):
            for j in range(0, 4):
                if (self.move_tile(self.tiles, "x", 1, 3, j, i, False) == 1 or
                        self.move_tile(self.tiles, "x", -1, 0, j, i, False) == 1 or
                        self.move_tile(self.tiles, "y", 1, 0, i, j, False) == 1 or
                        self.move_tile(self.tiles, "y", -1, 3, i, j, False) == 1):
                    self.loss = False
        return

    # this sets a random tile to a value, and sets none if there are none available
    def set_random_tile(self, val):
        full = True
        for i in range(0, 4):
            for j in range(0, 4):
                if (self.tiles[i][j] == 0):
                    full = False
                    break
        if (full):
            return
        xrand = random.randint(0, 3)
        yrand = random.randint(0, 3)
        while (self.tiles[xrand][yrand] != 0):
            xrand = random.randint(0, 3)
            yrand = random.randint(0, 3)
        self.tiles[xrand][yrand] = val
        return
