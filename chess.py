from copy import deepcopy as copy


class Chess:
	def __init__(self, board=None):
		if board is None:
			self.board = [
			['RW', 'NW', 'BW', 'QW', 'KW', 'BW', 'NW', 'RW', ],
			['PW', 'PW', 'PW', 'PW', 'PW', 'PW', 'PW', 'PW', ],
			['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
			['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
			['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
			['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
			['PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB', ],
			['RB', 'NB', 'BB', 'QB', 'KB', 'BB', 'NB', 'RB', ]]
		self.colour = 'W'
		self.rocharde_white = True
		self.rocharde_black = True


	def inv(self, colour):
		if colour == 'W':
			return 'B'
		elif colour == 'B':
			return 'W'
		else:
			raise Exception(f'Colour {colour} does not exsist.')


	def toggle(self):
		self.colour = self.inv(self.colour)


	def __call__(self, dom, sub):
		if self.legal(dom, sub):
			result = self.move(dom, sub)
			self.board = result
			return result
		else:
			return False


	def move(self, dom, sub):
		board = copy(self.board)
		i_d, j_d = dom
		i_s, j_s = sub
		board[i_s][j_s] = board[i_d][j_d]
		board[i_d][j_d] = '  '
		return board


	def legal(self, dom, sub):
		i_d, j_d = dom
		i_s, j_s = sub
		board = self.move(dom, sub)
		if self.check(board):
			return False
		figure = self.board[i_d][j_d][0]
		if figure == 'P':
			return sub in self.pawn(dom)
		elif figure == 'K':
			return sub in self.king(dom)
		#elif figure == 'Q':
		#	return sub in self.queen(dom)
		#elif figure == 'B':
		#	return sub in self.bishop(dom)
		#elif figure == 'N':
		#	return sub in self.knight(dom)
		#elif figure == 'R':
		#	return sub in self.rook(dom)
		else:
			return True


	def check(self, board):
		return False


	def pawn(self, dom):
		moves = []
		i, j = dom
		if self.colour == 'W':
			if i == 1 and self.board[i+1][j] == '  ' and self.board[i+2][j] == '  ':
				moves.append((i+2, j))
			if 0 < i < 7:
				if self.board[i+1][j] == '  ':
					moves.append((i+1, j))
				if 0 < j < 7 and self.board[i+1][j+1][1] in (' ', 'B'):
					moves.append((i+1, j+1))
				if 0 < j < 7 and self.board[i+1][j-1][1] in (' ', 'B'):
					moves.append((i+1, j-1))
		elif self.colour == 'B':
			if i == 6 and self.board[i-1][j] == '  ' and self.board[i-2][j] == '  ':
				moves.append((i-2, j))
			if 0 < i < 7:
				if self.board[i-1][j] == '  ':
					moves.append((i-1, j))
				if 0 < j < 7 and self.board[i-1][j+1][1] in (' ', 'W'):
					moves.append((i-1, j+1))
				if 0 < j < 7 and self.board[i-1][j-1][1] in (' ', 'W'):
					moves.append((i-1, j-1))
		return moves


	def king(self, dom):
		def helper(self, moves, i, j):
			if not (0 < i < 7 and 0 < j < 7):
				return
			if self.board[i][j] in (' ', self.inv(self.colour)):
				moves.append((i, j))
		moves = []
		i, j = dom
		helper(self, moves, i+1, j+1)
		helper(self, moves, i+1, j)
		helper(self, moves, i+1, j-1)
		helper(self, moves, i, j+1)
		helper(self, moves, i, j-1)
		helper(self, moves, i-1, j+1)
		helper(self, moves, i-1, j)
		helper(self, moves, i-1, j-1)
		return moves

