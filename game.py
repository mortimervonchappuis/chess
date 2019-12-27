from chess import *
from kiasa import *


class Game:
	def __init__(self):
		self.chess = Chess()
		self.board = self.chess.board
		self.kiasa = Kiasa()


	def __call__(self, dom, sub):
		result = self.chess(dom, sub)
		if result:
			self.board = result
			self.kiasa.chess(dom, sub)
			return True
		else:
			return False


	def answer(self):
		dom, sub = self.kiasa()
		self.board = self.chess(dom, sub)
