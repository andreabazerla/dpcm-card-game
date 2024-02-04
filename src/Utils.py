from itertools import product
import json
import logging
import os
import sys
import numpy as np
import pandas as pd

def get_config():
    with open('config.json', 'r') as file:
        config = json.load(file)

    return config

def print_players(players, logger):
    for player in players:
        logger.info(player)

def clear_console():
    clear = lambda: os.system('cls')
    clear()

def get_states(players):
    states = []

    config = get_config()
    config_cards_deck = config['DECK']
    config_cards_zone = config_cards_deck['ZONE']
    config_cards_certification = config_cards_deck['CERTIFICATION']
    config_cards_wild = config_cards_deck['WILD']

    # Deck zone states
    states.append(np.arange(len(config_cards_zone) + 1, dtype=np.int8))

    # Number of cards in other players hand
    for _ in range(len(players) - 1):
        states.append(np.arange(4, dtype=np.int8))

    # Infected state
    states.append(np.arange(4, dtype=np.int8))

    # Playble cards in hand states
    for _ in range(len(config_cards_zone) + len(config_cards_certification) + len(config_cards_wild)):
        states.append(np.arange(2, dtype=np.int8))

    return list(product(*states))

def get_moves():
    moves = []

    config = get_config()
    config_cards_deck = config['DECK']
    config_cards_zone = config_cards_deck['ZONE']
    config_cards_certification = config_cards_deck['CERTIFICATION']
    config_cards_wild = config_cards_deck['WILD']

    for card_zone in config_cards_zone:
        moves.append("ZONE_" + card_zone)
        
    for card_certification in config_cards_certification:
        moves.append("CERTIFICATION_" + card_certification)

    for card_wild in config_cards_wild:
        moves.append("WILD_" + card_wild)

    return moves

def get_rewards(states, moves, players):
    R = np.zeros((len(states), len(moves)))
   
    state = [min(sum(states[i][1 + (len(players) - 1) + 1:]), 1) for i in range(len(states))]

    for i in range(len(states)):
        if state[i] == 0:
            R[i] = 1

    R = pd.DataFrame(
        data=R, 
        columns=moves, 
        index=states
    )

    R = R.astype('int8')
    return R

def get_size_in_gb(obj):
    size_in_bytes = sys.getsizeof(obj)
    size_in_gb = size_in_bytes / (1024 ** 3)
    return size_in_gb

def rotate_players(players):
    return players[1:] + players[:1]

def is_expected_winner(player_winner, players):
    return player_winner == players[0]

def get_logger(name, level=logging.INFO, console=None, file=None):
    logger = logging.getLogger(name)

    handlers = []
    if console:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        handlers.append(handler)
    if file:
        handler = logging.FileHandler(f'{file}')
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        handlers.append(handler)

    for handler in handlers:    
        logger.addHandler(handler)

    logger.setLevel(level)

    return logger

def clear_file(file):
    try:
        with open(f'{file}', 'r+') as file:
            file.truncate(0)
    except:
        pass