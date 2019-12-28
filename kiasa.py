from chess import *
from copy import deepcopy as copy
import pathos.pools as p


class Kiasa:
	def __init__(self, depth=2, max_d=1<<15):
		self.chess = Chess()
		self.depth = depth
		self.max_d = max_d


	def __call__(self):
		moves = self.chess.legal_moves()
		if len(moves) == 1:
			dom, sub = moves[0]
			return dom, sub
		with p.ProcessPool(4) as pool:
			func = lambda x: self.minimax(copy(self.chess), x[0], x[1], self.depth, d=len(moves))
			values = {k: v for k, v in zip(moves, pool.map(func, moves))}
		try:
			if self.chess.colour == 'W':
				dom, sub = max(values.items(), key=lambda x: x[1])[0]
			elif self.chess.colour == 'B':
				dom, sub = min(values.items(), key=lambda x: x[1])[0]
		except:
			print('RESIGN')
			quit()
		self.chess(dom, sub)
		return dom, sub


	def minimax(self, chess, dom, sub, n, u=0, d=0):
		chess(dom, sub)
		#if n == 0:
		#	return chess.utility()
		moves = chess.legal_moves()
		d_next = d * max(len(moves), 1)
		if d_next > self.max_d and n <= 0:
			util = chess.utility()
			return util
		if chess.colour == 'W':
			#if u > 0 and util > 0:
			#	return float('-inf')
			try:
				return max(self.minimax(copy(chess), dom, sub, n-1, d=d_next) for dom, sub in moves)
			except:
				return float('-inf')
		elif chess.colour == 'B':
			#if u > 0 and util > 0:
			#	return float('inf')
			try:
				return min(self.minimax(copy(chess), dom, sub, n-1, d=d_next) for dom, sub in moves)
			except:
				return float('inf')
