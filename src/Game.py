import time
from typing import List

from src.Logger import Logger
from src.Table import Table
from src.Deck import Deck
from src.Player import Player
from src.Utils import get_config, is_expected_winner, print_players

class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.deck = Deck()
        self.winner = None

    def reset_players(self):
        for player in self.get_players():
            player.reset()

    def get_winner(self):
        return self.winner

    def set_winner(self, winner):
        self.winner = winner

    def scan_winner(self, players):
        for player in players:
            if not player.get_cards():
                player.set_winner(True)
                return
            
    def search_winner(self, players):
        for player in players:
            if player.is_winner():
                return player

    def get_players(self):
        return self.players

    def get_deck(self): 
        return self.deck
    
    def get_players_live(self):
        player_live = []
        for player in self.get_players():
            if not player.is_winner():
                player_live.append(player)

        return player_live
    
    def is_game_over(self):
        for player in self.get_players():
            if player.is_winner():
                return True
        return False
    
    def check_game_over(self, logger:Logger, players:List[Player], loop):
        self.scan_winner(players)
       
        game_over = self.is_game_over()
        player_winner = None
        if game_over:
            player_winner = self.search_winner(players)
            self.set_winner(player_winner)

            logger.info('')
            logger.info(f'Game over!')
            logger.info(f'Winner: player {player_winner.get_name()}')
            logger.info(f'Loop: {loop}')
            logger.info('')
            
        return game_over, player_winner

    def start(self, logger: Logger):

        config = get_config()
        game_config = config['GAME']

        deck = self.get_deck()

        logger.info('')
        logger.info('GAME INIT')

        logger.info('')
        logger.info('Deck: %s', deck)

        table = Table(deck)

        logger.info('')
        logger.info('Table: %s', table)

        logger.info('')
        logger.info('Deck: %s', deck)

        players = self.get_players()

        self.reset_players()

        logger.info('')
        cards_per_player = game_config['CARDS_PER_PLAYER']
        for player in players:
            player.draw_from_deck(deck, table, cards_per_player)
            logger.info(player)

        logger.info('')
        logger.info('Deck: %s', deck)

        logger.info('')
        logger.info('GAME STARTED')
        logger.info('')

        loop = 1
        game_over = False
        quarantine = 0
        skip = False
        
        while True:
            
            logger.info('Loop: %s', loop)
            logger.info('')
            
            logger.info('Deck: %s', deck)

            logger.info('')
            logger.info('Table: %s', table)
            logger.info('')

            print_players(players)
            logger.info('')
        
            for player in players:

                logger.info('Turn of player: %s', player.get_name())
                logger.info('')

                if skip:
                    logger.info('Turn of player %s skipped', player.get_name())
                    logger.info('')
                    skip = False
                    continue

                card_stolen, card_gifted, next_player = player.swap_from_player(players)
                logger.info(f'Player {player.get_name()} stole card [{card_stolen}] and gifted [{card_gifted}] from/to player {next_player.get_name()}')

                logger.info('')
                print_players(players)
                logger.info('')

                card_played, certification_card, drew_from_deck, quarantine, infected, vaccinated, skip, move = player.play_cards(players, table, deck, quarantine)
                if not drew_from_deck:
                    if not infected:
                        logger_string = f'Player {player.get_name()} played [{card_played}] card'
                        
                        if certification_card:
                            logger_string += f' and then played [{certification_card}] card'
                        elif card_played.is_wild() and card_played.is_vaccine() and vaccinated:
                            logger_string += f' and recovered from COVID-19 with vaccine'
                        elif card_played.is_wild() and card_played.is_skip():
                            logger_string += f' and skip turn of player {player.get_next_player(players).get_name()}'
                    else:
                        logger_string = f'Player {player.get_name()} was infected and drew {quarantine} cards from deck'
                        quarantine = 0

                    logger.info(logger_string)
                else:
                    logger.info(f'Player {player.get_name()} drew from deck card [{card_played[0]}] and pass his turn')

                game_over, player_winner = self.check_game_over(logger, players, loop)
                if player_winner is not None:
                    if player_winner.is_ai():
                        state = player_winner.update_state(players, table, quarantine)
                        player_winner.update_q(state, move)

                    fake_winner = False

                    expected_winner = is_expected_winner(player_winner, players)

                    break

                logger.info('')
                logger.info('Deck: %s', deck)

                logger.info('')
                logger.info('Table: %s', table)
                logger.info('')

                print_players(players)
                logger.info('')
                
            if game_over:
                break

            loop = loop + 1

        return player_winner, loop, fake_winner, expected_winner