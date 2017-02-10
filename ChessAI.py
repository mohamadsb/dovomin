from ChessRules import ChessRules
import random
class ChessAI:
	def __init__(self,name,color):
		self.name = name
		self.color = color
		self.type = 'AI'
		self.Rules = ChessRules()
	def GetName(self):
		return self.name
	def GetColor(self):
		return self.color
	def GetType(self):
		return self.type

class ChessAI_random(ChessAI): #az harakate mojaz ye harakate random migire

	def GetMove(self,board,color):
		myPieces = self.moherehaye_harakatdar(board,color)
		fromTuple = myPieces[random.randint(0,len(myPieces)-1)]
		harakate_mojaz = self.Rules.listofvalidmoves(board,color,fromTuple)
		toTuple = harakate_mojaz[random.randint(0,len(harakate_mojaz)-1)]
		moveTuple = (fromTuple,toTuple)
		return moveTuple

	def moherehaye_harakatdar(self,board,color):
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
		else:
			myColor = 'w'
			harifColor = 'b'

		myPieces = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece:
					if len(self.Rules.listofvalidmoves(board,color,(row,col))) > 0:
						myPieces.append((row,col))

		return myPieces

class ChessAI_defense(ChessAI_random): #tamame harakate mojaze khodam va harif ro chek mikonam
# kheylee sade harakati ke be ye khune montahi mishano hazf mikonam. @ betarze ahmaqane harakati ke harifo kish mikonan
#ro tarjih midam!! :| dar gheire in soorat ye harakat random az mabaqie harakat bar midaram.
	def __init__(self,name,color,protectionPriority=("queen","rook","knight","bishop","pawn")):
		self.piecePriority = protectionPriority
		ChessAI.__init__(self,name,color)
	def GetMove(self,board,color):
		myPieces = self.moherehaye_harakatdar(board,color)
		harifPieces = self.GetharifPiecesWithharakate_mojaz(board,color)
		protectedMoveTuples = self.GetProtectedMoveTuples(board,color,myPieces,harifPieces)
		movesThatPutharifInCheck = self.GetMovesThatPutharifInCheck(board,color,protectedMoveTuples)
		if len(movesThatPutharifInCheck) > 0:
			return movesThatPutharifInCheck[random.randint(0,len(movesThatPutharifInCheck)-1)]
        for pieceType in self.piecePriority: #olaviate 2 inja harakatayi entekhab mishe ke az khatare zade shodan nejat mide
			piecesProtectedMoves = self.GetMovesThatProtectPiece(board,color,pieceType,protectedMoveTuples)
			if len(piecesProtectedMoves) > 0:
				return piecesProtectedMoves[random.randint(0,len(piecesProtectedMoves)-1)]
		#olaviate 3 - harakati entekhab mishe ke ye mohre az harif begire
		for pieceType in self.piecePriority:
			capturePieceMoves = self.GetMovesThatCaptureharifPiece(board,color,pieceType,protectedMoveTuples)
			if len(capturePieceMoves) > 0:
				return capturePieceMoves[random.randint(0,len(capturePieceMoves)-1)]
		#age az olaviat haye 1 ta 3 chzi nabud, yeki az protected haro entekahb mikone
		if len(protectedMoveTuples) > 0:
			return protectedMoveTuples[random.randint(0,len(protectedMoveTuples)-1)]
		else: # age protected ham nabud ye random begir!
			return ChessAI_random.GetMove(self,board,color)
	def GetharifPiecesWithharakate_mojaz(self,board,color):
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
			harifColor_full = 'white'
		else:
			myColor = 'w'
			harifColor = 'b'
			harifColor_full = 'black'
		harifPieces = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if harifColor in piece:
					if len(self.Rules.listofvalidmoves(board,harifColor_full,(row,col))) > 0:
						harifPieces.append((row,col))
		return harifPieces
	def GetProtectedMoveTuples(self,board,color,myPieces,harifPieces):
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
			harifColor_full = 'white'
		else:
			myColor = 'w'
			harifColor = 'b'
			harifColor_full = 'black'
		protectedMoveTuples = []
		for my_p in myPieces:   ## in for ro chek kon shak daram :| :|
			my_harakate_mojaz = self.Rules.listofvalidmoves(board,color,my_p)
			toBeRemoved = []
		    for harif_p in harifPieces:
                harif_moves = self.Rules.listofvalidmoves(board,harifColor_full,harif_p)
                for harif_m in harif_moves:
                    if harif_m in my_harakate_mojaz:
                        toBeRemoved.append(harif_m)
			for remove_m in toBeRemoved:
				if remove_m in my_harakate_mojaz:
					my_harakate_mojaz.remove(remove_m)
			for my_m in my_harakate_mojaz: #now, "dangerous" moves are removed
				protectedMoveTuples.append((my_p,my_m))
		return protectedMoveTuples
	def GetMovesThatProtectPiece(self,board,color,pieceType,protectedMoveTuples):
		piecesProtectedMoves = []
		piecePositions = self.PiecePositions(board,color,pieceType)
		if len(piecePositions)>0:
			for p in piecePositions:
				if self.PieceCanBeCaptured(board,color,p):
					piecesProtectedMoves.extend(self.GetPiecesMovesFromMoveTupleList(p,protectedMoveTuples))
		return piecesProtectedMoves
	def GetMovesThatCaptureharifPiece(self,board,color,pieceType,protectedMoveTuples):
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
			harifColor_full = 'white'
		else:
			myColor = 'w'
			harifColor = 'b'
			harifColor_full = 'black'
		capturePieceMoves = []
		harifPiecePositions = self.PiecePositions(board,harifColor,pieceType)
		if len(harifPiecePositions)>0:
			for p in harifPiecePositions:
				if self.PieceCanBeCaptured(board,harifColor,p):
					capturePieceMoves.extend(self.GetCapturePieceMovesFromMoveTupleList(p,protectedMoveTuples))
		return capturePieceMoves
	def GetMovesThatPutharifInCheck(self,board,color,protectedMoveTuples): #range harif ro midam besh :))
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
			harifColor_full = 'white'
		else:
			myColor = 'w'
			harifColor = 'b'
			harifColor_full = 'black'
		movesThatPutharifInCheck = []
		for mt in protectedMoveTuples:
			if self.Rules.chek_Achmaz(board,harifColor_full,mt[0],mt[1]):
				movesThatPutharifInCheck.append(mt)
		return movesThatPutharifInCheck
	def PiecePositions(self,board,color,pieceType):
		if color == "black":
			myColor = 'b'
		else:
			myColor = 'w'

		if pieceType == "king":
			myPieceType = 'K'
		elif pieceType == "queen":
			myPieceType = 'Q'
		elif pieceType == "rook":
			myPieceType = 'R'
		elif pieceType == "knight":
			myPieceType = 'T'
		elif pieceType == "bishop":
			myPieceType = 'B'
		elif pieceType == "pawn":
			myPieceType = 'P'
		piecePositions = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece and myPieceType in piece:
					piecePositions.append((row,col))
		return piecePositions

	def PieceCanBeCaptured(self,board,color,p):
		if color == "black":
			myColor = 'b'
			harifColor = 'w'
			harifColorFull = 'white'
		else:
			myColor = 'w'
			harifColor = 'b'
			harifColorFull = 'black'

		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if harifColor in piece:
					if self.Rules.Sah_move(board,harifColorFull,(row,col),p):
						return True
		return False

	def GetCapturePieceMovesFromMoveTupleList(self,p,possibleMoveTuples): ##possible hamoon protected ha hastan
		moveTuples = []
		for m in possibleMoveTuples:
			if m[1] == p:
				moveTuples.append(m)
		return moveTuples

	def GetPiecesMovesFromMoveTupleList(self,p,possibleMoveTuples):
		moveTuples = []
		for m in possibleMoveTuples:
			if m[0] == p:
				moveTuples.append(m)
		return moveTuples
class ChessAI_offense(ChessAI_defense):
	def GetMove(self,board,color):
		myPieces = self.moherehaye_harakatdar(board,color)
		harifPieces = self.GetharifPiecesWithharakate_mojaz(board,color)
		#inja AI harakatio tarjih khahad dad ke mana natunam begiram.
		protectedMoveTuples = self.GetProtectedMoveTuples(board,color,myPieces,harifPieces)
		#olaviat aval hamlei ke be man hamle kone
		movesThatPutharifInCheck = self.GetMovesThatPutharifInCheck(board,color,protectedMoveTuples)
		if len(movesThatPutharifInCheck) > 0:
			#print "Picking move that puts harif in check"
			return movesThatPutharifInCheck[random.randint(0,len(movesThatPutharifInCheck)-1)]
		#hamlei mikone ke yeki az mohre haye harifo migire
		for pieceType in self.piecePriority:
			capturePieceMoves = self.GetMovesThatCaptureharifPiece(board,color,pieceType,protectedMoveTuples)
			if len(capturePieceMoves) > 0:
				return capturePieceMoves[random.randint(0,len(capturePieceMoves)-1)]

		#olaviate 3 harakati mkone ke khatar roshu raf kone
		for pieceType in self.piecePriority:
			piecesProtectedMoves = self.GetMovesThatProtectPiece(board,color,pieceType,protectedMoveTuples)
			if len(piecesProtectedMoves) > 0:
				return piecesProtectedMoves[random.randint(0,len(piecesProtectedMoves)-1)]
		#age az 1ta 3 chizi nadasht yeki az protected ha bar midare dg
		if len(protectedMoveTuples) > 0:
			return protectedMoveTuples[random.randint(0,len(protectedMoveTuples)-1)]
		else:
			return ChessAI_random.GetMove(self,board,color)

if __name__ == "__main__":

	from ChessBoard import ChessBoard
	cb = ChessBoard(3)
	board = cb.GetState()
	color = 'black'

	from ChessGUI_pygame import ChessGUI_pygame
	gui = ChessGUI_pygame()
	gui.Draw(board,highlightSquares=[])
	defense = ChessAI_defense('Bob','black')

	myPieces = defense.moherehaye_harakatdar(board,color)
	harifPieces = defense.GetharifPiecesWithharakate_mojaz(board,color)
	protectedMoveTuples = defense.GetProtectedMoveTuples(board,color,myPieces,harifPieces)
	movesThatPutharifInCheck = defense.GetMovesThatPutharifInCheck(board,color,protectedMoveTuples)
	print ("MyPieces = ", cb.ConvertSquareListToAlgebraicNotation(myPieces))
	print ("harifPieces = ", cb.ConvertSquareListToAlgebraicNotation(harifPieces))
	print ("protectedMoveTuples = ", cb.ConvertMoveTupleListToAlgebraicNotation(protectedMoveTuples))
	print ("movesThatPutharifInCheck = ", cb.ConvertMoveTupleListToAlgebraicNotation(movesThatPutharifInCheck))
	#c =raw_input("Press any key to quit.")#pause at the end
