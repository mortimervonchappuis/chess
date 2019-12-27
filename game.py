from chess import *


class Game:
	def __init__(self):
		self.chess = Chess()
		self.board = self.chess.board


	def __call__(self, dom, sub):
		result = self.chess(dom, sub)
		if result:
			self.board = result
			self.chess.toggle()
			return True
		else:
			return False
