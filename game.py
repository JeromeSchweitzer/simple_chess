import chess
from time import sleep
from random import randint



def random_move(board):
    legal_moves_list = list(board.legal_moves)
    random_int_choice = randint(0,board.legal_moves.count()-1)
    move = legal_moves_list[random_int_choice]
    return move



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

    computer_move = random_move(board)

    print()
    print(computer_move)
    print()
    board.push(computer_move)

print("The game is over")