import chess
from random import choice
from time import perf_counter


# Constants
PAWN_WEIGHT=1
KNIGHT_WEIGHT=3
BISHOP_WEIGHT=3
ROOK_WEIGHT=5
QUEEN_WEIGHT=9

# Information
recursive_calls = 0


def game_loop(board):
    global recursive_calls

    while not board.is_game_over():
        user_move_str = input("Enter move:      ")
        user_move = chess.Move.from_uci(user_move_str)

        while user_move not in list(board.legal_moves):
            print("\n***** illegal move *****\n")
            user_move_str = input("Enter move:      ")
            user_move = chess.Move.from_uci(user_move_str)

        board.push(user_move)
        print(board)

        if board.is_game_over():
            break
        
        recursive_calls = 0
        before_time = perf_counter()
        computer_move, computer_move_evl = recursive_minimax(board, num_half_moves_ahead=3)
        after_time = perf_counter()
        print(f"Computer move chosen as {computer_move}, with an evaluation of {computer_move_evl}.")
        print(f"Move chosen in {after_time-before_time:0.4f} seconds; {recursive_calls} recursive calls.")

        board.push(computer_move)
        print(board)


def generate_half_move_ahead(board, maximize=True):
    legal_moves = dict.fromkeys(board.legal_moves)

    for move in legal_moves.keys():
        analysis_board = board.copy()
        analysis_board.push(move)
        legal_moves[move] = dumb_evl(analysis_board)
    
    best_evl = max(legal_moves.values()) if maximize else min(legal_moves.values())

    candidate_moves = [move for move,evl in legal_moves.items() if evl==best_evl]

    best_move = choice(candidate_moves)
    
    return (best_move, best_evl)


def recursive_minimax(board, num_half_moves_ahead) -> (chess.Move, int):
    global recursive_calls
    recursive_calls += 1
    
    if num_half_moves_ahead == 1:
        best_move, best_evl = generate_half_move_ahead(board, maximize=board.turn==chess.WHITE)
        return (best_move, best_evl)
    
    root_moves = dict.fromkeys(board.legal_moves)
    for move in root_moves:
        analysis_board = board.copy()
        analysis_board.push(move)

        if analysis_board.is_game_over():
            return (move, 100000 if analysis_board.result()=='1-0' else -100000 if analysis_board.result()=='0-1' else 0)
        else:
            best_move, minimax_evl = recursive_minimax(analysis_board, num_half_moves_ahead-1)
            root_moves[move] = minimax_evl
    
    best_evl = max(root_moves.values()) if board.turn==chess.WHITE else min(root_moves.values())
    candidate_moves = [move for move,evl in root_moves.items() if evl==best_evl]
    
    return (choice(candidate_moves), best_evl)


def dumb_evl(analysis_board):
    # This is "dumb" because we're just counting material
    white_evl = count_material(analysis_board, chess.WHITE)
    black_evl = count_material(analysis_board, chess.BLACK)
    evl = white_evl - black_evl
    if analysis_board.is_game_over():
        return 100000 if analysis_board.result()=='1-0' else -100000 if analysis_board.result()=='0-1' else 0

    return evl


def count_material(analysis_board, color):
    material_count = (
        PAWN_WEIGHT*len(analysis_board.pieces(chess.PAWN,color)) +
        KNIGHT_WEIGHT*len(analysis_board.pieces(chess.KNIGHT,color)) +
        BISHOP_WEIGHT*len(analysis_board.pieces(chess.BISHOP,color)) +
        ROOK_WEIGHT*len(analysis_board.pieces(chess.ROOK,color)) +
        QUEEN_WEIGHT*len(analysis_board.pieces(chess.QUEEN,color))
    )

    return material_count


if __name__=='__main__':
    board = chess.Board()
    print(board)
    game_loop(board)
    print(f"The game is over, {board.result()}")

