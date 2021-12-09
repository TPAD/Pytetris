#!/usr/bin/python

import random
from Tkinter import*		

class Tetris:
	#game piece as 2d array of bool
	iPiece = [ [1, 1, 1, 1] ]
	jPiece = [ [1, 0, 0], [1, 1, 1] ]
	lPiece = [ [0, 0, 1], [1, 1, 1] ]
	sPiece = [ [0, 1, 1], [1, 1, 0] ]
	tPiece = [ [0, 1, 0], [1, 1, 1] ]
	zPiece = [ [1, 1, 0], [0, 1, 1] ]
	oPiece = [ [1, 1], [1, 1] ]

	pieces  = [iPiece, jPiece, lPiece, sPiece, tPiece, zPiece, oPiece]
	pColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
	#piece IN PLAY
	pIP 	= iPiece;	pIPC 	= "red"	
	pIPRow  = 0;		pIPCol  = 0	
	# size of board
	rows = 18; cols = 10
	# background, foreground and multiplier constants
	bg 		= 25;		fg 	 = 24
	C 		= 30;	border 	 = bg - fg
	score 	= 0;	gameOver = False

	# reference to the colors that appear on the board
	colorRef = [];	bgColor = "#FF5733"

	def __init__(self):
		w = self.C * self.cols; h = self.C * self.rows
		root = Tk()
		root.wm_title("TETRIS")
		# makes root window a fixed size
		root.resizable(width=0, height=0)
		root.bind("<Key>", lambda event: self.buttons(canvas, event))
		#add canvas widget
		canvas = Canvas(root, width=w, height=h)
		canvas.pack()
		self.setupGame(canvas)
		root.mainloop()

	def makeColorList(self, r, c, color):
		lis = []
		for i in range(r):
			lis += [[color] * c]
		return lis

	def makeColorListRef(self):
		self.colorRef = self.makeColorList(self.rows, self.cols, self.bgColor)

	def setupGame(self, canvas):
		self.drawGameRect(canvas)
		self.makeColorListRef()
		self.drawBoard(canvas)
		self.spawnNewPiece(canvas)
		self.timerFired(canvas)

	def drawGameRect(self, canvas):
		width 	= self.C * self.cols
		height 	= self.C * self.rows
		canvas.create_rectangle(0, 0, width, height, fill="#A9DFBE")

	def drawCell(self, canvas, row, col, color):
		bg 	  = self.bg;		 top = 2*self.rows + 10
		left  = 2*self.cols + 5; x	 = bg*col + left
		y 	  = top + bg*row;    w 	 = x + bg
		h 	  = y + bg 
		canvas.create_rectangle(x, y, w, h, fill="black")
		canvas.create_rectangle(x+1, y+1, w-1, h-1, fill=color)

	def drawBoard(self, canvas):
		for row in range(self.rows):
			for col in range(self.cols):
				self.drawCell(canvas, row, col, self.colorRef[row][col])

	def spawnNewPiece(self, canvas):
		pieceNum = random.randint(0, (len(self.pieces)-1))
		self.pIP = self.pieces[pieceNum]
		self.pIPC = self.pColors[pieceNum]
		self.pIPRow = 0
		self.pIPCol = (self.cols - len(self.pIP[0]))/2

	def drawPieceInPlay(self, canvas):
		for row in range(len(self.pIP)):
			for col in range(len(self.pIP[0])):
				if self.pIP[row][col]:
					r = self.pIPRow + row
					c = self.pIPCol + col
					self.drawCell(canvas, r, c, self.pIPC)

	def drawGameOverMsg(self, canvas):
		x = (self.C * self.cols)/2
		y = (self.C * self.rows)/2
		font = "Times New Roman"
		size = 2*self.cols
		canvas.create_text(x, y, text="GAME OVER", font=(font, size, "bold"))

	def redrawAll(self, canvas):
		canvas.delete("all")
		self.drawGameRect(canvas)
		self.drawBoard(canvas)
		self.drawPieceInPlay(canvas)
		self.drawScore(canvas)
		if self.gameOver:
			self.drawGameOverMsg(canvas)

	def legal(self, new_r, new_c):
		row_range = len(self.pIP)
		col_range = len(self.pIP[0])
		for row in range(row_range):
			for col in range(col_range):
				if self.pIP[row][col]:
					if (((new_r + row) < 0) or ((new_r + row) > (self.rows - 1))
					    or (new_c + col < 0) or (new_c + col) > (self.cols - 1)):
							return False
					elif self.colorRef[new_r + row][new_c + col] in self.pColors:
						return False
		return True

	def pieceIPMotion(self, canvas, r, c):
		new_r = self.pIPRow + r
		new_c = self.pIPCol + c
		if self.legal(new_r, new_c):
			self.pIPRow = new_r
			self.pIPCol = new_c
			return True
		return False

	def pIPCenter(self):
		center_x = self.pIPRow + (len(self.pIP)/2)
		center_y = self.pIPCol + (len(self.pIP[0])/2)
		return (center_x, center_y)

	def rotatePIP(self):
		row = self.pIPRow; col = self.pIPCol
		piece = self.pIP
		(center_x, center_y) = self.pIPCenter()
		pIPRotated = self.makeColorList(len(self.pIP[0]), len(self.pIP), None)
		for r in xrange(len(self.pIP)):
			for c in xrange(len(self.pIP[0])):
				pIPRotated[(len(self.pIP[0]) - c - 1)][r] = self.pIP[r][c]
		self.pIP = pIPRotated
		(new_center_x, new_center_y) = self.pIPCenter()
		new_row = self.pIPRow + (center_x - new_center_x)
		new_col = self.pIPCol + (center_y - new_center_y)
		if self.legal(new_row, new_col):
			self.pIPRow = new_row
			self.pIPCol = new_col


	def placePIP(self):
		for i in xrange(len(self.pIP)):
			for j in xrange(len(self.pIP[0])):
				if self.pIP[i][j]:
					self.colorRef[i + self.pIPRow][j + self.pIPCol] = self.pIPC

	def timerFired(self, canvas):
		if self.gameOver == False:
			self.redrawAll(canvas)
			if not self.pieceIPMotion(canvas, 1, 0):
				self.placePIP()
				self.removeFullRows()
				self.spawnNewPiece(canvas)
				if not self.legal(self.pIPRow, self.pIPCol):
					self.gameOver = True
		def update(): self.timerFired(canvas)
		canvas.after(600, update)

	def drawScore(self, canvas):
		canvas.create_text(40, 15, fill="black",\
						   text="Score: %s" %(str(self.score)))

	def removeFullRows(self):
		count = 0
		for prev in xrange(self.rows-1, 0, -1):
			if not self.bgColor in self.colorRef[prev]:
				for col in xrange(self.cols):
					self.colorRef[prev][col] = self.bgColor
				count += 1
			else:
				self.colorRef[prev + count] = self.colorRef[prev]
		self.score += count**2

	def buttons(self, canvas, event):
		if (event.keysym == "Left"):
			self.pieceIPMotion(canvas, 0, -1)
		elif(event.keysym == "Right"):
			self.pieceIPMotion(canvas, 0, 1)
		elif(event.keysym == "Down"):
			self.pieceIPMotion(canvas, 1, 0)
		elif(event.keysym == "Up"):
			self.rotatePIP()
		elif(event.keysym == "r"):
			self.spawnNewPiece(canvas)
			self.score = 0
			self.makeColorListRef()
			self.gameOver = False
		self.redrawAll(canvas)

Tetris()




