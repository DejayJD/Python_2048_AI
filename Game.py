import pygame
import random
from AIPlayer import AIPlayer


# The game class controls all of the game data
# Currently it's not very different from the Main class,
# But in the future when I want to add starting a new game, it will be much easier
class Game(pygame.sprite.Sprite):
    def __init__(self, screenHeight, screenWidth, screen, mDeep):

        self.screen = screen
        self.AIPlayer = AIPlayer(4)

        pygame.sprite.Sprite.__init__(self)
        self.set_random_tile(1)
        self.loss = False

    # this moves tiles across a row/column
    # -- PARAMS:
    # @newTileDestination = the position on the board where the new tile will move
    # @direction = "x" or "y"
    # @tdir = ""
    # @far =
    # @colrow =
    # @currentTileLoc = position of the current tile before moving it
    # @move =
    def move_tile(self, tiles, direction, tdir, far, colrow, currentTileLoc, move):
        newTileDestination = currentTileLoc + tdir
        if (0 <= newTileDestination < 4):
            if (direction == "x"):
                tile = tiles[currentTileLoc][colrow]
                newTile = tiles[newTileDestination][colrow]
            elif (direction == "y"):
                tile = tiles[colrow][currentTileLoc]
                newTile = tiles[colrow][newTileDestination]
            if (newTile == 0):
                if (move == True):
                    if (direction == "x"):
                        tiles[currentTileLoc][colrow], tiles[newTileDestination][colrow] = tiles[newTileDestination][colrow], tiles[currentTileLoc][colrow]
                    if (direction == "y"):
                        tiles[colrow][currentTileLoc], tiles[colrow][newTileDestination] = tiles[colrow][newTileDestination], tiles[colrow][currentTileLoc]
                self.move_tile(tiles, direction, tdir, far, colrow, newTileDestination, move)
                return 1
            elif (newTile == tile):
                if (move):
                    if (direction == "x"):
                        tiles[newTileDestination][colrow] += 1
                        tiles[currentTileLoc][colrow] = 0
                    if (direction == "y"):
                        tiles[colrow][newTileDestination] += 1
                        tiles[colrow][currentTileLoc] = 0
                return 1
        return 0

    # This function iterates over the tiles using the key inputs
    def move_tiles(self, tiles, xdir, ydir):
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
                if (tiles[i][j] != 0):
                    if (xdir != 0):
                        self.move_tile(tiles, "x", xdir, xFar, j, i, True)
                    if (ydir != 0):
                        self.move_tile(tiles, "y", ydir, yFar, i, j, True)
        return

    def render_game(self):
        aiMove = self.AIPlayer.getMove(self.tiles)
        if (aiMove is not None):
            self.key_move(aiMove)
        # This is the endless rendering loop (called in mainloop)
        self.render_board()

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
            self.move_tiles(self.tiles, xdir, ydir)
        # add a new tile
        self.set_random_tile(1)
        # check if the player has lost yet
        self.check_win_loss()



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
