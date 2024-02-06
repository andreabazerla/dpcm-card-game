import numpy as np
import pandas as pd

from src.Player import Player
from src.Utils import get_config, get_moves, get_rewards, get_states, rotate_players
from src.Game import Game

class Turnament:
    def __init__(self, game_number, turnament_fair):
        self.game_number = game_number
        self.turnament_fair = turnament_fair

    def get_game_number(self):
        return self.game_number

    def is_turnament_fair(self):
        return self.turnament_fair
    
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
    
    def set_players(self, players):
        self.players = players

    def get_players(self):
        return self.players
    
    def start(self, logger, q, visited):
        config = get_config()

        players_config = config['PLAYERS']
        players = self.create_players(players_config)
        self.set_players(players)

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

            player_winner, turn, fake_winner, expected_winner = game.start(logger)

            if turnament % 10 == 0:
                state_seen = None
                for player in players:
                    if player.is_ai():
                        player_selected = player
                        state_seen = player.get_state_seen()
                        new_state_seen = {'Before': [state[0] for state in state_seen], 'After': [state[1] for state in state_seen]}
                        break
                if state_seen is not None:
                    try:
                        state_seen_df = pd.read_csv('data/state_seen.csv')

                        new_state_seen_df = pd.DataFrame(new_state_seen)

                        state_seen_df = pd.concat([state_seen_df, new_state_seen_df], ignore_index=True)
                    except:
                        state_seen_df = pd.DataFrame(new_state_seen)

                    state_seen_df.to_csv('data/state_seen.csv', index=False)

                if player_selected is not None:
                    player_selected.reset_state_seen()
            
            winner_list.append((player_winner, turn, fake_winner, expected_winner))

            if self.is_turnament_fair():
                players = rotate_players(players)

            turnament = turnament + 1

        return winner_list