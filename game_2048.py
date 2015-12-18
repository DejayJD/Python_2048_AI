import os, sys
import pygame
import random
import copy
from pygame.locals import *
global screenWidth
screenWidth = 300
global screenHeight
global win
win = False
global loss
loss = False
screenHeight = 300

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Main:
	def __init__(self, width, height):
		#Initialize PyGame
		pygame.init()
		random.seed
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()

		#Set a plain background
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))

		#Create a game object
		self.game = Game(self.screen, 1)
		
	#This is the constant running game loop.	
	def mainLoop(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						self.game.keyMove("right")
					if event.key == pygame.K_LEFT:
						self.game.keyMove("left")
					if event.key == pygame.K_DOWN:
						self.game.keyMove("down")
					if event.key == pygame.K_UP:
						self.game.keyMove("up")
			
			self.game.renderGame()

class MinMaxTree:
	def __init__(self, state, move=None):
		self.state = state
		self.hValue = None
		self.children = []
		self.move = move

	def insert(self, newState, move=None):
		self.children.append(MinMaxTree(newState, move))

	def calcHeuristic(self):
		emptySpots = getEmpty(self.state)
		highestTile = getHighestTile(self.state)
		
		self.hValue =  highestTile['value'] + emptySpots['sum']
		return self.hValue

	def abTreeSearch(self, depth, alpha=-float("inf"), beta=float("inf"), player = -1):
		if (depth == 0):
			return self.calcHeuristic()
		if (player > 0):
			value = -float("inf")
			empty = getEmpty(self.state)
			for i in range(empty['sum']): #Max - insert min trees
				tempState = copy.deepcopy(self.state)
				emptyX = empty['tiles'][i][0]
				emptyY = empty['tiles'][i][1]
				tempState[emptyX][emptyY] = 1
				self.insert(tempState)
				value = max(value, self.children[i].abTreeSearch(depth-1, alpha, beta, player*-1))
				alpha = max(alpha, value)
				self.hValue = value
				if (beta <= alpha):
					break
			return value 
		elif (player < 0): #Min - insert max trees
			value = float("inf")
			directions = ["up", "right", "left", "down"]
			xdirs = [0, 1, -1, 0]
			ydirs = [-1, 0, 0, 1]
			for i in range(4):
				tempState = copy.deepcopy(self.state)
				moveTiles(self.state, xdirs[i],ydirs[i])
				self.insert(tempState, directions[i])
				child = self.children[i]
				value = min(value, child.abTreeSearch(depth-1, alpha, beta, player*-1))
				beta = min(beta, value)
				self.hValue = value
				if (beta <= alpha):
					break
			return value

	def getMax(self, level=1):
		self.abTreeSearch(level)
		rootValue = -float("inf")
		bestMove = None
		for child in self.children:
			if (child.hValue > rootValue):
				bestMove = child.move
				rootValue = child.hValue
		self.hValue = rootValue
		return bestMove

	def __repr__(self, level=0):
		ret = "\t"*level + str(self.move) + " " + str(self.hValue) + "\n"
		for child in self.children:
			ret += child.__repr__(level+1)
		return ret


class AIPlayer:
	def __init__(self, mDeep):
		self.mDeep = mDeep

	def getMove(self, board):
		self.tree = MinMaxTree(board, self.mDeep)
		move = self.tree.getMax(self.mDeep*2)
		return move


#this moves tiles across a row/column
def moveTile(tiles, direction, tdir, far, colrow, tileCurr, move):
	global win
	newT = tileCurr+tdir
	if (newT >= 0 and newT < 4):
		if (direction == "x"):
			tile = tiles[tileCurr][colrow]
			newTile = tiles[newT][colrow]
		elif (direction == "y"):
			tile = tiles[colrow][tileCurr]
			newTile = tiles[colrow][newT]
		if (newTile == 0):
			if (move == True):
				if (direction=="x"):
					tiles[tileCurr][colrow], tiles[newT][colrow] = tiles[newT][colrow], tiles[tileCurr][colrow]
				if (direction=="y"):
					tiles[colrow][tileCurr], tiles[colrow][newT] = tiles[colrow][newT], tiles[colrow][tileCurr]
			moveTile(tiles, direction, tdir, far, colrow, newT, move)
			return 1
		elif (newTile == tile):
			if (move == True):
				if (direction=="x"):
					tiles[newT][colrow] += 1
					tiles[tileCurr][colrow] = 0
				if (direction=="y"):
					tiles[colrow][newT] += 1
					tiles[colrow][tileCurr] = 0

			return 1
	return 0		


#This function iterates over the tiles using the key inputs
def moveTiles(tiles, xdir, ydir):
	#move tiles based on a keystroke
	#I tried to use a simple math equations to find my numbers for the loops in order to save code
	yFar = 0
	xFar = 0
	if (xdir != 0):
		xFar = 3*(1+xdir)/2 #Is 0 when xdir = -1 and 3 when xdir = 1
		xDist = 4-xFar-(1+xdir) #Is 4 when xdir = -1, is -1 when xdir = 1
		yDist = 4
		xr = xdir*-1
		yr = 1
	if (ydir != 0):
	 	yFar = 3*(1+ydir)/2 #Is 0 when ydir = -1 and 3 when ydir = 1
	 	yDist = 4-yFar-(1+ydir) #Is 4 when ydir = -1, is -1 when ydir = 1
	 	xDist = 4
	 	yr = ydir*-1
	 	xr = 1
	for i in range (xFar, xDist, xr):
	 	for j in range (yFar, yDist, yr):
	   		if (tiles[i][j] != 0):
	   			if (xdir != 0):
	   				moveTile(tiles, "x", xdir, xFar, j, i, True)
	   			if (ydir != 0):
	   				moveTile(tiles, "y", ydir, yFar, i, j, True)
	return

def getEmpty(tiles):
	empty = {}
	empty['sum'] = 0
	empty['tiles'] = []
	for i in range(0,4):
		for j in range(0,4):
			if (tiles[i][j] == 0):
				empty['sum'] += 1
				empty['tiles'].append([i, j])
	return empty

def getHighestTile(tiles):
	highest = {}
	highest['value'] =0
	for i in range(0,4):
		for j in range(0,4):
			if (tiles[i][j] > highest['value']):
				highest['value'] = tiles[i][j]
				highest['pos'] = [i,j]
	return highest


#The game class controls all of the game data
#Currently it's not very different from the Main class,
#But in the future when I want to add starting a new game, it will be much easier
class Game(pygame.sprite.Sprite):
	def __init__(self, screen, mDeep):
		global screenWidth
		global screenHeight
		self.screen = screen
		self.AIPlayer = AIPlayer(4)
		self.pos = {}
		self.pos['x'] = screenWidth/2-(217/2)
		self.pos['y'] = screenHeight/2-(217/2)
		pygame.sprite.Sprite.__init__(self) 
		self.image = pygame.image.load('gameboard.png')
		self.tiles = [[0 for j in range(4)] for i in range(4)]
		self.setRandomTile(1)
		self.tileimage = pygame.image.load('tile.png')
		
	def renderGame(self):
		aiMove = self.AIPlayer.getMove(self.tiles)
		if (aiMove != None):
			self.keyMove(aiMove)
		# This is the main rendering loop (called in mainloop)
		self.renderBoard()

	def keyMove(self, key):
		#check for Key Presses
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
		#move tiles accordingly
		moveTiles(self.tiles, xdir, ydir)
		#add a new tile
		self.setRandomTile(1)
		#check if the player has lost yet
		self.checkWinLoss()

	def renderBoard(self):
		global win
		winfont = pygame.font.SysFont("ClearSans-Regular.ttf", 68)
		#Display Winning/Losing text
		if (win == True):
			text = winfont.render("YOU WON!", 1, (255,255,255))
			self.screen.blit(text, (22, 0))
		if (loss == True):
			text = winfont.render("YOU LOST!", 1, (255,255,255))
			self.screen.blit(text, (22, 0))

		#Board background
		self.screen.blit(self.image, (self.pos['x'], self.pos['y']))

		#Render all the tiles
		for i in range(4):
			for j in range(4):
				tile = self.tiles[i][j]
				if (tile != 0):
					fontSize = 32
					if (tile > 6):
						fontSize = 30
					if (tile > 9):
						fontSize = 25
					tfont = pygame.font.SysFont("ClearSans-Regular.ttf", fontSize)
					
					tx = i*48 + 5*(i+1) + self.pos['x']
					ty = j*48 + 5*(j+1) + self.pos['y']
					self.screen.blit(self.tileimage, (tx, ty))
					text = tfont.render(str(2**tile), 1, (0,0,0))
					self.screen.blit(text, (tx+tile+15-(8*(len(str(2**tile))-1)), ty+14))
		pygame.display.update()

	#uses the existing move tile function to check for losing
	def checkWinLoss(self):
		global loss
		global win
		loss = True
		for i in range(0, 4):
			for j in range(0, 4):
				if (self.tiles[i][j] > 10):
					win = True
				if (moveTile(self.tiles, "x", 1, 3, j, i, False) == 1 or 
					moveTile(self.tiles, "x", -1, 0, j, i, False) == 1 or
					moveTile(self.tiles, "y", 1, 0, i, j, False) == 1 or 
					moveTile(self.tiles, "y", -1, 3, i, j, False) == 1):
					loss = False
		return
	
	#this sets a random tile to a value, and sets none if there are none available
	def setRandomTile(self, val):
		full = True
		for i in range(0, 4):
			for j in range(0, 4):
				if (self.tiles[i][j] == 0):
					full = False
					break
		if (full == True):
			return
		xrand = random.randint(0,3)
		yrand = random.randint(0,3)
		while (self.tiles[xrand][yrand] != 0):
			xrand = random.randint(0, 3)
			yrand = random.randint(0, 3)
		self.tiles[xrand][yrand] = val
		return


if __name__ == "__main__":
	MainWindow = Main(screenWidth, screenHeight)
	MainWindow.mainLoop()             