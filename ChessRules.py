class ChessRules:
	def listofvalidmoves(self,board,color,fromTuple): ## list hameye harakat haye sahih momken ro barmigardune
		list = []
		for row in range(8):
			for col in range(8):
				d = (row,col)
				if self.Sah_move(board,color,fromTuple,d):
					if not self.chek_Achmaz(board,color,fromTuple,d):
						list.append(d)
		return list

	def Sah_move(self,board,color,fromTuple,toTuple): ##chek mikone ke aya harakat doroste y na

		fromSquare_raw = fromTuple[0]
		fromSquare_columnolumn = fromTuple[1]
		toSquare_raw = toTuple[0]
		toSquare_column = toTuple[1]
		fromPiece = board[fromSquare_raw][fromSquare_column]
		toPiece = board[toSquare_raw][toSquare_column]

		if color == "black":
			harifColor = 'w'
		if color == "white":
			harifColor = 'b'

		if fromTuple == toTuple:
			return False

		if "P" in fromPiece:
			#Pawn
			if color == "black":
				if toSquare_raw == fromSquare_raw-1 and toSquare_column == fromSquare_column and toPiece == 'e':
					#ye harakat be jolo
					return True
				if fromSquare_raw == 6 and toSquare_raw == fromSquare_raw-2 and toSquare_column == fromSquare_column and toPiece == 'e':
					#2harakat be jolo
					if self.Chek_Masir(board,fromTuple,toTuple):
						return True
				if toSquare_raw == fromSquare_raw-1 and (toSquare_column == fromSquare_column-1 or toSquare_column == fromSquare_column+1) and harifColor in toPiece:
					#harakat qotrie sarbaz
					return True

			elif color == "white":
				if toSquare_raw == fromSquare_raw+1 and toSquare_column == fromSquare_column and toPiece == 'e':
					return True
				if fromSquare_raw == 1 and toSquare_raw == fromSquare_raw+2 and toSquare_column == fromSquare_column and toPiece == 'e':
					if self.Chek_Masir(board,fromTuple,toTuple):
						return True
				if toSquare_raw == fromSquare_raw+1 and (toSquare_column == fromSquare_column+1 or toSquare_column == fromSquare_column-1) and harifColor in toPiece:
					return True

		elif "R" in fromPiece:
			#Rook
			if (toSquare_raw == fromSquare_raw or toSquare_column == fromSquare_column) and (toPiece == 'e' or harifColor in toPiece):
				if self.Chek_Masir(board,fromTuple,toTuple):
					return True

		elif "T" in fromPiece:
			#Knight
			col_diff = toSquare_column - fromSquare_column
			row_diff = toSquare_raw - fromSquare_raw
			if toPiece == 'e' or harifColor in toPiece:
				if col_diff == 1 and row_diff == -2:
					return True
				if col_diff == 2 and row_diff == -1:
					return True
				if col_diff == 2 and row_diff == 1:
					return True
				if col_diff == 1 and row_diff == 2:
					return True
				if col_diff == -1 and row_diff == 2:
					return True
				if col_diff == -2 and row_diff == 1:
					return True
				if col_diff == -2 and row_diff == -1:
					return True
				if col_diff == -1 and row_diff == -2:
					return True

		elif "B" in fromPiece:
			#Bishop
			if ( abs(toSquare_raw - fromSquare_raw) == abs(toSquare_column - fromSquare_column) ) and (toPiece == 'e' or harifColor in toPiece):
				if self.Chek_Masir(board,fromTuple,toTuple):
					return True

		elif "Q" in fromPiece:
			#Queen
			if (toSquare_raw == fromSquare_raw or toSquare_column == fromSquare_column) and (toPiece == 'e' or harifColor in toPiece):
				if self.Chek_Masir(board,fromTuple,toTuple):
					return True
			if ( abs(toSquare_raw - fromSquare_raw) == abs(toSquare_column - fromSquare_column) ) and (toPiece == 'e' or harifColor in toPiece):
				if self.Chek_Masir(board,fromTuple,toTuple):
					return True

		elif "K" in fromPiece:
			#King
			col_diff = toSquare_column - fromSquare_column
			row_diff = toSquare_raw - fromSquare_raw
			if toPiece == 'e' or harifColor in toPiece:
				if abs(col_diff) == 1 and abs(row_diff) == 0:
					return True
				if abs(col_diff) == 0 and abs(row_diff) == 1:
					return True
				if abs(col_diff) == 1 and abs(row_diff) == 1:
					return True

		return False

	def chek_Achmaz(self,board,color,fromTuple,toTuple): ##harakato anajm mide va chek mikone bbine ke achmaz hast ya na!!!

        fromSquare_raw = fromTuple[0]
		fromSquare_column = fromTuple[1]
		toSquare_raw = toTuple[0]
		toSquare_column = toTuple[1]
		fromPiece = board[fromSquare_raw][fromSquare_column]
		toPiece = board[toSquare_raw][toSquare_column]
		board[toSquare_raw][toSquare_column] = fromPiece
		board[fromSquare_raw][fromSquare_column] = 'e'
		res = self.chek_kish(board,color)
		board[toSquare_raw][toSquare_column] = toPiece
		board[fromSquare_raw][fromSquare_column] = fromPiece

		return res

	def chek_kish(self,board,color):
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
			harifColorFull = 'white'
		else:
			myColor = 'w'
			harifColor = 'b'
			harifColorFull = 'black'
		kingTuple = (0,0)   ##jaye shah ro aval peyda mikonim
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if 'K' in piece and myColor in piece:
					kingTuple = (row,col)
		for row in range(8):  ## harakat haye harifo chek mikonim bbinim be khune shah mikhore ya na
			for col in range(8):
				piece = board[row][col]
				if harifColor in piece:
					if self.Sah_move(board,harifColorFull,(row,col),kingTuple):
						return True
		return False


    def kishomat(self,board,color):
        if color == "black":
            myColor = 'b'
            harifColor = 'w'
        else:
            myColor = 'w'
            harifColor = 'b'

        myColorValidMoves = [];
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if myColor in piece:
                    b=(row,col)
                    myColorValidMoves.extend(self.listofvalidmoves(board,color,b))

        if len(myColorValidMoves) == 0:
            return True
        else:
            return False


	def Chek_Masir(self,board,fromTuple,toTuple):  ## masir ro chek mikone ke teyye ye harakat too masir chizi nabashe, ye tabe bazgashti hast!

		fromSquare_raw = fromTuple[0]
		fromSquare_column = fromTuple[1]
		toSquare_raw = toTuple[0]
		toSquare_column = toTuple[1]
		fromPiece = board[fromSquare_raw][fromSquare_column]

		if abs(fromSquare_raw - toSquare_raw) <= 1 and abs(fromSquare_column - toSquare_column) <= 1:
			return True
		else:
			if toSquare_raw > fromSquare_raw and toSquare_column == fromSquare_column:
				#amoodi roo be bala
				newTuple = (fromSquare_raw+1,fromSquare_column)
			elif toSquare_raw < fromSquare_raw and toSquare_column == fromSquare_column:
				#amoodi roo be pain
				newTuple = (fromSquare_raw-1,fromSquare_column)
			elif toSquare_raw == fromSquare_raw and toSquare_column > fromSquare_column:
				#ofofqi roo be rast
				newTuple = (fromSquare_raw,fromSquare_column+1)
			elif toSquare_raw == fromSquare_raw and toSquare_column < fromSquare_column:
				#ofoqi roo be chap
				newTuple = (fromSquare_raw,fromSquare_column-1)
			elif toSquare_raw > fromSquare_raw and toSquare_column > fromSquare_column:
				#qotri be shomal sharq
				newTuple = (fromSquare_raw+1,fromSquare_column+1)
			elif toSquare_raw > fromSquare_raw and toSquare_column < fromSquare_column:
				#qotri be shomal gharb
				newTuple = (fromSquare_raw+1,fromSquare_column-1)
			elif toSquare_raw < fromSquare_raw and toSquare_column > fromSquare_column:
				#qotri be jonoob sharq
				newTuple = (fromSquare_raw-1,fromSquare_column+1)
			elif toSquare_raw < fromSquare_raw and toSquare_column < fromSquare_column:
				#qotri be jonoob gharb
				newTuple = (fromSquare_raw-1,fromSquare_column-1)

		if board[newTuple[0]][newTuple[1]] != 'e':
			return False
		else:
			return self.Chek_Masir(board,newTuple,toTuple)
