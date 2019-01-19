# Requirements: https://pypi.org/project/websocket-client/
from websocket import create_connection
from math import ceil
import json
import random

# URL = "ws://localhost:3012"
URL = "ws://dmc.alepoydes.com:3012"

LOGIN = "Как тебе такое, Илон Маск?"
PASSWORD = "ysakci0g0sBqrtq29wbWy8pPZLGdS8Fw5FijNT2gRdpTSnvGpLfChq0kYgPgZv2a"
DEBUG = False

def receive():
    result = json.loads(ws.recv())
  #  print("in:", result)
    if result["state"]=="error":
        print("Error: {}".format(result["error"]))
        return None
    return result

def send(msg):
  #  print("out:", msg)
    ws.send(json.dumps(msg))

if __name__ == "__main__":
    random.seed()
    ws = create_connection(URL)
    result = receive()
    assert(result["state"]=="info")
    print("Playing \"{}\", version {}".format(result["name"], result["version"]))

    send({"state": "login", "login": LOGIN, "password": PASSWORD, "debug": DEBUG})
    result = receive()
    if result is None:
        print("Access denied")
        exit(1)
    assert(result["state"]=="access")
    print("Logged as {} {}".format(result["user"], "(debug)" if result["debug"] else "(release)"))

    myHand = 0
    competitor = 1

    while True:
        result = receive()
        isFirstTurn = False
        isFirstTurnDone = False
        eyeTurns = 0
        isCompetitorRandomFriendly = True
        isEyeInitialized = False
        numberOfIdentificationTurns = 10
        numberOfBadRandomMoves = 0
        payMatrix = []
        isEyeBetter = False
        if result is None: continue
        game = result["game"]
        if result["state"]=="start":
            print("New game {} as hand {}".format(game, result["hand"]))
            print("Game parameters: {}".format(result["parameters"]))
            isFirstTurn = True
            myHand = result["hand"]
            payMatrix = result["parameters"]["payoff"]
            isEyeBetter = payMatrix[0][0][0] * 2 < payMatrix[0][1][0] + payMatrix[0][1][1]
            competitor = abs(result["hand"] - 1)
        elif result["state"]=="gameover":
            print("Game {} is finished with scores {}".format(game,result["scores"]))
            continue
        elif result["state"]=="turnover":
            print("Game {} end of turn, players moves are {}".format(game, result["moves"]))
            pass
        else:
            print("Unknown message: {}".format(result))
            exit(1)

        if isFirstTurn:
            move = 1
            isFirstTurn = False
            isFirstTurnDone = True
            numberOfIdentificationTurns -= 1
        else:
            numberOfIdentificationTurns -= 1
            if isFirstTurnDone:
                isFirstTurnDone = False
                if result["moves"][competitor] == 0:
                    isCompetitorRandomFriendly = False

            if numberOfIdentificationTurns > 0:
                move = result["moves"][competitor]
                if move == 0:
                    numberOfBadRandomMoves += 1
                if result["moves"][competitor] != result["moves"][myHand]:
                    eyeTurns += 1
                else:
                    eyeTurns = 0
            else:
                if numberOfBadRandomMoves >= 8:
                    move = 0
                elif ceil(eyeTurns) / 2 == numberOfBadRandomMoves and not isEyeBetter:
                    move = 0
                elif ceil(eyeTurns) / 2 < numberOfBadRandomMoves:
                    move = 0
                elif isEyeBetter and eyeTurns == 0 and not isEyeInitialized:
                    isEyeInitialized = True
                    move = 0
                else:
                    move = result["moves"][competitor]
        send({"state":"move", "strategy": move, "game": game})