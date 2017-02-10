class ChessBoard:
	def __init__(self,setupType=0):
		self.squares = [['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e'],
						['e','e','e','e','e','e','e','e']]

		if setupType == 0:
			self.squares[0] = ['bR','bT','bB','bQ','bK','bB','bT','bR']
			self.squares[1] = ['bP','bP','bP','bP','bP','bP','bP','bP']
			self.squares[2] = ['e','e','e','e','e','e','e','e']
			self.squares[3] = ['e','e','e','e','e','e','e','e']
			self.squares[4] = ['e','e','e','e','e','e','e','e']
			self.squares[5] = ['e','e','e','e','e','e','e','e']
			self.squares[6] = ['wP','wP','wP','wP','wP','wP','wP','wP']
			self.squares[7] = ['wR','wT','wB','wQ','wK','wB','wT','wR']

	def GetState(self):
		return self.squares

	def Con_Move_to__horoof(self,moveTupleList):
		newTupleList = []
		for move in moveTupleList:
			newTupleList.append((self.Con_to_horoof(move[0]),self.Con_to_horoof(move[1])))
		return newTupleList

	def Con_square_to_horoof(self,list):
		newList = []
		for square in list:
			newList.append(self.Con_to_horoof(square))
		return newList

	def Con_to_horoof(self,a):
		#converting from (0,0) to (7,7) to a1....a8...h1....h8 .
		return  self.Con_to_horoof_col(a[1]) + self.Con_to_horoof_row(a[2])

    def Con_to_horoof_row(self,row):
		B = ['8','7','6','5','4','3','2','1']
		return B[row]

	def Con_to_horoof_col(self,col):
		A = ['a','b','c','d','e','f','g','h']
		return A[col]


	def GetFullString(self,p):
		if 'b' in p:
			name = "black "
		else:
			name = "white "
		if 'P' in p:
			name = name + "pawn"
		if 'R' in p:
			name = name + "rook"
		if 'T' in p:
			name = name + "knight"
		if 'B' in p:
			name = name + "bishop"
		if 'Q' in p:
			name = name + "queen"
		if 'K' in p:
			name = name + "king"
		return name

	def MovePiece(self,moveTuple):
		fromsquare_raw = moveTuple[0][0]
		fromSquare_column = moveTuple[0][1]
		toSquare_raw = moveTuple[1][0]
		toSquare_column = moveTuple[1][1]

		fromPiece = self.squares[fromsquare_raw][fromSquare_column]
		toPiece = self.squares[toSquare_raw][toSquare_column]

		self.squares[toSquare_raw][toSquare_column] = fromPiece
		self.squares[fromsquare_raw][fromSquare_column] = 'e'

		fromPiece_fullString = self.GetFullString(fromPiece)
		toPiece_fullString = self.GetFullString(toPiece)

		if toPiece == 'e':
			messageString = fromPiece_fullString+ " moves from "+self.Con_to_horoof(moveTuple[0])+" to "+self.Con_to_horoof(moveTuple[1])
		else:
			messageString = fromPiece_fullString+ " from "+self.Con_to_horoof(moveTuple[0])+" captures "+toPiece_fullString+" at "+self.Con_to_horoof(moveTuple[1])+"!"
		return messageString
