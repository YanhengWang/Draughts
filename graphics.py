from utils import *
import tkinter
import time

COLOUR_BACKGROUND = "#DAB887"
COLOUR_BLACK = "#251507"
COLOUR_WHITE = "#F7F0DF"
COLOUR_NORMAL = "#A96020"
COLOUR_MARKED = "#AF2020"

class Graphics:
	# Constructor of the class
	def __init__(self, Callback):
		self.board = [0] * 51  # stores the board pieces
		self.stone = [0] * 51  # stores the stone objects
		self.Callback = Callback
		self.window = tkinter.Tk(className = "Draughts")
		self.window.resizable(width = False, height = False)
		self.canvas = tkinter.Canvas(self.window, width = 500, height = 500, background = COLOUR_BACKGROUND)
		self.canvas.bind("<Button-1>", self.EventHandler)
		self.canvas.pack()
		
		# Create stones & board pieces
		for i in range(1, 51):
			self.board[i] = self.canvas.create_rectangle(IndexToBox(i), fill = COLOUR_NORMAL, width = 0)
			self.stone[i] = self.canvas.create_oval(IndexToBox(i, 5))
		
		self.SetStone(BLACK, *list(range(1, 21)))
		self.SetStone(EMPTY, *list(range(21, 31)))
		self.SetStone(WHITE, *list(range(31, 51)))
	
	# Run the message loop
	def Run(self):
		self.window.mainloop()
	
	# Set the display options of stones
	def SetStone(self, st, *idxList):
		for idx in idxList:
			if st == EMPTY:
				self.canvas.itemconfig(self.stone[idx], state = tkinter.HIDDEN)
			else:
				self.canvas.itemconfig(self.stone[idx], state = tkinter.NORMAL)
			
			if HasFlag(st, BLACK):
				self.canvas.itemconfig(self.stone[idx], fill = COLOUR_BLACK, outline = COLOUR_WHITE)
			elif HasFlag(st, WHITE):
				self.canvas.itemconfig(self.stone[idx], fill = COLOUR_WHITE, outline = COLOUR_BLACK)
			
			if HasFlag(st, KING):
				self.canvas.itemconfig(self.stone[idx], width = 3)
			else:
				self.canvas.itemconfig(self.stone[idx], width = 0)
	
	# Set the display options of board
	def SetBoard(self, marked, *idxList):
		for idx in idxList:
			if marked:
				self.canvas.itemconfig(self.board[idx], fill = COLOUR_MARKED)
			else:
				self.canvas.itemconfig(self.board[idx], fill = COLOUR_NORMAL)
	
	# Show the given move in animation.
	# st: The state of the stone being moved
	def Move(self, move, st):
		prev = move[0]
		self.SetBoard(False, prev)
		for this in move[1: ]:
			self.SetBoard(False, this)
			self.SetStone(st, this)
			
			d = GetDirection(prev, this)
			while prev != this:
				self.SetStone(EMPTY, prev)
				prev = Adjacent(prev, d)
			
			self.canvas.update_idletasks()
			time.sleep(0.5)
		
		if (this<=5 and HasFlag(st, WHITE)) or (this>=46 and HasFlag(st, BLACK)):
			self.SetStone(st|KING, this)
		self.canvas.update_idletasks()
		
	# Deal with mouse events and call back
	def EventHandler(self, event):
		dispatcher = self.canvas.find_withtag(tkinter.CURRENT)  # get the object that trigger the event
		if len(dispatcher)==0:  # illegal
			return
		if dispatcher[0] in self.board:  # clicked on the board
			self.Callback(self.board.index(dispatcher[0]), BOARD)
		else:  # clicked at a stone
			self.Callback(self.stone.index(dispatcher[0]), STONE)
	