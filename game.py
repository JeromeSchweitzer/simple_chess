import chess
from time import sleep
from random import choice


# Constants
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

        if board.is_game_over():
            break
        
        computer_move, computer_move_score = recursive_minimax(board, num_half_moves_ahead=2)
        print(f"Computer move chosen as {computer_move}, with a score of {computer_move_score}.")

        board.push(computer_move)
        print(board)


def generate_half_move_ahead(board, maximize=True):
    legal_moves = dict.fromkeys(board.legal_moves)

    for move in legal_moves.keys():
        analysis_board = board.copy()
        legal_moves[move] = dumb_move_score(analysis_board, move)
    
    best_score = max(legal_moves.values()) if maximize else min(legal_moves.values())

    candidate_moves = [move for move,score in legal_moves.items() if score==best_score]

    best_move = choice(candidate_moves)
    
    return (best_move, best_score)


def recursive_minimax(board, num_half_moves_ahead) -> (chess.Move, int):
    if num_half_moves_ahead == 1:
        best_move, best_score = generate_half_move_ahead(board, maximize=board.turn==chess.BLACK)
        return (best_move, best_score)
    
    root_moves = list(board.legal_moves)
    root_moves_scores = []
    for root_move in root_moves:
        temp_board = board.copy()
        temp_board.push(root_move)
        # try:
        if temp_board.is_game_over():
            return (root_move, 100000 if temp_board.result()=='0-1' else -100000)
        else:
            best_move, best_score = recursive_minimax(temp_board, num_half_moves_ahead-1)
            root_moves_scores.append(best_score)
    
    best_score = max(root_moves_scores) if board.turn==chess.BLACK else min(root_moves_score)
    candidate_moves = []
    for idx, move_score in enumerate(root_moves_scores):
        if move_score == best_score:
            candidate_moves.append(root_moves[idx])
    
    # if num_half_moves_ahead == NUM_MOVES_AHEAD:
    #     print()
    #     print(root_moves)
    #     print(root_moves_evals)
    #     print()
    return (choice(candidate_moves), best_score)


def dumb_move_score(analysis_board, move):
    analysis_board.push(move)
    after_white_score = count_material(analysis_board, chess.WHITE)
    after_black_score = count_material(analysis_board, chess.BLACK)
    after_score = after_black_score - after_white_score
    if analysis_board.is_game_over():
        return 100000 if analysis_board.result()=='0-1' else -100000

    return after_score


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
    print("The game is over")

