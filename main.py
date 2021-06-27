import random
import chess
import chess.svg
import chess.polyglot
import collections
import chess.pgn
import chess.engine



# Evaluating the board
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval


def alphabeta(board, alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(board, alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(board, -beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(board, alpha, beta):
    stand_pat = evaluate_board(board)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:

        if board.is_capture(move):
            board.push(move)
            score = -quiesce(board, -beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


def select_move(board, depth):
    best_move = chess.Move.null()
    best_value = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves:
        print(move)
        board.push(move)
        board_value = -alphabeta(board, -beta, -alpha, depth - 1)
        if board_value > best_value:
            best_value = board_value
            best_move = move
        if board_value > alpha:
            alpha = board_value
        board.pop()
    return best_move


def board_to_game(board):
    game = chess.pgn.Game()

    # Undo all moves.
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())

    game.setup(board)
    node = game

    # Replay all moves.
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)

    game.headers["Result"] = board.result()
    return game


def main():
    board = chess.Board()

    book_move_count = 0

    engine = chess.engine.SimpleEngine.popen_uci("C:\\files\\chessEn.exe")
    playing = True
    turn = False
    human = True
    bot_white = False

    while playing:
            good_move = True
            turn = not turn

            if turn:
                print("white to move")
                print(evaluate_board(board))
            else:
                print("black to move")

            if not human:
                #print(board_to_game(board))
                pass

            if not turn:

                if bot_white:
                    if not human:
                        engine.play(board, chess.engine.Limit(time=2.0))

                    else:
                        while good_move:
                            move = input()
                            try:
                                board.push_san(move)
                            except ValueError:
                                good_move = False

                            good_move = not good_move
                else:
                    # Ai Logic

                    if book_move_count > 0:
                        best_move = chess.Move.null()
                        with chess.polyglot.open_reader("C:\\Users\\משתמש\\Documents\\projects\\ChessAi\\ChessAi\\performance.bin") as book:
                            best_move = random.choice ([entry.move for entry in book.find_all(board)])

                        book_move_count -= 1


                    else:
                        print("i am here!!!")
                        best_move = select_move(board, 4)

                    board.push(best_move)

            else:
                if bot_white:
                    # Ai Logic

                    if book_move_count > 0:
                        best_move = chess.Move.null()
                        with chess.polyglot.open_reader("performance.bin") as book:
                            best_move = random.choice ([entry.move for entry in book.find_all(board)])

                        book_move_count -= 1


                    else:
                        best_move = select_move(board, 4)

                    board.push(best_move)

                else:
                    if not human:
                        print("engine White")
                        print(board.turn)
                        engine.play(board, chess.engine.Limit(time=2.0))

                    else:
                        while good_move:
                            move = input()
                            try:
                                board.push_san(move)
                            except ValueError:
                                good_move = False

                            good_move = not good_move

            #_ = system("cls")
            if(bot_white):
                print(board.mirror())
            else:
                print(board)

            if board.is_checkmate():
                if turn:
                    print("white won!")
                else:
                    print("black won!")

                playing = False

                engine.close()
                print(board_to_game(board))

            if board.is_stalemate():
                print("stale mate")
                playing = False
                engine.close()
                print(board_to_game(board))

if __name__ == "__main__":
    main()
