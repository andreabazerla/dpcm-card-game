import random
from typing import List, Self

from src.Utils import get_moves
from src.Table import Table
from src.Deck import Deck
from src.Card import Card, CardColor, CardType, CardWild, Certification, Wild, Zone

class Player:
    def __init__(self, name, ai, epsilon, step_size):
        self.name = name
        self.ai = ai
        self.winner = False
        self.cards = []
        self.state = []
        self.moves = []
        self.rewards = None
        self.q = None
        self.visited = None
        self.previous_state = None
        self.previous_move = None
        self.epsilon = epsilon
        self.step_size = step_size

    def set_previous_state(self, previous_state):
        self.previous_state = previous_state

    def get_previous_state(self):
        return self.previous_state

    def set_previous_move(self, previous_move):
        self.previous_move = previous_move

    def get_previous_move(self):
        return self.previous_move

    def get_epsilon(self):
        return self.epsilon

    def get_step_size(self):
        return self.step_size

    def set_rewards(self, rewards):
        self.rewards = rewards
    
    def get_rewards(self):
        return self.rewards

    def set_q(self, q):
        self.q = q
    
    def get_q(self):
        return self.q

    def set_visited(self, visited):
        self.visited = visited

    def get_visited(self):
        return self.visited

    def get_name(self):
        return self.name
    
    def is_ai(self):
        return self.ai

    def get_cards(self):
        return self.cards

    def set_cards(self, cards):
        self.cards = cards
    
    def set_discareded(self, discarded):
        self.discarded = discarded

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_moves(self, moves):
        self.moves = moves

    def get_moves(self):
        return self.moves
    
    def is_winner(self):
        return self.winner
    
    def set_winner(self, winner):
        self.winner = winner
    
    def draw_from_player(self, players):
        next_player = self.get_next_player(players)
        card_stolen = self.execute_draw_player(next_player)

        return card_stolen, next_player
    
    def execute_draw_player(self, next_player:Self):
        card_stolen = random.choice(next_player.get_cards())
        next_player.remove_card(card_stolen)
        self.add_card(card_stolen)

        return card_stolen
    
    def swap_from_player(self, players:List[Self]):
        next_player = self.get_next_player(players)
        card_stolen, card_gifted = self.execute_swap_player(next_player)

        return card_stolen, card_gifted, next_player
    
    def get_next_player(self, players:List[Self]):
        index = players.index(self)
       
        players_number = len(players)
    
        if index < 0 or index >= players_number:
            return None

        next_index = (index + 1) % players_number

        return players[next_index]
    
    def execute_swap_player(self, player:Self):
        card_stolen = random.choice(player.get_cards())
        player.remove_card(card_stolen)

        card_gifted = random.choice(self.get_cards())
        self.remove_card(card_gifted)
        
        self.add_card(card_stolen)
        player.add_card(card_gifted)

        return card_stolen, card_gifted
    
    def draw_player_random(self, players):
        move_choosen = None
        move_labels = get_moves(players)[1:3]
        moves = self.get_moves()[1:3]
        moves_possible = [move_label for move, move_label in zip(moves, move_labels) if move == 1]
        
        if moves_possible:
            random.shuffle(moves_possible)
            move_choosen = random.choice(moves_possible)

        return move_choosen

    def choose_player(self, players):
        nearby_players = self.get_nearby_players(players)
        return random.choice(nearby_players)

    def get_nearby_players(self, players):
        index = players.index(self)
       
        players_number = len(players)
    
        if index < 0 or index >= players_number:
            return None

        previous_index = (index - 1) % players_number
        next_index = (index + 1) % players_number

        previous_player = players[previous_index]
        next_player = players[next_index]

        return previous_player, next_player
    
    def steal_card(self, player):
        card_choosen = random.choice(player.get_cards())

        player.cards.remove(card_choosen)

        return card_choosen
    
    def add_card(self, card):
        self.get_cards().append(card)

    def draw_from_deck(self, deck:Deck, table:Table, cards_number=1):
        new_cards = deck.draw_cards(table, cards_number)
        self.cards.extend(new_cards)
        return new_cards

    def play_cards(self, players:List[Self], table:Table, deck:Deck, quarantine):
        state = self.update_state(players, table, quarantine)
        self.update_moves(players, table)

        drew_from_deck = False
        if self.is_ai():
            move = self.play_card_ai()
        else:
            move = self.play_card_random()

        move_final = move
        
        certification_card = None
        infected = False
        vaccinated = False
        skip = False
        if move is None and quarantine == 0:
            card = self.draw_from_deck(deck, table)
            drew_from_deck = True
        else:
            card, quarantine, infected, vaccinated, skip = self.execute_move(move, table, quarantine)

            if not infected:
                if card is not None and card.is_zone() and not card.is_black():
                    self.update_state(players, table, quarantine)
                    self.update_moves(players, table, certification=True)

                    if self.is_ai():
                        move_plus = self.play_card_ai()
                    else:
                        move_plus = self.play_card_random()
                    
                    if move_plus is not None:
                        certification_card, _, _, _, _ = self.execute_move(move_plus, table, quarantine)

                        if self.is_ai():
                            self.update_q(state, move)

                        self.set_previous_state(state)
                        self.set_previous_move(move)
                        
                        self.update_visited(move_plus)

                        move_final = move_plus
                
                if self.is_ai():
                    self.update_q(state, move)

                self.set_previous_state(state)
                self.set_previous_move(move)

                self.update_visited(move)
            else:
                self.draw_from_deck(deck, table, quarantine)

        return card, certification_card, drew_from_deck, quarantine, infected, vaccinated, skip, move_final
    
    def update_visited(self, move):
        iloc_previous_state = self.get_q().index.get_loc(tuple(self.get_previous_state()))
        self.visited.iloc[iloc_previous_state][move] += 1

    def update_q(self, state, move):
        if self.get_previous_move() is not None:
            iloc_previous_state = self.q.index.get_loc(tuple(self.get_previous_state()))
            iloc_state = self.q.index.get_loc(tuple(state))

            previous_q = self.q.iloc[iloc_previous_state][self.get_previous_move()]
            this_q = self.q.iloc[iloc_state][move]
            reward = self.rewards.iloc[iloc_state][move]
            
            if reward == 0:
                self.q.iloc[iloc_previous_state][self.get_previous_move()] = previous_q + self.get_step_size() * (reward + this_q - previous_q) 
            else:
                self.q.iloc[iloc_previous_state][self.get_previous_move()] = previous_q + self.get_step_size() * (reward - previous_q)

    def execute_draw_from_player(self, player:Self):
        card = random.choice(player.get_cards())
        
        player.remove_card(card)
        self.add_card(card)

        return card

    def execute_move(self, move, table:Table, quarantine):
        moves_possible = get_moves()

        card = self.get_card_by_move(move)

        infected = False
        vaccinated = False
        skip = False
        if move == moves_possible[0] \
            or move == moves_possible[1] \
            or move == moves_possible[2] \
            or move == moves_possible[3] \
            or move == moves_possible[4]:
            
            if quarantine > 0:
                infected = True
            else:
                table.play_zone(card)
                self.remove_card(card)
        elif move == moves_possible[5] \
            or move == moves_possible[6] \
            or move == moves_possible[7]:
            
            if quarantine > 0:
                infected = True
            else:
                table.play_certification(card)
                self.remove_card(card)
        elif move == moves_possible[8]:
            infected = False
            vaccinated = True

            table.play_certification(card)
            self.remove_card(card)
        elif move == moves_possible[9] \
            or move == moves_possible[10] \
            or move == moves_possible[11]:
            
            if quarantine > 0:
                infected = True
            else:
                quarantine = card.get_value()
                table.play_certification(card)
                self.remove_card(card)
        elif move == moves_possible[12]:
            if quarantine > 0:
                infected = True
            else:
                skip = True
                table.play_certification(card)
                self.remove_card(card)
        else:
            if quarantine > 0:
                infected = True
        
        return card, quarantine, infected, vaccinated, skip

    def draw_cards(self, player, cards_quantity, deck, table):
        player.draw_from_deck(deck, table, cards_quantity)
    
    def get_card_by_move(self, move):
        moves_possible = get_moves()

        card = None
        if move == moves_possible[0]:
            card = Zone(CardColor.WHITE)
        elif move == moves_possible[1]:
            card = Zone(CardColor.YELLOW)
        elif move == moves_possible[2]:
            card = Zone(CardColor.ORANGE)
        elif move == moves_possible[3]:
            card = Zone(CardColor.RED)
        elif move == moves_possible[4]:
            card = Zone(CardColor.BLACK)
        elif move == moves_possible[5]:
            card = Certification(CardColor.YELLOW)
        elif move == moves_possible[6]:
            card = Certification(CardColor.ORANGE)
        elif move == moves_possible[7]:
            card = Certification(CardColor.RED)
        elif move == moves_possible[8]:
            card = Wild(CardWild.VACCINE)
        elif move == moves_possible[9]:
            card = Wild(CardWild.ONE)
        elif move == moves_possible[10]:
            card = Wild(CardWild.TWO)
        elif move == moves_possible[11]:
            card = Wild(CardWild.THREE)
        elif move == moves_possible[12]:
            card = Wild(CardWild.SKIP)

        return card
        
    def play_card_ai(self):
        move_choosen = None
        
        move_labels = get_moves()
        moves = self.get_moves()
        
        moves_possible = [move_label for move, move_label in zip(moves, move_labels) if move == 1]

        if not moves_possible:
            return None

        random.shuffle(moves_possible)
        
        if len(moves_possible) > 0:
            if random.random() < self.get_epsilon():
                move_choosen = random.choice(moves_possible)
            else:
                val_max = 0
                for move in moves_possible:
                    iloc = self.q.index.get_loc(tuple(self.get_state()))
                    val = self.q.iloc[iloc][move]
                    if val >= val_max: 
                        val_max = val
                        move_choosen = move
        
        return move_choosen
    
    def draw_player_ai(self, players):
        move_choosen = None
        move_labels = get_moves(players)[1:3]
        moves = self.get_moves()[1:3]
        moves_possible = [move_label for move, move_label in zip(moves, move_labels) if move == 1]
        random.shuffle(moves_possible)
        
        if len(moves_possible) > 0:
            if random.random() < self.get_epsilon():
                move_choosen = random.choice(moves_possible)
            else:
                val_max = 0
                for move in moves_possible:
                    iloc = self.q.index.get_loc(tuple(self.get_state()))
                    val = self.q.iloc[iloc][move]
                    if val >= val_max: 
                        val_max = val
                        move_choosen = move
        
        return move_choosen
    
    def get_other_players(self, players: List[Self]):
        other_players = []

        for player in players:
            if not self == player:
                other_players.append(player)
            
        return other_players

    def update_state(self, players:List[Self], table:Table, quarantine):
        other_players = self.get_other_players(players)
        
        state = []

        state.append(table.get_top_zone().get_value())
        
        for other_player in other_players:
            cards_quantity = len(other_player.get_cards())
            if cards_quantity == 0:
                state.append(0)
            elif cards_quantity < 2:
                state.append(1)
            elif cards_quantity < 6:
                state.append(2)
            else:
                state.append(3)

        state.append(quarantine)

        state.append(self.player_is(CardType.ZONE, CardColor.WHITE))
        state.append(self.player_is(CardType.ZONE, CardColor.YELLOW))
        state.append(self.player_is(CardType.ZONE, CardColor.ORANGE))
        state.append(self.player_is(CardType.ZONE, CardColor.RED))
        state.append(self.player_is(CardType.ZONE, CardColor.BLACK))
        state.append(self.player_is(CardType.CERTIFICATION, CardColor.YELLOW))
        state.append(self.player_is(CardType.CERTIFICATION, CardColor.ORANGE))
        state.append(self.player_is(CardType.CERTIFICATION, CardColor.RED))
        state.append(self.player_is(CardType.WILD, CardWild.VACCINE))
        state.append(self.player_is(CardType.WILD, CardWild.ONE))
        state.append(self.player_is(CardType.WILD, CardWild.TWO))
        state.append(self.player_is(CardType.WILD, CardWild.THREE))
        state.append(self.player_is(CardType.WILD, CardWild.SKIP))

        self.set_state(state)

        return state
    
    def get_cards_state(self, players):
        return self.get_state()[1 + (len(players) - 1) + 1: ]

    def update_moves(self, players:List[Self], table:Table, certification=False):
        cards_state = self.get_cards_state(players)
        move_labels = get_moves()

        moves = [None] * len(move_labels)
        for move_index, move_label in enumerate(move_labels):
            move_value = 0

            if move_label == move_labels[0]: # ZONE_WHITE
                if cards_state[0] > 0:
                    if not table.has_top_zone(Zone(CardColor.WHITE)):
                        if not certification:
                            move_value = 1
            elif move_label == move_labels[1]: # ZONE_YELLOW
                if cards_state[1] > 0:
                    if table.has_top_zone(Zone(CardColor.NONE)) \
                        or table.has_top_zone(Zone(CardColor.WHITE)) \
                        or table.has_top_zone(Zone(CardColor.ORANGE)):
                        if not certification:
                            move_value = 1
            elif move_label == move_labels[2]: # ZONE_ORANGE
                if cards_state[2] > 0:
                    if table.has_top_zone(Zone(CardColor.NONE)) \
                        or table.has_top_zone(Zone(CardColor.YELLOW)) \
                        or table.has_top_zone(Zone(CardColor.RED)):
                        if not certification:
                            move_value = 1
            elif move_label == move_labels[3]: # ZONE_RED
                if cards_state[3] > 0:
                    if table.has_top_zone(Zone(CardColor.NONE)) \
                        or table.has_top_zone(Zone(CardColor.ORANGE)) \
                        or table.has_top_zone(Zone(CardColor.BLACK)):
                        if not certification:
                            move_value = 1
            elif move_label == move_labels[4]: # ZONE_BLACK
                if cards_state[4] > 0:
                    if not table.has_top_zone(Zone(CardColor.BLACK)):
                        if not certification:
                            move_value = 1
            elif move_label == move_labels[5]: # CERTIFICATION_YELLOW
                if cards_state[5] > 0:
                    if table.has_top_zone(Zone(CardColor.WHITE)) \
                        or table.has_top_zone(Zone(CardColor.YELLOW)):
                            move_value = 1
            elif move_label == move_labels[6]: # CERTIFICATION_ORANGE
                if cards_state[6] > 0:
                    if table.has_top_zone(Zone(CardColor.WHITE)) \
                        or table.has_top_zone(Zone(CardColor.YELLOW)) \
                        or table.has_top_zone(Zone(CardColor.ORANGE)):
                            move_value = 1
            elif move_label == move_labels[7]: # CERTIFICATION_RED
                if cards_state[7] > 0:
                    if table.has_top_zone(Zone(CardColor.WHITE)) \
                        or table.has_top_zone(Zone(CardColor.YELLOW)) \
                        or table.has_top_zone(Zone(CardColor.ORANGE)) \
                        or table.has_top_zone(Zone(CardColor.RED)):
                            move_value = 1
            elif move_label == move_labels[8]: # WILD_VACCINE
                if cards_state[8] > 0:
                    if not certification:
                        move_value = 1
            elif move_label == move_labels[9]: # WILD_+1
                if cards_state[9] > 0:
                    if not certification:
                        move_value = 1
            elif move_label == move_labels[10]: # WILD_+2
                if cards_state[10] > 0:
                    if not certification:
                        move_value = 1
            elif move_label == move_labels[11]: # WILD_+3
                if cards_state[11] > 0:
                    if not certification:
                        move_value = 1
            elif move_label == move_labels[12]: # WILD_SKIP
                if cards_state[12] > 0:
                    if not certification:
                        move_value = 1
                    
            moves[move_index] = move_value

        self.set_moves(moves)

        return moves
    
    def is_player_live(self, players, player_index):
        player = self.get_player(players, player_index)
        return not player.is_winner()
    
    def get_player(self, players, player_index):
        other_players = self.get_other_players(players)
        return other_players[player_index]
    
    def player_is(self, card_type, card_data):
        if Card(card_type, card_data) in self.get_cards():
            return 1
        return 0
        
    def play_card_random(self):
        move_choosen = None
        
        move_labels = get_moves()
        moves = self.get_moves()
        
        moves_possible = [move_label for move, move_label in zip(moves, move_labels) if move == 1]

        if not moves_possible:
            return None
        
        if moves_possible:
            random.shuffle(moves_possible)
            move_choosen = random.choice(moves_possible)

        return move_choosen

    def execute_random_move(self, moves):
        random.shuffle(moves)
        return self.execute_move(moves[0])

    def play_zone(self, card_zone, player):
        card_return = []

        player.set_zone(card_zone)
        self.remove_card(card_zone)

        card_return.append(card_zone)

        if self == player:
            card_certification = self.search_certification()
            if card_certification:
                self.play_certification(card_certification)
                card_return.append(card_certification)

        return card_return

    def play_certification(self, card):
        self.remove_card(card)
        return [card]
    
    def search_certification(self):
        for card in self.get_cards():
            if card.is_certification():
                if card.is_playable(self.get_zone()):
                    return card
        return None

    def get_random_card(self):
        self.shuffle_cards()
        return self.cards[0]
    
    def shuffle_cards(self):
        random.shuffle(self.cards)
        
    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            
    def reset(self):
        self.set_cards([])
        self.set_state([])
        self.set_moves([])
        self.set_winner(False)
        self.set_previous_state(None)
        self.set_previous_move(None)

    def __eq__(self, other):
        if isinstance(other, Player):
            if self.get_name() == other.get_name():
                return True
        return False
    
    def __str__(self):
        cards_string = ''

        player_cards = self.get_cards()
        for card in player_cards:
            cards_string = cards_string + card.__str__() + ' '

        return f'Player {self.name}: ({len(player_cards):2d}) {cards_string}'