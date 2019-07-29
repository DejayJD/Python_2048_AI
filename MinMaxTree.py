import copy

class MinMaxTree:
    def __init__(self, board, move=None):
        self.board = board
        self.hValue = None
        self.children = []
        self.move = move

    def get_empty(self, tiles):
        empty = {
            'sum': 0,
            'tiles': []
        }
        for i in range(0, 4):
            for j in range(0, 4):
                if (tiles[i][j] == 0):
                    empty['sum'] += 1
                    empty['tiles'].append([i, j])
        return empty

    def get_highest_tile(self, tiles):
        highest = {
            'value': 0
        }
        for i in range(0, 4):
            for j in range(0, 4):
                if (tiles[i][j] > highest['value']):
                    highest['value'] = tiles[i][j]
                    highest['pos'] = [i, j]
        return highest

    def insertTreeLevel(self, newState, move=None):
        self.children.append(MinMaxTree(newState, move))

    def calc_heuristic(self):
        emptySpots = self.get_empty(self.board.tiles)
        highestTile = self.get_highest_tile(self.board.tiles)

        self.hValue = highestTile['value'] + emptySpots['sum']
        return self.hValue

    def ab_tree_search(self, depth, alpha=-float("inf"), beta=float("inf"), player=-1):
        if (depth == 0):
            return self.calc_heuristic()
        if (player > 0):
            value = -float("inf")
            empty = self.get_empty(self.board.tiles)
            for i in range(empty['sum']):  # Max - insert min trees
                boardCopy = copy.deepcopy(self.board)
                emptyX = empty['tiles'][i][0]
                emptyY = empty['tiles'][i][1]
                boardCopy.tiles[emptyX][emptyY] = 1
                self.insertTreeLevel(boardCopy)
                value = max(value, self.children[i].ab_tree_search(depth - 1, alpha, beta, player * -1))
                alpha = max(alpha, value)
                self.hValue = value
                if (beta <= alpha):
                    break
            return value
        elif (player < 0):  # Min - insert max trees
            value = float("inf")
            directions = ["up", "right", "left", "down"]
            xdirs = [0, 1, -1, 0]
            ydirs = [-1, 0, 0, 1]
            for i in range(4):
                boardCopy = copy.deepcopy(self.board)
                boardCopy.move_tiles(xdirs[i], ydirs[i])
                self.insertTreeLevel(boardCopy, directions[i])
                child = self.children[i]
                value = min(value, child.ab_tree_search(depth - 1, alpha, beta, player * -1))
                beta = min(beta, value)
                self.hValue = value
                if (beta <= alpha):
                    break
            return value

    def get_max(self, level=1):
        self.ab_tree_search(level)
        rootValue = -float("inf")
        bestMove = None
        for child in self.children:
            if (child.hValue > rootValue):
                bestMove = child.move
                rootValue = child.hValue
        self.hValue = rootValue
        return bestMove

    def __repr__(self, level=0):
        ret = "\t" * level + str(self.move) + " " + str(self.hValue) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
