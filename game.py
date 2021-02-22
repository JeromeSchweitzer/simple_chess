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
        user_move = get_user_move(board)

        board.push(user_move)
        print(board)

        if board.is_game_over():
            break
        
        recursive_calls = 0
        before_time = perf_counter()
        computer_move, computer_move_evl = recursive_minimax(board, depth=3)
        after_time = perf_counter()
        
        print(f"Computer move chosen as {computer_move}, with an evaluation of {computer_move_evl}.")
        print(f"Move chosen in {after_time-before_time:0.4f} seconds; {recursive_calls} recursive calls.")

        board.push(computer_move)
        print(board)


def recursive_minimax(board, depth) -> (chess.Move, int):
    global recursive_calls  #   Used for debugging/useful stats
    recursive_calls += 1
    
    if depth == 0:
        evl = dumb_evl(board)
        return (None, evl)
    
    root_moves = dict.fromkeys(board.legal_moves)
    for move in root_moves:
        analysis_board = board.copy()
        analysis_board.push(move)

        if analysis_board.is_game_over():   # Don't need to continue here if game over
            return (move, 100000 if analysis_board.result()=='1-0' else -100000 if analysis_board.result()=='0-1' else 0)
        else:
            best_move, minimax_evl = recursive_minimax(analysis_board, depth-1)
            root_moves[move] = minimax_evl
    
    best_evl = max(root_moves.values()) if board.turn==chess.WHITE else min(root_moves.values())
    candidate_moves = [move for move,evl in root_moves.items() if evl==best_evl]
    
    return (choice(candidate_moves), best_evl)


def dumb_evl(analysis_board):
    # This is "dumb" because we're just counting material
    if analysis_board.is_game_over():   # If game is over, don't bother
        return 100000 if analysis_board.result()=='1-0' else -100000 if analysis_board.result()=='0-1' else 0

    white_evl = count_material(analysis_board, chess.WHITE)
    black_evl = count_material(analysis_board, chess.BLACK)
    evl = white_evl - black_evl

    return evl


def count_material(analysis_board, color):
    material_count = (
        PAWN_WEIGHT     * len(analysis_board.pieces(chess.PAWN,color)) +
        KNIGHT_WEIGHT   * len(analysis_board.pieces(chess.KNIGHT,color)) +
        BISHOP_WEIGHT   * len(analysis_board.pieces(chess.BISHOP,color)) +
        ROOK_WEIGHT     * len(analysis_board.pieces(chess.ROOK,color)) +
        QUEEN_WEIGHT    * len(analysis_board.pieces(chess.QUEEN,color))
    )

    return material_count


def get_user_move(board):
    user_move = None
    valid_move = False

    while not valid_move:
        user_input = input("Enter move:      ")
        try:
            user_move = board.parse_san(user_input)
            valid_move = True
        except:
            try:
                user_move = board.parse_uci(user_input)
                valid_move = True
            except:
                print("\n***** cannot parse input *****\n")
        if valid_move and user_move not in board.legal_moves:
            valid_move = False
            print("\n***** illegal move *****\n")

    return user_move


if __name__=='__main__':
    board = chess.Board()
    print(board)
    game_loop(board)
    print(f"The game is over, {board.result()}")

