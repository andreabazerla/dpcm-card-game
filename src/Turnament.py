import numpy as np
import pandas as pd

from src.Logger import Logger
from src.Player import Player
from src.Utils import get_config, get_moves, get_rewards, get_states, rotate_players
from src.Game import Game

class Turnament:
    def __init__(self, game_number):
        self.game_number = game_number

    def get_game_number(self):
        return self.game_number
    
    def create_players(self, players_config):
        players = []
        
        for player_config in players_config:
            name = player_config['NAME']
            ai = player_config['AI']

            epsilon = None
            step_size = None
            try:
                epsilon = player_config['EPSILON']
                step_size = player_config['STEP_SIZE']
            except KeyError:
                pass

            players.append(Player(name, ai, epsilon, step_size))

        return players
    
    def start_turnament(self, logger: Logger, q, visited):
        config = get_config()

        players_config = config['PLAYERS']
        players = self.create_players(players_config)

        states = get_states(players)
        moves = get_moves()
        rewards = get_rewards(states, moves, players)

        if q is None:
            q = pd.DataFrame(
                data = np.zeros((len(states), len(moves))), 
                columns = moves,
                index = states
            )

            visited = q.copy()

        for player in players:
            player.set_q(q)
            player.set_rewards(rewards)
            player.set_visited(visited)

        logger.info('TURNAMENT STARTED')
        logger.info('')

        turnament = 1
        winner_list = []
        for _ in range(self.get_game_number()):
            logger.info('Turnament: %s', turnament)

            game = Game(players)

            player_winner, loop, fake_winner, expected_winner = game.start(logger)

            winner_list.append((player_winner, loop, fake_winner, expected_winner))

            players = rotate_players(players)

            turnament = turnament + 1

            #time.sleep(0.005)

        return winner_list, q, visited