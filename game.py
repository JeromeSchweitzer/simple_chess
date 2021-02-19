import chess
from time import sleep
from random import randint

def dumb_move_eval(board, move):
    # Returns True if black has more pieces than white
    before_white_score = (
        len(board.pieces(1,True)) +
        3*len(board.pieces(2,True)) +
        3*len(board.pieces(3,True)) +
        5*len(board.pieces(4,True)) +
        9*len(board.pieces(5,True))
    )
    before_black_score = (
        len(board.pieces(1,False)) +
        3*len(board.pieces(2,False)) +
        3*len(board.pieces(3,False)) +
        5*len(board.pieces(4,False)) +
        9*len(board.pieces(5,False))
    )
    before_eval = before_black_score - before_white_score

    temp_board = board.copy()
    temp_board.push(move)
    after_white_score = (
        len(temp_board.pieces(1,True)) +
        3*len(temp_board.pieces(2,True)) +
        3*len(temp_board.pieces(3,True)) +
        5*len(temp_board.pieces(4,True)) +
        9*len(temp_board.pieces(5,True))
    )
    after_black_score = (
        len(temp_board.pieces(1,False)) +
        3*len(temp_board.pieces(2,False)) +
        3*len(temp_board.pieces(3,False)) +
        5*len(temp_board.pieces(4,False)) +
        9*len(temp_board.pieces(5,False))
    )
    after_eval = after_black_score - after_white_score

    return after_eval - before_eval


def generate_random_move(move_list):
    random_int_choice = randint(0,len(move_list)-1)
    move = move_list[random_int_choice]
    return move

def generate_half_move_ahead(board):
    legal_moves_list = list(board.legal_moves)

    move_evals = []
    for move in legal_moves_list:
        move_evals.append(dumb_move_eval(board, move))
    
    best_eval = max(move_evals)

    candidate_moves = []
    for idx, move_eval in enumerate(move_evals):
        if move_eval == best_eval:
            candidate_moves.append(legal_moves_list[idx])
    
    best_move = generate_random_move(candidate_moves)

    print("The best move is " + str(best_move) + " with a score of " + str(best_eval))
    
    return best_move


board = chess.Board()


while not board.is_game_over():
    print(board)
    user_move_str = input("Enter move:      ")
    user_move = chess.Move.from_uci(user_move_str)

    while user_move not in list(board.legal_moves):
        print("\n***** illegal move *****\n")
        user_move_str = input("Enter move:      ")
        user_move = chess.Move.from_uci(user_move_str)

    board.push(user_move)
    if board.is_game_over():
        break

    print(board)
    sleep(2)

    # computer_move = generate_random_move(list(board.legal_moves))
    computer_move = generate_half_move_ahead(board)

    print()
    print(computer_move)
    print()
    board.push(computer_move)

print("The game is over")