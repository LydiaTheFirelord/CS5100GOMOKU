import time

from game import Game, Piece
from agent import AlphaBetaAgent, NewAgent, NewAlphaBetaAgent

TEST_TIME = 5

def print_board(board):
    for i in range(15):
        for j in range(15):
            print(board[i][j].value, end = " ")
        print("")

def single_run(agent_black, agent_white, print):
    game = Game(agent_black, agent_white)
    winner = None

    while game.get_running():
        game.set_running(False)
        if game.check_full_board():
            break

        x, y = game.next_round()
        winner = game.judge(x, y)
        if not winner:
            game.set_running(True)

    if print:
        print_board(game.get_board())

    if winner == Piece.Black:
        return "black"
    elif winner == Piece.White:
        return "white"
    else:
        return "tie"

if __name__ == "__main__":
    game = Game(NewAgent(), NewAlphaBetaAgent())
    agent1 = NewAgent()
    agent2 = NewAlphaBetaAgent()

    result = {"agent1": 0, "agent2": 0, "tie": 0}
    duration = list()
    for i in range(TEST_TIME):
        start = time.time()
        winner = single_run(agent1, agent2, False)
        end = time.time()
        
        if winner == "black":
            result["agent1"] += 1
        elif winner == "white":
            result["agent2"] += 1
        else:
            result["tie"] += 1
        duration.append(end - start)

        # Switch color
        start = time.time()
        winner = single_run(agent2, agent1, False)
        end = time.time()
        
        if winner == "black":
            result["agent2"] += 1
        elif winner == "white":
            result["agent1"] += 1
        else:
            result["tie"] += 1
        duration.append(end - start)

    print(result)
    print(duration)