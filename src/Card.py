import random
from typing import Self

class CardType:
    CERTIFICATION = 'CERTIFICATION'
    ZONE = 'ZONE'
    WILD = 'WILD'

class CardColor:
    NONE = {
        'string': '_',
        'value': 0
    }

    WHITE = {
        'string': 'W',
        'value': 1
    }
    
    YELLOW = {
        'string': 'Y',
        'value': 2
    }

    ORANGE = {
        'string': 'O',
        'value': 3
    }

    RED = {
        'string': 'R',
        'value': 4
    }

    BLACK = {
        'string': 'B',
        'value': 5
    }

class CardWild:
    VACCINE = {
        'string': 'v',
        'value': 0
    }

    ONE = {
        'string': '1',
        'value': 1
    }

    TWO = {
        'string': '2',
        'value': 2
    }

    THREE = {
        'string': '3',
        'value': 3
    }
    
    SKIP = {
        'string': 's',
        'value': 4
    }

class Card:
    def __init__(self, type, data, name=None, description=None):
        self.type = type
        self.data = data
        self.name = name
        self.description = description

    def get_type(self):
        return self.type
    
    def get_data(self):
        return self.data

    def get_color(self):
        return self.data['string'] if self.data is not None else None
    
    def get_value(self):
        return self.data['value'] if self.data is not None else None
    
    def get_name(self):
        return self.name
    
    def is_zone(self):
        if self.get_type() == CardType.ZONE:
            return True
        return False

    def is_certification(self):
        if self.get_type() == CardType.CERTIFICATION:
            return True
        return False
    
    def is_wild(self):
        if self.get_type() == CardType.WILD:
            return True
        return False

    def __str__(self):
        if self.type == CardType.CERTIFICATION:
            return self.get_color().lower()
        elif self.type == CardType.ZONE:
            return self.get_color().upper()
        elif self.type == CardType.WILD:
            return self.get_data()['string'].upper()
        
    def __eq__(self, other):
        if isinstance(other, Card):
            if self.type == other.type:
                if self.get_data() == other.get_data():
                    return True
        return False

class Zone(Card):
    def __init__(self, data):
        super().__init__(type=CardType.ZONE, data=data)
    
    def is_playable(self, zone: Self):
        if zone is None or (zone is not None and self != zone and abs(self.get_value() - zone.get_value()) < 2 and (not zone.is_black() or (zone.is_black() and self.is_red()))):
            return True
        return False

    def is_white(self):
        return self == Zone(CardColor.WHITE)
    
    def is_yellow(self):
        return self == Zone(CardColor.YELLOW)

    def is_orange(self):
        return self == Zone(CardColor.ORANGE)
    
    def is_red(self):
        return self == Zone(CardColor.RED)

    def is_black(self):
        return self == Zone(CardColor.BLACK)
    
    def __str__(self):
        return self.get_color().upper()

class Certification(Card):
    def __init__(self, data):
        super().__init__(type=CardType.CERTIFICATION, data=data)

    def is_playable(self, zone):
        if zone.is_white() \
            or self.get_value() >= zone.get_value():
            return True
        return False
    
    def __str__(self):
        return self.get_color().lower()
    
class Wild(Card):
    def __init__(self, data):
        super().__init__(type=CardType.WILD, data=data)

    def is_vaccine(self):
        return self.get_value() == 0

    def is_covid(self):
        return self.get_value() > 0 and self.get_value() < 4
    
    def is_skip(self):
        return self.get_value() == 4
        
    def __str__(self):
        return self.get_data()['string']
    
def get_random_card(type=None, color=None):

    card_type = type
    if type != None:
        card_type = random.choice(list(CardType))
    
    card_color = color
    if color != None:
        card_color = random.choice(list(CardColor))

    return Card(card_type, card_color)