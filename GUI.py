from tkinter import *
from PIL import Image, ImageTk
from game import Game
from time import sleep
from playsound import playsound


def mouse_click(event=None):
	global first, second, game
	if game.chess.colour == 'B':
		return
	x = event.x
	y = event.y
	for row in range(8):
		for column in range(8):
			if ((row * 100 + 50 - y) ** 2 + (column * 100 + 50 - x) ** 2) ** 0.5 <= 50:
				if first == ():
					first = (row, column)
				else:
					second = (row, column)
					if game(first, second):
						board_update()
						game.answer()
						board_update()
					first, second = (), ()


def board_update():
	global game, master, full_board
	newboard = Image.open("board.png")
	newboard = newboard.resize((800,800), Image.ANTIALIAS)
	for i  in range(8):
		for j in range(8):
			figure = game.board[i][j]
			if figure != '  ':
				newboard.paste(eval(figure.lower()), (j*100 , i*100), eval(figure.lower()))
	img = ImageTk.PhotoImage(newboard)
	global full_board
	full_board.configure(image=img)
	full_board.image = img
	master.update()
	playsound('placement.mp3')
	return


master = Tk()
master.title("KIASA Chess-Engine") # (Kasparow Is A Sexist Arsehole)
board = Image.open("board.png")

rw = Image.open("rook_white.png")
nw = Image.open("knight_white.png")
bw = Image.open("bishop_white.png")
kw = Image.open("king_white.png")
qw = Image.open("queen_white.png")
pw = Image.open("pawn_white.png")
rb = Image.open("rook_black.png")
nb = Image.open("knight_black.png")
bb = Image.open("bishop_black.png")
kb = Image.open("king_black.png")
qb = Image.open("queen_black.png")
pb = Image.open("pawn_black.png")

rw = rw.resize((100,100), Image.ANTIALIAS)
nw = nw.resize((100,100), Image.ANTIALIAS)
bw = bw.resize((100,100), Image.ANTIALIAS)
kw = kw.resize((100,100), Image.ANTIALIAS)
qw = qw.resize((100,100), Image.ANTIALIAS)
pw = pw.resize((100,100), Image.ANTIALIAS)
rb = rb.resize((100,100), Image.ANTIALIAS)
nb = nb.resize((100,100), Image.ANTIALIAS)
bb = bb.resize((100,100), Image.ANTIALIAS)
kb = kb.resize((100,100), Image.ANTIALIAS)
qb = qb.resize((100,100), Image.ANTIALIAS)
pb = pb.resize((100,100), Image.ANTIALIAS)

tkimage = ImageTk.PhotoImage(board)
full_board = Label(master, image=tkimage)
full_board.pack()
full_board.bind("<ButtonPress-1>", func=mouse_click)
game = Game()
first = ()
second = ()
board_update()
master.mainloop()
