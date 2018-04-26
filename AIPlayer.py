from MinMaxTree import MinMaxTree

class AIPlayer:
	def __init__(self, mDeep):
		self.mDeep = mDeep

	def getMove(self, board):
		self.tree = MinMaxTree(board, self.mDeep)
		move = self.tree.get_max(self.mDeep * 2)
		return move