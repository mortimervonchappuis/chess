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
			['RB', 'NB', 'BB', 'QB', 'KB', 'BB', 'NB', 'RB', ],]
		self.colour = 'W'
		self.rocharde_white_left = True
		self.rocharde_white_right = True
		self.rocharde_black_left = True
		self.rocharde_black_right = True


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
			i, j = dom
			result = self.move(dom, sub)
			if self.board[i][j][0] == 'K':
				if self.colour == 'W':
					self.rocharde_white_left = False
					self.rocharde_white_right = False
				elif self.colour == 'B':
					self.rocharde_black_left = False
					self.rocharde_black_right = False
			if self.board[i][j][0] == 'R':
				if self.colour == 'W':
					if j == 0:
						self.rocharde_white_left = False
					elif j == 7:
						self.rocharde_white_right = False
				elif self.colour == 'B':
					if j == 0:
						self.rocharde_black_left = False
					elif j == 7:
						self.rocharde_black_right = False
			self.board = result
			return result
		else:
			return False


	def move(self, dom, sub):
		board = copy(self.board)
		i_d, j_d = dom
		i_s, j_s = sub
		if board[i_d][j_d][0] == 'K':
			if self.colour == 'W':
				if self.rocharde_white_left and j_s == 7:
					board[i_s][4:] = ['  ', 'RW', 'KW', '  ']
					return board
				elif self.rocharde_white_right and j_s == 0:
					board[i_s][:5] = ['  ', '  ', 'KW', 'RW', '  ']
					return board
			elif self.colour == 'B':
				if self.rocharde_black_left and j_s == 7:
					board[i_s][4:] = ['  ', 'RB', 'KB', '  ']
					return board
				elif self.rocharde_black_right and j_s == 0:
					board[i_s][:5] = ['  ', '  ', 'KB', 'RB', '  ']
					return board
		if board[i_d][j_d][0] == 'P':
			if self.colour == 'W' and i_d == 6:
				board[i_s][j_s] = 'QW'
				board[i_d][j_d] = '  '
				return board
			elif self.colour == 'B' and i_d == 1:
				board[i_s][j_s] = 'QB'
				board[i_d][j_d] = '  '
				return board
		board[i_s][j_s] = board[i_d][j_d]
		board[i_d][j_d] = '  '
		return board


	def legal(self, dom, sub):
		i_d, j_d = dom
		i_s, j_s = sub
		if self.board[i_d][j_d][1] != self.colour:
			return False
		board = self.move(dom, sub)
		if self.check(board):
			print('CHECK')
			return False
		figure = self.board[i_d][j_d][0]
		if figure == 'P':
			return sub in self.pawn(dom)
		elif figure == 'K':
			return sub in self.king(dom)
		elif figure == 'Q':
			return sub in self.queen(dom)
		elif figure == 'B':
			return sub in self.bishop(dom)
		elif figure == 'N':
			return sub in self.knight(dom)
		elif figure == 'R':
			return sub in self.rook(dom)
		else:
			return False


	def check(self, board, colour=None):
		if colour is None:
			colour = self.colour
		king = self.find(board, 'K'+colour)
		if king:
			for i in range(8):
				for j in range(8):
					if board[i][j][1] != self.inv(colour):
						continue
					else:
						figure = board[i][j][0]
						if figure == 'P' and king in self.pawn((i, j), board, self.inv(colour)):
							return True
						elif figure == 'K' and king in self.king((i, j), board, self.inv(colour)):
							return True
						elif figure == 'Q' and king in self.queen((i, j), board, self.inv(colour)):
							return True
						elif figure == 'B' and king in self.bishop((i, j), board, self.inv(colour)):
							return True
						elif figure == 'N' and king in self.knight((i, j), board, self.inv(colour)):
							return True
						elif figure == 'R' and king in self.rook((i, j), board, self.inv(colour)):
							return True
		return False


	def find(self, board, figure):
		for i in range(8):
			for j in range(8):
				if board[i][j] == figure:
					return (i, j)
		return False


	def pawn(self, dom, board=None, colour=None):
		if board is None:
			board = self.board
		if colour is None:
			colour = self.colour
		moves = []
		i, j = dom
		if colour == 'W':
			if i == 1 and board[i+1][j] == '  ' and board[i+2][j] == '  ':
				moves.append((i+2, j))
			if 0 < i < 7:
				if board[i+1][j] == '  ':
					moves.append((i+1, j))
				if 0 < j < 7 and board[i+1][j+1][1] in (' ', 'B'):
					moves.append((i+1, j+1))
				if 0 < j < 7 and board[i+1][j-1][1] in (' ', 'B'):
					moves.append((i+1, j-1))
		elif colour == 'B':
			if i == 6 and board[i-1][j] == '  ' and board[i-2][j] == '  ':
				moves.append((i-2, j))
			if 0 < i < 7:
				if board[i-1][j] == '  ':
					moves.append((i-1, j))
				if 0 < j < 7 and board[i-1][j+1][1] in (' ', 'W'):
					moves.append((i-1, j+1))
				if 0 < j < 7 and board[i-1][j-1][1] in (' ', 'W'):
					moves.append((i-1, j-1))
		return moves


	def king(self, dom, board=None, colour=None):
		if board is None:
			board = self.board
		if colour is None:
			colour = self.colour
		def helper(self, moves, i, j):
			if not (0 <= i < 8 and 0 <= j < 8):
				return
			if board[i][j][1] in (' ', self.inv(colour)):
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
		if colour == 'W':
			if board[i][1:4] == ['  ', '  ', '  '] and self.rocharde_white_left:
				moves.append((i, 0))
			elif board[i][5:7] == ['  ', '  '] and self.rocharde_white_right:
				moves.append((i, 7))
		if colour == 'B':
			if board[i][1:4] == ['  ', '  ', '  '] and self.rocharde_black_left:
				moves.append((i, 0))
			elif board[i][5:7] == ['  ', '  '] and self.rocharde_black_right:
				moves.append((i, 7))
		return moves


	def queen(self, dom, board=None, colour=None):
		if board is None:
			board = self.board
		if colour is None:
			colour = self.colour
		def helper(self, i, j, moves, trans):
			tmp_i, tmp_j = trans(i, j)
			while 0 <= tmp_i < 8 and 0 <= tmp_j < 8 and board[tmp_i][tmp_j][1] == ' ':
				moves.append((tmp_i, tmp_j))
				tmp_i, tmp_j = trans(tmp_i, tmp_j)
			if 0 <= tmp_i < 8 and 0 <= tmp_j < 8 and board[tmp_i][tmp_j][1] == self.inv(colour):
				moves.append((tmp_i, tmp_j))
		moves = []
		i, j = dom
		helper(self, i, j, moves, lambda x, y: (x+1, y+1))
		helper(self, i, j, moves, lambda x, y: (x+1, y))
		helper(self, i, j, moves, lambda x, y: (x+1, y-1))
		helper(self, i, j, moves, lambda x, y: (x, y+1))
		helper(self, i, j, moves, lambda x, y: (x, y-1))
		helper(self, i, j, moves, lambda x, y: (x-1, y+1))
		helper(self, i, j, moves, lambda x, y: (x-1, y))
		helper(self, i, j, moves, lambda x, y: (x-1, y-1))
		return moves


	def bishop(self, dom, board=None, colour=None):
		if board is None:
			board = self.board
		if colour is None:
			colour = self.colour
		def helper(self, i, j, moves, trans):
			tmp_i, tmp_j = trans(i, j)
			while 0 <= tmp_i < 8 and 0 <= tmp_j < 8 and board[tmp_i][tmp_j][1] == ' ':
				moves.append((tmp_i, tmp_j))
				tmp_i, tmp_j = trans(tmp_i, tmp_j)
			if 0 <= tmp_i < 8 and 0 <= tmp_j < 8 and board[tmp_i][tmp_j][1] == self.inv(colour):
				moves.append((tmp_i, tmp_j))
		moves = []
		i, j = dom
		helper(self, i, j, moves, lambda x, y: (x+1, y+1))
		helper(self, i, j, moves, lambda x, y: (x+1, y-1))
		helper(self, i, j, moves, lambda x, y: (x-1, y+1))
		helper(self, i, j, moves, lambda x, y: (x-1, y-1))
		return moves


	def rook(self, dom, board=None, colour=None):
		if board is None:
			board = self.board
		if colour is None:
			colour = self.colour
		def helper(self, i, j, moves, trans):
			tmp_i, tmp_j = trans(i, j)
			while 0 <= tmp_i < 8 and 0 <= tmp_j < 8 and board[tmp_i][tmp_j][1] == ' ':
				moves.append((tmp_i, tmp_j))
				tmp_i, tmp_j = trans(tmp_i, tmp_j)
			if 0 <= tmp_i < 8 and 0 <= tmp_j < 8 and board[tmp_i][tmp_j][1] == self.inv(colour):
				moves.append((tmp_i, tmp_j))
		moves = []
		i, j = dom
		helper(self, i, j, moves, lambda x, y: (x+1, y))
		helper(self, i, j, moves, lambda x, y: (x, y+1))
		helper(self, i, j, moves, lambda x, y: (x, y-1))
		helper(self, i, j, moves, lambda x, y: (x-1, y))
		return moves


	def knight(self, dom, board=None, colour=None):
		if board is None:
			board = self.board
		if colour is None:
			colour = self.colour
		def helper(self, moves, i, j):
			if not (0 <= i < 8 and 0 <= j < 8):
				return
			if board[i][j][1] in (' ', self.inv(colour)):
				moves.append((i, j))
		moves = []
		i, j = dom
		helper(self, moves, i+1, j+2)
		helper(self, moves, i+1, j-2)
		helper(self, moves, i-1, j+2)
		helper(self, moves, i-1, j-2)
		helper(self, moves, i+2, j+1)
		helper(self, moves, i+2, j-1)
		helper(self, moves, i-2, j+1)
		helper(self, moves, i-2, j-1)
		return moves
