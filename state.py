from utils import *
import math
import copy

class State:
	# Constructor
	def __init__(self, parent, move):
		if parent == None:
			self.pos = [0] + ([BLACK]*20) + ([EMPTY]*10) + ([WHITE]*20)  # position
			self.passed = [False] * 51  # used in FindRoute() only
			self.player = WHITE
			self.opponent = BLACK
		else:
			self.pos = copy.copy(parent.pos)
			self.passed = parent.passed  # use this array in public in order to save memory
			self.Move(move)
			self.player = parent.opponent
			self.opponent = parent.player
		self.child = []  # children list
		self.n = 1  # visit count
		self.v = 0  # value
		
		self.moves = []
		self.mandatory = False
		maxLength = 0
		for idx in range(1, 51):
			if self.GetColour(idx) != self.player:
				continue
			flag, tmp = self.GetMoves(idx)
			self.mandatory = self.mandatory or flag
			if self.mandatory:
				if not flag:
					continue
				if len(tmp[0]) == maxLength:
					self.moves += tmp
				elif len(tmp[0]) > maxLength:
					self.moves = tmp
					maxLength = len(tmp[0])
			else:
				self.moves += tmp
		
	# Simulate the specific move
	def Move(self, move):
		prev = move[0]
		st = self.pos[prev]
		for this in move[1: ]:
			d = GetDirection(prev, this)
			while prev!=this:
				self.pos[prev] = EMPTY
				prev = Adjacent(prev, d)
		if (this<=5 and HasFlag(st, WHITE)) or (this>=46 and HasFlag(st, BLACK)):
			st |= KING
		self.pos[this] = st
	
	# Search for moves originating from idx
	def FindRoute(self, idx, king):
		route = [[]]
		for d in (LEFT|UP, LEFT|DOWN, RIGHT|UP, RIGHT|DOWN):
			p = Adjacent(idx, d)
			while king and p and self.pos[p]==EMPTY:
				p = Adjacent(p, d)
			if p==None or self.GetColour(p)!=self.opponent or self.passed[p]:
				continue
			
			self.passed[p] = True
			q = Adjacent(p, d)
			while q and self.pos[q]==EMPTY:
				route += self.FindRoute(q, king)  # recurence
				if not king:
					break
				q = Adjacent(q, d)
			self.passed[p] = False
		
		maxLength = 0
		ret = []
		for p in route:  # find the longest route(s) and make a list
			if len(p) == maxLength:
				p.insert(0, idx)
				ret.append(p)
			elif len(p) > maxLength:
				maxLength = len(p)
				p.insert(0, idx)
				ret = [p]
		return ret
		
	# Get the colour of given index
	def GetColour(self, idx):
		if HasFlag(self.pos[idx], WHITE):
			return WHITE
		if HasFlag(self.pos[idx], BLACK):
			return BLACK
		return EMPTY
	
	# Get possible moves originating from idx. Returns a flag and a list
	def GetMoves(self, idx):
		st = self.pos[idx]  # backup
		self.pos[idx] = EMPTY
		ret = self.FindRoute(idx, HasFlag(st, KING))
		self.pos[idx] = st  # restore
		if len(ret[0]) > 1:
			return (True, ret)
		
		ret = []
		if HasFlag(st, KING):
			for d in (LEFT|UP, LEFT|DOWN, RIGHT|UP, RIGHT|DOWN):
				p = Adjacent(idx, d)
				while p and self.pos[p]==EMPTY:
					ret.append([idx, p])
					p = Adjacent(p, d)
		else:
			for d in (LEFT, RIGHT):
				p = Adjacent(idx, d | (UP if self.player==WHITE else DOWN))
				if p and self.pos[p]==EMPTY:
					ret.append([idx, p])
		return (False, ret)
	
	def Expand(self):
		if len(self.moves) > len(self.child):  # there exists unexpanded move(s)
			newObj = State(self, self.moves[len(self.child)])
			self.child.append(newObj)
			return True
		return False
	
	def BestChild(self):
		best = None
		maxScore = -100
		for c in self.child:
			score = -c.v/c.n + 0.3*math.sqrt(math.log(self.n) / c.n)
			if score > maxScore:
				maxScore = score
				best = c
		return best
