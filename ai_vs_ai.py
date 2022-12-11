from game import Game
from agent import AlphaBetaAgent, NewAgent

def print_board(board):
    for i in range(15):
        for j in range(15):
            print(board[i][j].value, end = " ")
        print("")

if __name__ == "__main__":
    game = Game(NewAgent(), AlphaBetaAgent())

    t = 0

    winner = None
    while game.get_running():
        # if t == 10:
        #     break
        
        game.set_running(False)
        if game.check_full_board():
            break

        x, y = game.next_round()
        winner = game.judge(x, y)
        if not winner:
            game.set_running(True)

        t += 1

    if winner:
        print(winner)
    else:
        print("tie")
    print_board(game.get_board())