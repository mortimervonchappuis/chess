class Chess:
	def __init__(self):
		self.board = [
		['RW', 'NW', 'BW', 'QW', 'KW', 'BW', 'NW', 'RW', ],
		['PW', 'PW', 'PW', 'PW', 'PW', 'PW', 'PW', 'PW', ],
		['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
		['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
		['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
		['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
		['PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB', ],
		['RB', 'NB', 'BB', 'QB', 'KB', 'BB', 'NB', 'RB', ]]
		self.colour = "W"
		self.rocharde_white = True
		self.rocharde_black = True


	def legal_moves(self):
		moves = []
		for i in range(8):
			for j in range(8):
				if self.board[i][j][1] == self.colour:
					moves.extend(self.moves(i, x))
		return moves


	def moves(self, x, y):
		figure = self.board[i][j][0]
		colour = self.board[i][j][1]
		if figure == 'P':
			return self.pawn(i, j, colour)
		elif figure == 'R':
			return self.rook(i, j, colour)
		elif figure == 'N':
			return self.knight(i, j, colour)
		elif figure == 'B':
			return self.bishop(i, j, colour)
		elif figure == 'Q':
			return self.queen(i, j, colour)
		elif figure == 'K':
			return self.king(i, j, colour)
		else:
			raise Exception(f'ERROR! figure {figure} not defined.')


	def check(self, colour=None, board=None):
		if colour is None:
			colour = self.colour
		if board is None:
			board = self.board
		for i in range(8):
			for j in range(8):
				if board[i][j] == 'K'+colour:
					king = i, j
		for i in range(8):
			for j in range(8):
				if board[i][j][1] == self.inv(colour):
					figure = board[i][j][0]
					if self.targets(figure, colour, (i, j), king, board):
						return True
		return False


	def targets(self, figure, colour, dom, sub, board):
		i_d, j_d = dom
		if figure == 'P':
			i_s, i_s = sub
			if colour == 'W':
				return i_d - i_s == 1 and abs(j_d - j_s) == 1
			elif colour = 'B':
				return i_d - i_s == -1 and abs(j_d - j_s) == 1
		elif figure == 'R':
			return sub in self.rook(i_d, j_d, colour, board)
		elif figure == 'N':
			return sub in self.knight(i_d, j_d, colour, board)
		elif figure == 'B':
			return sub in self.bishop(i_d, j_d, colour, board)
		elif figure == 'Q':
			return sub in self.queen(i_d, j_d, colour, board)
		elif figure == 'K':
			return sub in self.king(i_d, j_d, colour, board)
		else:
			raise Exception(f'ERROR! figure {figure} not defined.')
		

	def inv(self, colour):
		if colour == 'W':
			return 'B'
		elif colour == 'B':
			return 'W'
		else:
			raise Exception(f'ERROR! colour {colour} not defined.')


	def move(self, dom, sub, board):
		i_d, j_d = dom
		i_s, j_s = sub
		board[i_s][j_s] = board[i_d][j_d]
		board[i_d][j_d] = '  '
		return board


	def pawn(self, i, j, colour, board=None):
		moves = []
		if board is None:
			board = self.board
		if colour == 'W':
			if i == 1 and board[i + 1][j] == '  ':
				if not self.check(self.inv(colour), self.move((i, j), (i + 2, j), board)):
					moves.append((i + 2, j))
			if not self.check(self.inv(colour), self.move((i, j), (i + 1, j), board)):
				moves.append((i + 1, j))
			if board[i + 1][j + 1][1] == self.inv(colour) and not self.check(self.inv(colour), self.move((i, j), (i + 1, j + 1), board)): 
				moves.append((i + 1, j + 1))
			if board[i + 1][j - 1][1] == self.inv(colour) and not self.check(self.inv(colour), self.move((i, j), (i + 1, j - 1), board)): 
				moves.append((i + 1, j - 1))
		elif colour == 'B':
			if i == 6 and board[i - 1][j] == '  ':
				if not self.check(self.inv(colour), self.move((i, j), (i - 2, j), board)):
					moves.append((i - 2, j))
			if not self.check(self.inv(colour), self.move((i, j), (i - 1, j), board)):
				moves.append((i - 1, j))
			if board[i - 1][j + 1][1] == self.inv(colour) and not self.check(self.inv(colour), self.move((i, j), (i - 1, j + 1), board)): 
				moves.append((i + 1, j + 1))
			if board[i - 1][j - 1][1] == self.inv(colour) and not self.check(self.inv(colour), self.move((i, j), (i - 1, j - 1), board)): 
				moves.append((i - 1, j - 1))
		return moves


	def rook(self, i, j, colour, board=None):
		moves = []
		if board is None:
			board = self.board
		tmp = i
		while 0 < tmp < 7 and board[tmp+1][j][1] != colour:
			tmp += 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp, j), board)):
				moves.append((tmp, j))
		tmp = i
		while 0 < tmp < 7 and board[tmp-1][j][1] != colour:
			tmp -= 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp, j), board)):
				moves.append((tmp, j))
		tmp = j
		while 0 < tmp < 7 and board[i][tmp+1][1] != colour:
			tmp += 1
			if not self.check(self.inv(colour), self.move((i, j), (i, tmp), board)):
				moves.append((i, tmp))
		tmp = j
		while 0 < tmp < 7 and board[i][tmp-1][1] != colour:
			tmp -= 1
			if not self.check(self.inv(colour), self.move((i, j), (i, tmp), board)):
				moves.append((i, tmp))
		return moves


	def bishop(self, i, j, colour, board=None):
		moves = []
		if board is None:
			board = self.board
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp+1][tmp_j+1][1] != colour:
			tmp_i += 1
			tmp_j += 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp+1][tmp_j-1][1] != colour:
			tmp_i += 1
			tmp_j -= 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp-1][tmp_j+1][1] != colour:
			tmp_i -= 1
			tmp_j += 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp-1][tmp_j-1][1] != colour:
			tmp_i -= 1
			tmp_j -= 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		return moves


	def queen(self, i, j, colour, board=None):
		moves = []
		if board is None:
			board = self.board
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp+1][tmp_j+1][1] != colour:
			tmp_i += 1
			tmp_j += 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp+1][tmp_j-1][1] != colour:
			tmp_i += 1
			tmp_j -= 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp-1][tmp_j+1][1] != colour:
			tmp_i -= 1
			tmp_j += 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i, j
		while 0 < tmp_i < 7 and 0 < tmp_j < 7 and board[tmp-1][tmp_j-1][1] != colour:
			tmp_i -= 1
			tmp_j -= 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
				moves.append((tmp_i, tmp_j))
		tmp = i
		while 0 < tmp < 7 and board[tmp+1][j][1] != colour:
			tmp += 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp, j), board)):
				moves.append((tmp, j))
		tmp = i
		while 0 < tmp < 7 and board[tmp-1][j][1] != colour:
			tmp -= 1
			if not self.check(self.inv(colour), self.move((i, j), (tmp, j), board)):
				moves.append((tmp, j))
		tmp = j
		while 0 < tmp < 7 and board[i][tmp+1][1] != colour:
			tmp += 1
			if not self.check(self.inv(colour), self.move((i, j), (i, tmp), board)):
				moves.append((i, tmp))
		tmp = j
		while 0 < tmp < 7 and board[i][tmp-1][1] != colour:
			tmp -= 1
			if not self.check(self.inv(colour), self.move((i, j), (i, tmp), board)):
				moves.append((i, tmp))
		return moves


	def knight(self, i, j, colour, board=None):
		moves = []
		if board is None:
			board = self.board
		tmp_i, tmp_j = i+1, j+2
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-1, j+2
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i+1, j-2
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-1, j-2
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i+2, j+1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i+2, j-1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-2, j+1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-2, j-1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		return moves


	def king(self, i, j, colour, board=None):
		moves = []
		if board is None:
			board = self.board
		tmp_i, tmp_j = i+1, j+1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-1, j+1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i+1, j-1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-1, j-1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i+1, j+1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i+1, j-1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-1, j+1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		tmp_i, tmp_j = i-1, j-1
		if 0 < tmp_i < 7 and 0 < tmp_j < 7 and not self.check(self.inv(colour), self.move((i, j), (tmp_i, tmp_j), board)):
			moves.append((tmp_i, tmp_j))
		return moves
