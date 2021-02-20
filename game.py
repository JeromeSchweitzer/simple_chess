import chess
from time import sleep
from random import randint


# Hyperparameters
PAWN_WEIGHT=1
KNIGHT_WEIGHT=3
BISHOP_WEIGHT=3
ROOK_WEIGHT=5
QUEEN_WEIGHT=9


def game_loop(board):
    while not board.is_game_over():
        user_move_str = input("Enter move:      ")
        user_move = chess.Move.from_uci(user_move_str)

        while user_move not in list(board.legal_moves):
            print("\n***** illegal move *****\n")
            user_move_str = input("Enter move:      ")
            user_move = chess.Move.from_uci(user_move_str)

        board.push(user_move)
        print(board)
        sleep(1)

        if board.is_game_over():
            break

        # computer_move = generate_random_move(list(board.legal_moves))
        computer_move = generate_half_move_ahead(board)

        print(f"\n{computer_move}\n")
        board.push(computer_move)
        print(board)


def generate_half_move_ahead(board):
    legal_moves_list = list(board.legal_moves)

    move_evals = []
    for move in legal_moves_list:
        move_evals.append(dumb_move_eval(board.copy(), move))
    
    best_eval = max(move_evals)

    candidate_moves = []
    for idx, move_eval in enumerate(move_evals):
        if move_eval == best_eval:
            candidate_moves.append(legal_moves_list[idx])
    
    best_move = generate_random_move(candidate_moves)

    print(f"\nThe best move is {best_move} with a score of {best_eval}")
    
    return best_move


def generate_random_move(move_list):
    random_int_choice = randint(0,len(move_list)-1)
    move = move_list[random_int_choice]
    return move


def dumb_move_eval(analysis_board, move):
    before_white_score = (
        len(analysis_board.pieces(chess.PAWN,True)) +
        3*len(analysis_board.pieces(2,True)) +
        3*len(analysis_board.pieces(3,True)) +
        5*len(analysis_board.pieces(4,True)) +
        9*len(analysis_board.pieces(5,True))
    )
    before_black_score = (
        len(analysis_board.pieces(1,False)) +
        3*len(analysis_board.pieces(2,False)) +
        3*len(analysis_board.pieces(3,False)) +
        5*len(analysis_board.pieces(4,False)) +
        9*len(analysis_board.pieces(5,False))
    )
    before_eval = before_black_score - before_white_score

    analysis_board.push(move)
    after_white_score = (
        len(analysis_board.pieces(1,True)) +
        3*len(analysis_board.pieces(2,True)) +
        3*len(analysis_board.pieces(3,True)) +
        5*len(analysis_board.pieces(4,True)) +
        9*len(analysis_board.pieces(5,True))
    )
    after_black_score = (
        len(analysis_board.pieces(1,False)) +
        3*len(analysis_board.pieces(2,False)) +
        3*len(analysis_board.pieces(3,False)) +
        5*len(analysis_board.pieces(4,False)) +
        9*len(analysis_board.pieces(5,False))
    )
    after_eval = after_black_score - after_white_score
    if analysis_board.is_game_over():
        return 100000

    return after_eval - before_eval


def count_material(color):
    material_count = (
        PAWN_WEIGHT*len(analysis_board.pieces(chess.PAWN,color)) +
        KNIGHT_WEIGHT*len(analysis_board.pieces(chess.KNIGHT,color)) +
        BISHOP_WEIGHT*len(analysis_board.pieces(chess.BISHOP,color)) +
        ROOK_WEIGHT*len(analysis_board.pieces(chess.ROOK,color)) +
        QUEEN_WEIGHT*len(analysis_board.pieces(chess.QUEEN,color))
    )


if __name__=='__main__':
    board = chess.Board()
    print(board)
    game_loop(board)
    print("The game is over")

