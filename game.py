import chess
from random import choice
from time import perf_counter
import chess.svg
from svglib.svglib import svg2rlg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io


# Constants
PAWN_WEIGHT=1
KNIGHT_WEIGHT=3
BISHOP_WEIGHT=3
ROOK_WEIGHT=5
QUEEN_WEIGHT=9
DEPTH=3
INF=100000

# Information
recursive_calls = 0
sum_recursive_calls = 0
move_count = 0


def game_loop(board):
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

        # computer_move, computer_move_evl = minimax(board, depth=4)
        computer_move, computer_move_evl = alpha_beta_minimax(board, depth=DEPTH, alpha=-INF, beta=INF)
        move_count += 1
        sum_recursive_calls += recursive_calls

        after_time = perf_counter()

        print(f"Computer move chosen as {computer_move}, with an evaluation of {computer_move_evl}.")
        print(f"Move chosen in {after_time-before_time:0.4f} seconds; {recursive_calls} recursive calls.")

        board.push(computer_move)
        print(board)
        display_board(board)


# TODO: Refactor this function
# Notes on Alpha Beta pruning
# 
# alpha represents the minimum score white is assured,
# beta represents the maximum score black is assured
# 
# alpha starts at -infinity, beta starts at infinity (worst possible scores)
# 
# nodes cease to be explored when the maximum score that black is assured is
# is less than the minimum score that white is assured
# 
def alpha_beta_minimax(board, depth, alpha, beta) -> (chess.Move, int):
    global recursive_calls  #   Used for debugging/useful stats
    recursive_calls += 1

    if depth == 0:
        evl = dumb_evl(board)
        return (None, evl)
    
    # root_moves = dict.fromkeys(board.legal_moves)
    root_moves = dict.fromkeys(get_ordered_legal_moves(board))
    for move in root_moves:
        analysis_board = board.copy()
        analysis_board.push(move)

        if analysis_board.is_game_over(claim_draw=True):   # Don't need to continue here if game over
            evl = INF if analysis_board.result()=='1-0' else -INF if analysis_board.result()=='0-1' else 0
            if board.turn == chess.WHITE:
                alpha = max(alpha, evl)
            else:
                beta = min(beta, evl)
            return (move, evl)
        
        best_move, minimax_evl = alpha_beta_minimax(analysis_board, depth-1, alpha, beta)
        root_moves[move] = minimax_evl
        
        if board.turn == chess.WHITE:
            alpha = max(alpha, minimax_evl)
        else:
            beta = min(beta, minimax_evl)
        
        if beta < alpha:
            break
    
    move_evls = [evl for evl in root_moves.values() if evl is not None]

    best_evl = max(move_evls) if board.turn==chess.WHITE else min(move_evls)
    candidate_moves = [move for move,evl in root_moves.items() if evl==best_evl]
    
    return (choice(candidate_moves), best_evl)


def minimax(board, depth) -> (chess.Move, int):
    global recursive_calls  #   Used for debugging/useful stats
    recursive_calls += 1
    
    if depth == 0:
        evl = dumb_evl(board)
        return (None, evl)
    
    root_moves = dict.fromkeys(board.legal_moves)
    for move in root_moves:
        analysis_board = board.copy()
        analysis_board.push(move)

        if analysis_board.is_game_over(claim_draw=True):   # Don't need to continue here if game over
            return (move, INF if analysis_board.result()=='1-0' else -INF if analysis_board.result()=='0-1' else 0)
        
        best_move, minimax_evl = minimax(analysis_board, depth-1)
        root_moves[move] = minimax_evl
    
    best_evl = max(root_moves.values()) if board.turn==chess.WHITE else min(root_moves.values())
    candidate_moves = [move for move,evl in root_moves.items() if evl==best_evl]
    
    return (choice(candidate_moves), best_evl)


# TODO: Take the following into account:
#       pins, castling, doubled pawns, any other positional stuff
def dumb_evl(analysis_board):
    # "dumb" because just counting weighted material
    if analysis_board.is_game_over(claim_draw=True):   # If game is over, don't bother
        return INF if analysis_board.result()=='1-0' else -INF if analysis_board.result()=='0-1' else 0

    white_evl = count_material(analysis_board, chess.WHITE)
    black_evl = count_material(analysis_board, chess.BLACK)
    evl = white_evl - black_evl         # White is "winning" if evl > 0, else black

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


# Returning legal moves, attempting to order s.t. alpha beta minimax is optimized
def get_ordered_legal_moves(board):
    legal_moves = list(board.legal_moves)
    ordered_legal_moves = []
    for move in legal_moves:
        ordered_legal_moves.insert(0 if board.is_capture(move) else len(ordered_legal_moves), move)
        # if board.is_capture(move):
        #     # ordered_legal_moves.append(legal_moves.pop(move))
        #     ordered_legal_moves.insert(0, move)
        # else:
        #     ordered_legal_moves.append()
    # ordered_legal_moves += legal_moves
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
    plt.pause(0.5)


if __name__=='__main__':
    plt.figure(num=f"depth={DEPTH}", figsize=(4.5,4.5))

    board = chess.Board()

    print(board)
    display_board(board)

    game_loop(board)

    print(f"The game is over, {board.result()}")
    ave_recursive_calls = sum_recursive_calls / move_count
    print(f"Average number of recursive calls for this game: {ave_recursive_calls}")
    plt.ioff()

