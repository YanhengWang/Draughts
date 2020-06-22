from utils import *
from graphics import Graphics
from state import State
from torch.autograd import Variable
import network
import torch

current = State(None, None)
net = network.ResNet()
focusMoves = []
focus = 0

def MCTS(root):
	global net
	
	if root.Expand():
		data = torch.FloatTensor(StateToImg(root.child[-1])).unsqueeze(0)
		delta = net(Variable(data)).data[0, 0]
		root.child[-1].v = delta
		delta *= -1
	else:
		best = root.BestChild()
		if best == None:
			delta = -1
		else:
			delta = -MCTS(best)
	root.v += delta
	root.n += 1
	return delta
	
def Callback(idx, place):
	global GUI
	global current
	global focusMoves
	global focus

	if place == STONE:
		focus = idx
		if current.GetColour(idx)==current.player and not(current.mandatory):
			for move in focusMoves:
				GUI.SetBoard(False, *move)
			_, focusMoves = current.GetMoves(focus)
			for move in focusMoves:
				GUI.SetBoard(True, *move)
	else:
		for i, move in enumerate(current.moves):
			if focus==move[0] and idx==move[-1]:  # a legal move
				for j, move2 in enumerate(current.moves):
					if j != i:
						GUI.SetBoard(False, *move2)  # clear other highlights
				GUI.Move(move, current.pos[move[0]])
				current = current.child[i]
				
				for j in range(1000):
					MCTS(current)
				data = torch.FloatTensor(StateToImg(current)).unsqueeze(0)
				print(net(Variable(data)).data[0,0])
				best = current.child[0]
				for c in current.child:
					if c.n > best.n:
						best = c
				move2 = current.moves[current.child.index(best)]
				GUI.Move(move2, current.pos[move2[0]])
				current = best
				
				data = torch.FloatTensor(StateToImg(current)).unsqueeze(0)
				print(net(Variable(data)).data[0,0])
				
				if current.mandatory:
					for move2 in current.moves:
						GUI.SetBoard(True, *move2)
				break

f = torch.load(PATH_PARAM)
net.load_state_dict(f)
net.eval()

for i in range(50):
	MCTS(current)
GUI = Graphics(Callback)
GUI.Run()
