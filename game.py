class Game:
    def __init__(self, game_id, hand, params):
        self._id = game_id
        self._hand = hand
        self._params = params or {}
        self._moves = []
        self._last_move = None
        self._scores = None

    @property
    def is_final(self):
        return self._scores is not None

    @property
    def hand(self):
        return self._hand

    @property
    def last_move(self):
        return self._last_move

    @property
    def my_strategies(self):
        strategies = self._params.get("number_of_strategies")
        return strategies[self._hand] if strategies is not None else 0

    @property
    def termination_probability(self):
        return self._params.get("termination_probability")

    def add_moves(self, moves):
        self._moves.append(moves)
        self.set_last_move(moves)

    def finish(self, scores):
        self._scores = scores or []

    def set_last_move(self, moves):
        self._last_move = moves
