import chess
import random
from os import system


board = chess.Board()


playing = True
turn = False


while playing:
    good_move = True
    turn = not turn
    if turn:
        print("white to move")
    else:
        print("black to move")

    if turn:
        while good_move:
            move = input()
            try:
                board.push_san(move)
            except ValueError:
                good_move = False

            good_move = not good_move
    else:
        board.push(random.choice(list(board.legal_moves)))



    _ = system("cls")
    print(board)

    if board.is_checkmate():
        if turn:
            print("white won!")
        else:
            print("black won!")

        playing = False

    if board.is_stalemate():
        print("stale mate")
        playing = False
