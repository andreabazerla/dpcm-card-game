import random

from src.Card import CardWild, Wild, Zone, Certification, CardColor, CardType
from src.Utils import get_config

class Deck:
    def __init__(self):
        self.cards = []

        config = get_config()

        deck_cards = config['DECK']
        zone_cards = deck_cards['ZONE']
        certification_cards = deck_cards['CERTIFICATION']
        wild_cards = deck_cards['WILD']

        for _ in range(zone_cards['WHITE']):
            self.cards.append(Zone(CardColor.WHITE))

        for _ in range(zone_cards['YELLOW']):
            self.cards.append(Zone(CardColor.YELLOW))
            
        for _ in range(zone_cards['ORANGE']):
            self.cards.append(Zone(CardColor.ORANGE))
            
        for _ in range(zone_cards['RED']):
            self.cards.append(Zone(CardColor.RED))

        for _ in range(zone_cards['BLACK']):
            self.cards.append(Zone(CardColor.BLACK))

        for _ in range(certification_cards['YELLOW']):
            self.cards.append(Certification(CardColor.YELLOW))
            
        for _ in range(certification_cards['ORANGE']):
            self.cards.append(Certification(CardColor.ORANGE))

        for _ in range(certification_cards['RED']):
            self.cards.append(Certification(CardColor.RED))

        for _ in range(wild_cards['VACCINE']):
            self.cards.append(Wild(CardWild.VACCINE))

        for _ in range(wild_cards['+1']):
            self.cards.append(Wild(CardWild.ONE))
        
        for _ in range(wild_cards['+2']):
            self.cards.append(Wild(CardWild.TWO))

        for _ in range(wild_cards['+3']):
            self.cards.append(Wild(CardWild.THREE))

        for _ in range(wild_cards['SKIP']):
            self.cards.append(Wild(CardWild.SKIP))

        random.shuffle(self.cards)

    def add_card(self, card):
        self.cards.appen(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def get_cards(self):
        return self.cards

    def set_cards(self, cards):
        self.cards = cards

    def draw_cards(self, table, cards_quantity):
        if not self.get_cards() or len(self.get_cards()) < cards_quantity:
            self.remake(table)
        
        cards = self.get_cards()[:cards_quantity]
        self.set_cards(self.get_cards()[cards_quantity:])
       
        return cards
    
    def remake(self, table):
        cards = table.remake(self)
            
        self.set_cards(cards)
        self.shuffle()
    
    def get_first_zone(self):
        for idx, card in enumerate(self.cards):
            if (card.type == CardType.DPCM):
                self.cards = self.cards[idx+1:]
                return card
            else:
                continue

    def __str__(self):
        cards_string = ''

        deck_cards = self.cards
        for card in deck_cards:
            cards_string = cards_string + str(card) + ' '

        return f'({str(len(deck_cards))}) {cards_string}'