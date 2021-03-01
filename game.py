import sys
import io
from time import perf_counter
from random import choice
import chess
import chess.svg
from svglib.svglib import svg2rlg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Constants
PAWN_WEIGHT=1
KNIGHT_WEIGHT=3
BISHOP_WEIGHT=3
ROOK_WEIGHT=5
QUEEN_WEIGHT=9
CASTLING_RIGHTS_WEIGHT=0.5
INF=100000

# Stats/Debugging
recursive_calls = 0
sum_recursive_calls = 0
move_count = 0


def game_loop(board, depth):
    global recursive_calls
    global move_count
    global sum_recursive_calls

    while not board.is_game_over(claim_draw=True):
        user_move = get_user_move(board)

        board.push(user_move)
        print(board)
        display_board(board)

        if board.is_game_over(claim_draw=True):
            break
        
        recursive_calls = 0
        before_time = perf_counter()

        # computer_move, computer_move_evl = minimax(board, depth=depth)
        computer_move, computer_move_evl = alpha_beta_minimax(board, depth=depth, alpha=-INF, beta=INF)
        move_count += 1
        sum_recursive_calls += recursive_calls

        after_time = perf_counter()

        print(f"Computer move chosen as {computer_move}, with an evaluation of {computer_move_evl}.")
        print(f"Move chosen in {after_time-before_time:0.4f} seconds; {recursive_calls} recursive calls.")

        board.push(computer_move)
        print(board)
        display_board(board)


def minimax(board, depth) -> (chess.Move, int):
    global recursive_calls  # Used for debugging/useful stats
    recursive_calls += 1
    
    if depth == 0 or board.is_game_over(claim_draw=True):   # Base case, either reached end of search or game is over
        evl = dumb_evl(board)
        return (None, evl)
    
    root_moves = dict.fromkeys(board.legal_moves)           # Unlike ab pruning, ordering this list doesn't help
    for move in root_moves:
        analysis_board = board.copy()   # Pushing the move on a copy of the board
        analysis_board.push(move)
        
        _, minimax_evl = minimax(analysis_board, depth-1)   # Only need evaluation here
        root_moves[move] = minimax_evl
    
    best_evl = max(root_moves.values()) if board.turn==chess.WHITE else min(root_moves.values())
    candidate_moves = [move for move,evl in root_moves.items() if evl==best_evl]
    
    return (choice(candidate_moves), best_evl)


# Notes on alpha beta pruning:
# 
# alpha the minimum score white is assured,
# beta the maximum score black is assured
# 
# alpha starts at -infinity, beta starts at infinity (worst possible scores)
# 
# nodes cease to be explored when the maximum score that black is assured is
# is less than the minimum score that white is assured
# 
def alpha_beta_minimax(board, depth, alpha, beta) -> (chess.Move, int):
    global recursive_calls  # Used for debugging/useful stats
    recursive_calls += 1

    if depth == 0 or board.is_game_over(claim_draw=True):
        evl = dumb_evl(board)
        return (None, evl)
    
    root_moves = dict.fromkeys(get_ordered_legal_moves(board))
    for move in root_moves:
        analysis_board = board.copy()
        analysis_board.push(move)
        
        _, minimax_evl = alpha_beta_minimax(analysis_board, depth-1, alpha, beta)
        root_moves[move] = minimax_evl
        
        if board.turn == chess.WHITE:   # Alpha beta pruning bit
            alpha = max(alpha, minimax_evl)
        else:
            beta = min(beta, minimax_evl)
        if beta < alpha:
            break
    
    move_evls = filter(lambda x: x is not None, root_moves.values()) # Filtering out pruned variations

    best_evl = max(move_evls) if board.turn==chess.WHITE else min(move_evls)
    candidate_moves = [move for move,evl in root_moves.items() if evl==best_evl]
    
    return (choice(candidate_moves), best_evl)


# TODO: Take the following into account:
#       pins, castling, doubled pawns, any other positional stuff
def dumb_evl(board):
    if board.is_game_over(claim_draw=True):   # If game is over, don't bother
        return INF if board.result()=='1-0' else -INF if board.result()=='0-1' else 0

    white_evl = count_material(board, chess.WHITE)
    white_evl += CASTLING_RIGHTS_WEIGHT * board.has_castling_rights(chess.WHITE)

    black_evl = count_material(board, chess.BLACK)
    black_evl += CASTLING_RIGHTS_WEIGHT * board.has_castling_rights(chess.BLACK)

    evl = white_evl - black_evl     # White is "winning" if evl > 0, else black

    return evl


def count_material(board, color):
    material_count = (
        PAWN_WEIGHT     * len(board.pieces(chess.PAWN,color)) +
        KNIGHT_WEIGHT   * len(board.pieces(chess.KNIGHT,color)) +
        BISHOP_WEIGHT   * len(board.pieces(chess.BISHOP,color)) +
        ROOK_WEIGHT     * len(board.pieces(chess.ROOK,color)) +
        QUEEN_WEIGHT    * len(board.pieces(chess.QUEEN,color))
    )

    return material_count


def get_ordered_legal_moves(board): # Returning legal moves, attempting to order s.t. alpha beta minimax is optimized
    legal_moves = list(board.legal_moves)
    ordered_legal_moves = []
    for move in legal_moves:
        ordered_legal_moves.insert(0 if board.is_capture(move) else len(ordered_legal_moves), move)
    
    return ordered_legal_moves


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


def display_board(board):
    board_svg_str = chess.svg.board(board)

    board_svg_bytes = io.StringIO(board_svg_str)
    board_rlg = svg2rlg(board_svg_bytes)
    board_png_str = board_rlg.asString("png")
    board_png_bytes = io.BytesIO(board_png_str)
    board_img = mpimg.imread(board_png_bytes, format="PNG")

    plt.axis('off')
    plt.imshow(board_img)
    plt.pause(0.1)


if __name__=='__main__':
    depth = 3 if len(sys.argv) == 1 else int(sys.argv[1])

    plt.figure(num=f"depth={depth}", figsize=(4.5,4.5))

    board = chess.Board()

    print(board)
    display_board(board)

    game_loop(board, depth)

    print(f"The game is over, {board.result()}")
    print(f"Average number of recursive calls for this game: {sum_recursive_calls/move_count:0.3f}")

