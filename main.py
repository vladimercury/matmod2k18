from client import Client
from prisoner import Prisoner
from sys import stderr

client = Client()
prisoner = Prisoner()

i = 0


def print_dot():
    global i
    if i < 150:
        print("-", end="")
        i += 1
    else:
        print("-")
        i = 0


while True:
    if client.receive() is None:
        continue

    if client.is_game_start:
        print_dot()
        client.send_move(prisoner.makeFirstMove(client.game_id, client.game_hand, client.game_params))
    elif client.is_turn_over:
        print_dot()
        client.send_move(prisoner.makeNextMove(client.game_id, client.game_moves))
    elif client.is_game_over:
        i = 0
        print("\nGame {} over with scores {}".format(client.game_id, client.game_scores))
        prisoner.acceptResult(client.game_id, client.game_scores)
    else:
        print("Unknown state:", client.state, file=stderr)
        break
