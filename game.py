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
        # computer_move = generate_half_move_ahead(board)
        computer_move = generate_minimax_move(board)

        print(f"\n{computer_move}\n")
        board.push(computer_move)
        print(board)


def generate_half_move_ahead(board, max=True):
    legal_moves_list = list(board.legal_moves)

    move_evals = []
    for move in legal_moves_list:
        move_evals.append(dumb_move_eval(board.copy(), move))
    
    best_eval = max(move_evals) if max else min(move_evals)

    candidate_moves = []
    for idx, move_eval in enumerate(move_evals):
        if move_eval == best_eval:
            candidate_moves.append(legal_moves_list[idx])
    
    best_move = generate_random_move(candidate_moves)

    print(f"\nThe best move is {best_move} with a score of {best_eval}")
    
    return (best_move, best_eval)


def generate_minimax_move(board, num_moves_ahead=1):
    root_moves = list(board.legal_moves)
    root_moves_evals = []
    for root_move in root_moves:
        analysis_board = board.copy()
        analysis_board.push(root_move)
        opp_moves = list(analysis_board.legal_moves)
        best_opp_move, best_opp_eval = generate_half_move_ahead(analysis_board, max=False)
        root_moves_evals.append(best_opp_eval)
    best_eval = max(root_moves_evals)
    candidate_moves = []
    for idx, move_eval in enumerate(root_moves_evals):
        if move_eval == best_eval:
            candidate_moves.append(root_moves[idx])
    
    best_move = generate_random_move(candidate_moves)
    return best_move


def generate_random_move(move_list):
    random_int_choice = randint(0,len(move_list)-1)
    move = move_list[random_int_choice]
    return move


def dumb_move_eval(analysis_board, move):
    before_white_score = count_material(analysis_board, chess.WHITE)
    before_black_score = count_material(analysis_board, chess.BLACK)
    before_eval = before_black_score - before_white_score

    analysis_board.push(move)
    after_white_score = count_material(analysis_board, chess.WHITE)
    after_black_score = count_material(analysis_board, chess.BLACK)
    after_eval = after_black_score - after_white_score
    if analysis_board.is_game_over():
        return 100000 if analysis_board.result()=='0-1' else -100000

    return after_eval - before_eval


def count_material(board, color):
    material_count = (
        PAWN_WEIGHT*len(board.pieces(chess.PAWN,color)) +
        KNIGHT_WEIGHT*len(board.pieces(chess.KNIGHT,color)) +
        BISHOP_WEIGHT*len(board.pieces(chess.BISHOP,color)) +
        ROOK_WEIGHT*len(board.pieces(chess.ROOK,color)) +
        QUEEN_WEIGHT*len(board.pieces(chess.QUEEN,color))
    )

    return material_count


if __name__=='__main__':
    board = chess.Board()
    print(board)
    game_loop(board)
    print("The game is over")

