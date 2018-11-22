# Requirements: https://pypi.org/project/websocket-client/
from websocket import create_connection
import json
import random


def receive():
    result = json.loads(ws.recv())
    if result["state"]=="error":
        print("Error: {}".format(result["error"]))
        return None
    return result


def send(msg):
    ws.send(json.dumps(msg))


if __name__ == "__main__":
    random.seed()

    print("Creating connection")
    ws = create_connection("ws://212.71.248.74:3012")

    print("Receiving game name.")
    result = receive()
    assert(result["state"]=="info")
    print("Playing \"{}\", version {}".format(result["name"], result["version"]))

    print("Sending authorization")
    send({"state":"login"})
    result = receive()
    if result is None:
        print("Access denied")
        exit(1)
    assert(result["state"] == "access")
    print("Logged as {}".format(result["user"]))

    print("Waiting for server")
    while True:
        result = receive()
        if result is None: continue
        game = result["game"]
        if result["state"]=="start":
            print("New game {} as hand {}".format(game, result["hand"]))
            print("Game parameters: {}".format(result["parameters"]))
        elif result["state"]=="gameover":
            print("Game {} is finished with scores {}".format(game,result["scores"]))
            continue
        elif result["state"]=="opponent":
            print("Opponent {} have made move {}".format(result['opponent'], result["strategy"]))
            pass
        else: 
            print("Unknown message: {}".format(result))
            exit(1)

        move = random.choice([0, 1])
        print("Making move {}".format(move))
        send({"state":"move", "strategy": move, "game": game})