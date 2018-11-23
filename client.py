from websocket import create_connection
from json import loads, dumps
from sys import stderr


class Client:
    def __init__(self, logging=False):
        self._url = "ws://dmc.alepoydes.com:3012"
        self._logging = logging

        self._socket = None

        self._error = None
        self._name = None
        self._state = None
        self._version = None
        self._user = None

        self._result = {}
        self._start()

    def _save_result(self, result):
        is_dict = isinstance(result, dict)
        self._result = result if is_dict else {}
        self._state = result.get("state") if is_dict else None
        self._error = result.get("error") if is_dict else None
        if self._state == "info":
            self._name = result.get("name")
            self._version = result.get("version")
        elif self._state == "access":
            self._user = result.get("user")

    def _start(self):
        self._socket = create_connection(self._url)

        print("Starting...", end=" ")
        self.receive()
        print("started {} v{}".format(self._name, self._version))

        self._send({"state": "login"})
        print("Logging in...", end=" ")
        if self.receive() is None:
            raise RuntimeError("Error logging in")
        print("logged as", self._user)
        return self

    def _send(self, message):
        self._socket.send(dumps(message))

    def receive(self):
        result = loads(self._socket.recv())
        self._save_result(result)
        if self._state == "error":
            print("Error: ", self._error, file=stderr)

        return result

    def send_move(self, move):
        self._send({
            "state": "move",
            "strategy": move,
            "game": self.game_id
        })

    @property
    def game_id(self):
        return self._result.get("game")

    @property
    def game_hand(self):
        return self._result.get("hand")

    @property
    def game_moves(self):
        return self._result.get("moves")

    @property
    def game_params(self):
        return self._result.get("parameters")

    @property
    def game_scores(self):
        return self._result.get("scores")

    @property
    def is_game_start(self):
        return self._state == "start"

    @property
    def is_game_over(self):
        return self._state == "gameover"

    @property
    def is_turn_over(self):
        return self._state == "turnover"

    @property
    def state(self):
        return self._state