from game import Game
from random import seed, choice

seed()


class Prisoner:
    def __init__(self):
        self._games = {}

    def _create_game(self, game_id, hand, params):
        self._games[game_id] = Game(game_id, hand, params)
        return self._games[game_id]

    def _get_game(self, game_id):
        return self._games[game_id]

    # Game parameters: {'number_of_strategies': [2, 2], 'payoff': [[[-0.3220958709716797, -0.3220958709716797], [0.5778458118438721, -0.9093070030212402]], [[-0.9093070030212402, 0.5778458118438721], [0.47325587272644043, 0.47325587272644043]]], 'termination_probability': 0.0014068891759961843}
    def makeFirstMove(self, game_id, game_hand, game_params):
        game = self._create_game(game_id, game_hand, game_params)
        return self._think_about_it(game)


    # Game 716 end of turn, players moves are [1, 1]
    def makeNextMove(self, game_id, game_moves):
        game = self._get_game(game_id)
        # game.add_moves(game_moves)
        game.set_last_move(game_moves)
        return self._think_about_it(game)

    # Game 719 is finished with scores [0.8855123519897461, -1.1391820907592773]
    def acceptResult(self, game_id, game_scores):
        pass

    def _think_about_it(self, game):
        return choice(range(game.my_strategies))
