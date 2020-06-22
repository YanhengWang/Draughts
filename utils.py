import math

'''--- Constants ---'''
PATH_DATA_FOLDER = "/Swallow/projects/Draughts/data/"
PATH_LABEL = PATH_DATA_FOLDER + "labels.dat"
PATH_PARAM = "param.pkl"
GRID_SIZE = 50

EMPTY = 0
WHITE = 1
BLACK = 2
KING = 4

BOARD = False
STONE = True

LEFT = 1
RIGHT = 2
UP = 4
DOWN = 8

'''--- Utilities ---'''
# Convert index on board to (row, col)-pair
def IndexToRC(idx):
	row = (idx-1) // 5
	if row%2 == 0:
		col = (idx-1) % 5 * 2 + 1
	else:
		col = (idx-1) % 5 * 2
	return (row, col)

# Convert index on board to (x, y)-pair
def IndexToXY(idx):
	row, col = IndexToRC(idx)
	return (col*GRID_SIZE, row*GRID_SIZE)

# Convert (x, y)-pair to index on board
def XYToIndex(x, y):
	x = x // GRID_SIZE
	y = y // GRID_SIZE
	return y * 5 + int(math.ceil((x+1)/2))

# Convert index to bounding box
def IndexToBox(idx, offset = 0):
	x, y = IndexToXY(idx)
	return (x + offset, y + offset, (x+GRID_SIZE) - offset, (y+GRID_SIZE) - offset)

# Convert the 1D state to a 3D representation shaped 5*10*10
def StateToImg(state):
	player = [([0]*10) for i in range(10)]
	opponent = [([0]*10) for i in range(10)]
	playerKing = [([0]*10) for i in range(10)]
	opponentKing = [([0]*10) for i in range(10)]
	
	for idx in range(1, 51):
		if state.player == WHITE:
			i, j = IndexToRC(idx)
		else:
			i, j = IndexToRC(51-idx)  # mirror
		if state.pos[idx] == state.player:
			player[i][j] = 1
		elif state.pos[idx] == state.opponent:
			opponent[i][j] = 1
		elif state.pos[idx] == (state.player|KING):
			playerKing[i][j] = 1
		elif state.pos[idx] == (state.opponent|KING):
			opponentKing[i][j] = 1
	return [player, opponent, playerKing, opponentKing]
	
# Judge if a state contains specific flag
def HasFlag(st, flag):
	return (st & flag) > 0

# Get the direction pinpointing from idx to idx2
def GetDirection(idx1, idx2):
	x1, y1 = IndexToXY(idx1)
	x2, y2 = IndexToXY(idx2)
	ret = (LEFT if x1 > x2 else RIGHT)
	ret |= (UP if y1 > y2 else DOWN)
	return ret

# Returns the adjacent index of the given one with respect to direction
def Adjacent(idx, direction):
	x, y = IndexToXY(idx)
	if HasFlag(direction, LEFT):
		x -= GRID_SIZE
	else:
		x += GRID_SIZE
	if HasFlag(direction, UP):
		y -= GRID_SIZE
	else:
		y += GRID_SIZE
	
	if x<0 or x>9*GRID_SIZE or y<0 or y>9*GRID_SIZE:
		return None
	return XYToIndex(x, y)

